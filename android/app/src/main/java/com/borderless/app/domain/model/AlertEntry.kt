package com.borderless.app.domain.model

data class AlertEntry(
    val id: String,
    val category: AlertCategory,
    val severity: AlertSeverity,
    val title: String,
    val description: String,
    val source: String,
    val tags: List<String> = emptyList()
)

enum class AlertCategory {
    LEGAL,
    CULTURAL,
    BEHAVIORAL;

    companion object {
        fun fromString(value: String): AlertCategory = when (value.lowercase()) {
            "legal" -> LEGAL
            "cultural" -> CULTURAL
            "behavioral" -> BEHAVIORAL
            else -> BEHAVIORAL
        }
    }

    fun toApiValue(): String = name.lowercase()

    fun displayName(): String = name.lowercase()
        .replaceFirstChar { it.uppercase() }
}

enum class AlertSeverity(val sortOrder: Int) {
    CRITICAL(0),
    IMPORTANT(1),
    INFORMATIONAL(2);

    companion object {
        fun fromString(value: String): AlertSeverity = when (value.lowercase()) {
            "critical" -> CRITICAL
            "important" -> IMPORTANT
            "informational" -> INFORMATIONAL
            else -> INFORMATIONAL
        }
    }

    fun toApiValue(): String = name.lowercase()

    fun displayName(): String = name.lowercase()
        .replaceFirstChar { it.uppercase() }
}
