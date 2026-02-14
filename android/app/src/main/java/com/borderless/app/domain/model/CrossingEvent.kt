package com.borderless.app.domain.model

data class CrossingEvent(
    val id: String,
    val fromRegionId: String,
    val fromRegionName: String,
    val toRegionId: String,
    val toRegionName: String,
    val latitude: Double,
    val longitude: Double,
    val alertsDelivered: Int,
    val timestamp: String
)
