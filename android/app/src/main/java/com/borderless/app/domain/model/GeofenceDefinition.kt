package com.borderless.app.domain.model

data class GeofenceDefinition(
    val lat: Double,
    val lng: Double,
    val radiusMeters: Float,
    val label: String
)
