package com.borderless.app.service

import android.content.Context
import com.borderless.app.BuildConfig
import com.borderless.app.R
import com.borderless.app.domain.model.AlertEntry
import com.borderless.app.domain.model.QaInteraction
import com.borderless.app.domain.model.QaSource
import com.borderless.app.domain.model.Region
import com.borderless.app.domain.model.RiskRating
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.util.concurrent.TimeUnit
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class GeminiService @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private val apiKey = BuildConfig.GEMINI_API_KEY
    private val modelName = "gemini-2.5-flash"
    private val baseUrl = "https://generativelanguage.googleapis.com/v1beta/models"

    private val httpClient by lazy {
        OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(60, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .build()
    }

    private val systemPrompt by lazy {
        context.resources.openRawResource(R.raw.qa_system_prompt)
            .bufferedReader()
            .use { it.readText() }
    }

    suspend fun askQuestion(
        question: String,
        region: Region,
        alerts: List<AlertEntry>,
        language: String,
        userDisplayName: String? = null
    ): Result<QaInteraction> = withContext(Dispatchers.IO) {
        runCatching {
            val startTime = System.currentTimeMillis()

            val prompt = buildPrompt(
                question = question,
                region = region,
                alerts = alerts,
                language = language,
                userDisplayName = userDisplayName
            )

            val responseText = callGeminiApi(prompt)
            parseResponse(responseText, language, startTime)
        }
    }

    private fun callGeminiApi(prompt: String): String {
        val url = "$baseUrl/$modelName:generateContent?key=$apiKey"

        val requestBody = JSONObject().apply {
            put("contents", JSONArray().put(
                JSONObject().apply {
                    put("parts", JSONArray().put(
                        JSONObject().apply {
                            put("text", prompt)
                        }
                    ))
                }
            ))
            put("generationConfig", JSONObject().apply {
                put("temperature", 0.4)
                put("topK", 40)
                put("topP", 0.95)
                put("maxOutputTokens", 1024)
            })
        }

        val request = Request.Builder()
            .url(url)
            .post(requestBody.toString().toRequestBody("application/json".toMediaType()))
            .build()

        val response = httpClient.newCall(request).execute()
        val body = response.body?.string() ?: throw Exception("Empty response body")

        if (!response.isSuccessful) {
            throw Exception("Gemini API error ${response.code}: $body")
        }

        val json = JSONObject(body)
        val candidates = json.optJSONArray("candidates")
            ?: throw Exception("No candidates in response")
        val content = candidates.getJSONObject(0)
            .getJSONObject("content")
        val parts = content.getJSONArray("parts")
        return parts.getJSONObject(0).getString("text")
    }

    private fun buildPrompt(
        question: String,
        region: Region,
        alerts: List<AlertEntry>,
        language: String,
        userDisplayName: String?
    ): String = buildString {
        // System prompt
        append(systemPrompt)
        append("\n\n")

        // User context
        if (!userDisplayName.isNullOrBlank()) {
            append("User: $userDisplayName\n")
        }
        append("User's current location: ${region.name} (${region.type.name.lowercase()})\n")
        append("Response Language: $language\n")
        append("Note: The user is currently in ${region.name}, but their question may be about ANY place in India. Answer about the place they are asking about, not their current location.\n\n")

        // Quick facts about current region (as additional context)
        if (region.quickFacts.isNotEmpty()) {
            append("Quick facts about user's current region (${region.name}):\n")
            region.quickFacts.forEach { fact ->
                append("- $fact\n")
            }
            append("\n")
        }

        // Alert data as grounding context (if available)
        if (alerts.isNotEmpty()) {
            append("Available alert data for grounding:\n")
            val alertsArray = JSONArray()
            for (alert in alerts) {
                alertsArray.put(JSONObject().apply {
                    put("id", alert.id)
                    put("category", alert.category.toApiValue())
                    put("severity", alert.severity.toApiValue())
                    put("title", alert.title)
                    put("description", alert.description)
                    put("source", alert.source)
                    if (alert.tags.isNotEmpty()) {
                        put("tags", JSONArray(alert.tags))
                    }
                })
            }
            append(alertsArray.toString(2))
        } else {
            append("No alert data available for this region. Use your own knowledge to answer.")
        }
        append("\n\n")

        // User question
        append("User question: $question\n\n")

        // Expected output
        append("Respond with a JSON object containing: ")
        append("\"answer\" (string), ")
        append("\"riskRating\" (one of: \"low\", \"medium\", \"high\", \"critical\"), ")
        append("\"sources\" (array of {\"alertId\", \"title\", \"source\"} from alerts you referenced, or empty array [] if none used).")
    }

    private fun parseResponse(
        responseText: String,
        language: String,
        startTime: Long
    ): QaInteraction {
        val jsonText = extractJson(responseText)
        val json = JSONObject(jsonText)

        val answer = json.optString("answer", "No answer generated.")
        val riskRating = json.optString("riskRating", "low")
        val sourcesArray = json.optJSONArray("sources") ?: JSONArray()

        val sources = (0 until sourcesArray.length()).map { i ->
            val src = sourcesArray.getJSONObject(i)
            QaSource(
                alertId = src.optString("alertId", ""),
                title = src.optString("title", ""),
                source = src.optString("source", "")
            )
        }

        return QaInteraction(
            answer = answer,
            riskRating = RiskRating.fromString(riskRating),
            sources = sources,
            language = language,
            responseTimeMs = System.currentTimeMillis() - startTime
        )
    }

    private fun extractJson(text: String): String {
        // Try markdown code block first
        val codeBlockMatch = """```(?:json)?\s*(\{[\s\S]*?\})\s*```""".toRegex().find(text)
        if (codeBlockMatch != null) return codeBlockMatch.groupValues[1]

        // Try raw JSON object
        val jsonMatch = """\{[\s\S]*\}""".toRegex().find(text)
        return jsonMatch?.value ?: text
    }
}
