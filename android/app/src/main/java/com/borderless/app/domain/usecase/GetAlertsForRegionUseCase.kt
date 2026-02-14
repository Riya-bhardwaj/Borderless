package com.borderless.app.domain.usecase

import com.borderless.app.domain.model.AlertEntry
import com.borderless.app.domain.model.AlertFilters
import com.borderless.app.domain.repository.AlertRepository
import javax.inject.Inject

class GetAlertsForRegionUseCase @Inject constructor(
    private val alertRepository: AlertRepository
) {
    suspend operator fun invoke(
        regionId: String,
        language: String = "en",
        filters: AlertFilters = AlertFilters()
    ): Result<List<AlertEntry>> {
        return alertRepository.getAlertsForRegion(regionId, language).map { alerts ->
            alerts.filter { alert ->
                when (alert.severity) {
                    com.borderless.app.domain.model.AlertSeverity.CRITICAL -> filters.critical
                    com.borderless.app.domain.model.AlertSeverity.IMPORTANT -> filters.important
                    com.borderless.app.domain.model.AlertSeverity.INFORMATIONAL -> filters.informational
                }
            }.sortedBy { it.severity.sortOrder }
        }
    }
}
