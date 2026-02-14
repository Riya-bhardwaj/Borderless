package com.borderless.app.data.remote.dto

import com.borderless.app.domain.model.QaInteraction
import com.borderless.app.domain.model.QaSource
import com.borderless.app.domain.model.RiskRating

data class QaRequest(
    val regionId: String,
    val question: String,
    val language: String = "en"
)

data class QaResponse(
    val answer: String,
    val riskRating: String,
    val sources: List<QaSourceDto>,
    val language: String,
    val responseTimeMs: Long
) {
    fun toDomainModel(): QaInteraction = QaInteraction(
        answer = answer,
        riskRating = RiskRating.fromString(riskRating),
        sources = sources.map { it.toDomainModel() },
        language = language,
        responseTimeMs = responseTimeMs
    )
}

data class QaSourceDto(
    val alertId: String,
    val title: String,
    val source: String
) {
    fun toDomainModel(): QaSource = QaSource(
        alertId = alertId,
        title = title,
        source = source
    )
}
