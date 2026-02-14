package com.borderless.app.domain.repository

import com.borderless.app.domain.model.CrossingEvent
import kotlinx.coroutines.flow.Flow

interface CrossingRepository {
    suspend fun logCrossing(
        fromRegionId: String,
        fromRegionName: String,
        toRegionId: String,
        toRegionName: String,
        latitude: Double,
        longitude: Double,
        alertsDelivered: Int
    ): Result<Unit>

    fun observeRecentCrossings(limit: Int = 20): Flow<List<CrossingEvent>>
    suspend fun getRemoteCrossings(limit: Int = 20): Result<List<CrossingEvent>>
}
