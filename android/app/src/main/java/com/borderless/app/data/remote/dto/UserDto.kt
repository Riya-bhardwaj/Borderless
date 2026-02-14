package com.borderless.app.data.remote.dto

import com.borderless.app.domain.model.AlertFilters
import com.borderless.app.domain.model.UserProfile

data class UserProfileRequest(
    val displayName: String,
    val language: String = "en",
    val alertFilters: AlertFiltersDto? = null
)

data class UserProfileResponse(
    val uid: String,
    val displayName: String,
    val language: String,
    val alertFilters: AlertFiltersDto,
    val createdAt: String,
    val updatedAt: String
) {
    fun toDomainModel(): UserProfile = UserProfile(
        uid = uid,
        displayName = displayName,
        language = language,
        alertFilters = alertFilters.toDomainModel(),
        createdAt = createdAt,
        updatedAt = updatedAt
    )
}

data class AlertFiltersDto(
    val critical: Boolean = true,
    val important: Boolean = true,
    val informational: Boolean = true
) {
    fun toDomainModel(): AlertFilters = AlertFilters(
        critical = critical,
        important = important,
        informational = informational
    )
}
