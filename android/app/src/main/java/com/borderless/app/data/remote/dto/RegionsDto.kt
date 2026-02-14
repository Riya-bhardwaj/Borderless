package com.borderless.app.data.remote.dto

import com.borderless.app.domain.model.GeofenceDefinition
import com.borderless.app.domain.model.Region
import com.borderless.app.domain.model.RegionType

data class RegionsResponse(
    val regions: List<RegionDto>,
    val lastUpdated: String
)

data class RegionDto(
    val id: String,
    val name: String,
    val type: String,
    val parentId: String?,
    val geofences: List<GeofenceDto>,
    val quickFacts: List<String>,
    val alertCount: Int
) {
    fun toDomainModel(): Region = Region(
        id = id,
        name = name,
        type = RegionType.fromString(type),
        parentId = parentId,
        geofences = geofences.map { it.toDomainModel() },
        quickFacts = quickFacts,
        alertCount = alertCount
    )
}

data class GeofenceDto(
    val lat: Double,
    val lng: Double,
    val radiusMeters: Float,
    val label: String
) {
    fun toDomainModel(): GeofenceDefinition = GeofenceDefinition(
        lat = lat,
        lng = lng,
        radiusMeters = radiusMeters,
        label = label
    )
}
