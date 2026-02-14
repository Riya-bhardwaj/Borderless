package com.borderless.app.data.repository

import com.borderless.app.data.remote.BorderlessApi
import com.borderless.app.domain.model.AlertEntry
import com.borderless.app.domain.repository.AlertRepository
import com.borderless.app.domain.repository.UserRepository
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AlertRepositoryImpl @Inject constructor(
    private val api: BorderlessApi,
    private val userRepository: UserRepository
) : AlertRepository {

    override suspend fun getAlertsForRegion(
        regionId: String,
        language: String,
        severity: String?
    ): Result<List<AlertEntry>> = runCatching {
        val token = userRepository.getAuthToken() ?: throw IllegalStateException("Not authenticated")
        val response = api.getAlerts(
            authToken = "Bearer $token",
            regionId = regionId,
            language = language.takeIf { it != "en" },
            severity = severity
        )
        response.alerts.map { it.toDomainModel() }
    }
}
