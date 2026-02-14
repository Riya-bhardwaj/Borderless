package com.borderless.app.data.repository

import com.borderless.app.data.local.CrossingHistoryDao
import com.borderless.app.data.local.CrossingHistoryEntity
import com.borderless.app.data.remote.BorderlessApi
import com.borderless.app.data.remote.dto.CrossingRequest
import com.borderless.app.domain.model.CrossingEvent
import com.borderless.app.domain.repository.CrossingRepository
import com.borderless.app.domain.repository.UserRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class CrossingRepositoryImpl @Inject constructor(
    private val api: BorderlessApi,
    private val crossingHistoryDao: CrossingHistoryDao,
    private val userRepository: UserRepository
) : CrossingRepository {

    override suspend fun logCrossing(
        fromRegionId: String,
        fromRegionName: String,
        toRegionId: String,
        toRegionName: String,
        latitude: Double,
        longitude: Double,
        alertsDelivered: Int
    ): Result<Unit> = runCatching {
        val now = System.currentTimeMillis()

        // Save locally first
        crossingHistoryDao.insert(
            CrossingHistoryEntity(
                fromRegionId = fromRegionId,
                fromRegionName = fromRegionName,
                toRegionId = toRegionId,
                toRegionName = toRegionName,
                latitude = latitude,
                longitude = longitude,
                alertCount = alertsDelivered,
                timestamp = now
            )
        )

        // Then sync to remote
        val token = userRepository.getAuthToken()
        if (token != null) {
            api.logCrossing(
                authToken = "Bearer $token",
                request = CrossingRequest(
                    fromRegionId = fromRegionId,
                    toRegionId = toRegionId,
                    latitude = latitude,
                    longitude = longitude,
                    alertsDelivered = alertsDelivered
                )
            )
        }
    }

    override fun observeRecentCrossings(limit: Int): Flow<List<CrossingEvent>> {
        return crossingHistoryDao.getRecentCrossings(limit).map { entities ->
            entities.map { it.toDomainModel() }
        }
    }

    override suspend fun getRemoteCrossings(limit: Int): Result<List<CrossingEvent>> = runCatching {
        val token = userRepository.getAuthToken() ?: throw IllegalStateException("Not authenticated")
        val response = api.getCrossings("Bearer $token", limit)
        response.crossings.map { dto ->
            CrossingEvent(
                id = dto.id,
                fromRegionId = dto.fromRegion.id,
                fromRegionName = dto.fromRegion.name,
                toRegionId = dto.toRegion.id,
                toRegionName = dto.toRegion.name,
                latitude = 0.0,
                longitude = 0.0,
                alertsDelivered = dto.alertsDelivered,
                timestamp = dto.timestamp
            )
        }
    }
}
