package com.borderless.app.domain.model

data class QaInteraction(
    val answer: String,
    val riskRating: RiskRating,
    val sources: List<QaSource>,
    val language: String,
    val responseTimeMs: Long
)

data class QaSource(
    val alertId: String,
    val title: String,
    val source: String
)

enum class RiskRating {
    LOW,
    MEDIUM,
    HIGH,
    CRITICAL;

    companion object {
        fun fromString(value: String): RiskRating = when (value.lowercase()) {
            "low" -> LOW
            "medium" -> MEDIUM
            "high" -> HIGH
            "critical" -> CRITICAL
            else -> LOW
        }
    }

    fun toApiValue(): String = name.lowercase()

    fun displayName(): String = name.lowercase()
        .replaceFirstChar { it.uppercase() }
}
