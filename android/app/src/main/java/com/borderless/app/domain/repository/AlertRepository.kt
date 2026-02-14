package com.borderless.app.domain.repository

import com.borderless.app.domain.model.AlertEntry

interface AlertRepository {
    suspend fun getAlertsForRegion(
        regionId: String,
        language: String = "en",
        severity: String? = null
    ): Result<List<AlertEntry>>
}
