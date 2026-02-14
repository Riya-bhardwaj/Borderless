package com.borderless.app.data.remote.dto

import com.borderless.app.domain.model.AlertCategory
import com.borderless.app.domain.model.AlertEntry
import com.borderless.app.domain.model.AlertSeverity

data class AlertsResponse(
    val regionId: String,
    val regionName: String,
    val alerts: List<AlertDto>,
    val totalCount: Int,
    val language: String
)

data class AlertDto(
    val id: String,
    val category: String,
    val severity: String,
    val title: String,
    val description: String,
    val source: String,
    val tags: List<String>
) {
    fun toDomainModel(): AlertEntry = AlertEntry(
        id = id,
        category = AlertCategory.fromString(category),
        severity = AlertSeverity.fromString(severity),
        title = title,
        description = description,
        source = source,
        tags = tags
    )
}
