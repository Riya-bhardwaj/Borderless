package com.borderless.app.domain.model

data class Region(
    val id: String,
    val name: String,
    val type: RegionType,
    val parentId: String? = null,
    val geofences: List<GeofenceDefinition> = emptyList(),
    val quickFacts: List<String> = emptyList(),
    val alertCount: Int = 0,
    val active: Boolean = true
)

enum class RegionType {
    COUNTRY,
    STATE,
    CITY;

    companion object {
        fun fromString(value: String): RegionType = when (value.lowercase()) {
            "country" -> COUNTRY
            "state" -> STATE
            "city" -> CITY
            else -> STATE
        }
    }

    fun toApiValue(): String = name.lowercase()
}
