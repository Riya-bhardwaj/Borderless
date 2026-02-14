package com.borderless.app.ui.qa

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.borderless.app.domain.model.QaInteraction
import com.borderless.app.domain.repository.RegionRepository
import com.borderless.app.domain.repository.UserRepository
import com.borderless.app.domain.usecase.AskQuestionUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.util.Locale
import javax.inject.Inject

data class QaUiState(
    val question: String = "",
    val isLoading: Boolean = false,
    val currentAnswer: QaInteraction? = null,
    val error: String? = null,
    val currentRegionId: String? = null,
    val currentRegionName: String? = null,
    val language: String = "en",
    val history: List<QaHistoryItem> = emptyList(),
    val isListening: Boolean = false,
    val voiceRmsDb: Float = 0f,
    val partialText: String = ""
)

data class QaHistoryItem(
    val question: String,
    val answer: QaInteraction
)

@HiltViewModel
class QaViewModel @Inject constructor(
    private val askQuestionUseCase: AskQuestionUseCase,
    private val regionRepository: RegionRepository,
    private val userRepository: UserRepository,
    @ApplicationContext private val appContext: Context
) : ViewModel() {

    private val _uiState = MutableStateFlow(QaUiState())
    val uiState: StateFlow<QaUiState> = _uiState.asStateFlow()

    private val mainHandler = Handler(Looper.getMainLooper())
    private var speechRecognizer: SpeechRecognizer? = null

    init {
        loadContext()
    }

    private fun loadContext() {
        viewModelScope.launch {
            val user = userRepository.getCurrentUser()
            val regions = regionRepository.getRegions()

            val firstRegion = regions.getOrNull()?.firstOrNull()
            _uiState.update {
                it.copy(
                    currentRegionId = firstRegion?.id,
                    currentRegionName = firstRegion?.name,
                    language = user?.language ?: "en"
                )
            }
        }
    }

    fun updateQuestion(question: String) {
        _uiState.update { it.copy(question = question, error = null) }
    }

    fun selectRegion(regionId: String, regionName: String) {
        _uiState.update {
            it.copy(currentRegionId = regionId, currentRegionName = regionName)
        }
    }

    fun startListening() {
        mainHandler.post {
            if (!SpeechRecognizer.isRecognitionAvailable(appContext)) {
                _uiState.update { it.copy(error = "Speech recognition not available on this device") }
                return@post
            }

            stopListeningInternal()

            speechRecognizer = SpeechRecognizer.createSpeechRecognizer(appContext).apply {
                setRecognitionListener(object : RecognitionListener {
                    override fun onReadyForSpeech(params: Bundle?) {
                        Log.d("QaViewModel", "Ready for speech")
                        _uiState.update { it.copy(isListening = true, partialText = "", voiceRmsDb = 0f) }
                    }

                    override fun onBeginningOfSpeech() {
                        Log.d("QaViewModel", "Speech started")
                    }

                    override fun onRmsChanged(rmsdB: Float) {
                        _uiState.update { it.copy(voiceRmsDb = rmsdB.coerceAtLeast(0f)) }
                    }

                    override fun onBufferReceived(buffer: ByteArray?) {}

                    override fun onEndOfSpeech() {
                        Log.d("QaViewModel", "Speech ended")
                        _uiState.update { it.copy(isListening = false) }
                    }

                    override fun onError(error: Int) {
                        val errorMsg = when (error) {
                            SpeechRecognizer.ERROR_AUDIO -> "Audio recording error"
                            SpeechRecognizer.ERROR_CLIENT -> "Client error"
                            SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS -> "Microphone permission required"
                            SpeechRecognizer.ERROR_NETWORK -> "Network error - check internet"
                            SpeechRecognizer.ERROR_NETWORK_TIMEOUT -> "Network timeout"
                            SpeechRecognizer.ERROR_NO_MATCH -> "Couldn't understand. Please try again."
                            SpeechRecognizer.ERROR_RECOGNIZER_BUSY -> "Recognizer busy"
                            SpeechRecognizer.ERROR_SERVER -> "Server error"
                            SpeechRecognizer.ERROR_SPEECH_TIMEOUT -> "No speech detected. Please try again."
                            else -> "Speech recognition error ($error)"
                        }
                        Log.e("QaViewModel", "Speech error: $errorMsg (code=$error)")
                        _uiState.update { it.copy(isListening = false, error = errorMsg) }
                    }

                    override fun onResults(results: Bundle?) {
                        val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                        val spokenText = matches?.firstOrNull()
                        Log.d("QaViewModel", "Speech results: $spokenText")
                        if (!spokenText.isNullOrBlank()) {
                            _uiState.update { it.copy(question = spokenText, isListening = false) }
                            askQuestion()
                        } else {
                            _uiState.update { it.copy(isListening = false, error = "Couldn't understand. Please try again.") }
                        }
                    }

                    override fun onPartialResults(partialResults: Bundle?) {
                        val partial = partialResults?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                        val partialText = partial?.firstOrNull()
                        if (!partialText.isNullOrBlank()) {
                            _uiState.update { it.copy(partialText = partialText) }
                        }
                    }

                    override fun onEvent(eventType: Int, params: Bundle?) {}
                })
            }

            val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale("en", "IN").toLanguageTag())
                putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, Locale("en", "IN").toLanguageTag())
                putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true)
                putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 3)
                putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_MINIMUM_LENGTH_MILLIS, 5000L)
                putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_COMPLETE_SILENCE_LENGTH_MILLIS, 3000L)
                putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_POSSIBLY_COMPLETE_SILENCE_LENGTH_MILLIS, 3000L)
            }

            Log.d("QaViewModel", "Starting speech recognizer")
            speechRecognizer?.startListening(intent)
        }
    }

    fun stopListening() {
        mainHandler.post { stopListeningInternal() }
    }

    private fun stopListeningInternal() {
        speechRecognizer?.apply {
            stopListening()
            cancel()
            destroy()
        }
        speechRecognizer = null
        _uiState.update { it.copy(isListening = false, voiceRmsDb = 0f, partialText = "") }
    }

    fun askQuestion() {
        val state = _uiState.value
        val regionId = state.currentRegionId ?: return
        val question = state.question.trim()

        if (question.isBlank()) {
            _uiState.update { it.copy(error = "Please enter a question") }
            return
        }

        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null, currentAnswer = null) }

            askQuestionUseCase(regionId, question, state.language)
                .onSuccess { answer ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            currentAnswer = answer,
                            question = "",
                            history = it.history + QaHistoryItem(question, answer)
                        )
                    }
                }
                .onFailure { error ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            error = error.message ?: "Failed to get answer. Please try again."
                        )
                    }
                }
        }
    }

    fun clearError() {
        _uiState.update { it.copy(error = null) }
    }

    override fun onCleared() {
        super.onCleared()
        mainHandler.post { stopListeningInternal() }
    }
}
