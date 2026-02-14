package com.borderless.app.data.remote.dto

data class CrossingRequest(
    val fromRegionId: String,
    val toRegionId: String,
    val latitude: Double,
    val longitude: Double,
    val alertsDelivered: Int
)

data class CrossingResponse(
    val id: String,
    val fromRegionId: String,
    val toRegionId: String,
    val alertsDelivered: Int,
    val timestamp: String
)

data class CrossingsListResponse(
    val crossings: List<CrossingItemDto>,
    val total: Int
)

data class CrossingItemDto(
    val id: String,
    val fromRegion: CrossingRegionDto,
    val toRegion: CrossingRegionDto,
    val alertsDelivered: Int,
    val timestamp: String
)

data class CrossingRegionDto(
    val id: String,
    val name: String
)
