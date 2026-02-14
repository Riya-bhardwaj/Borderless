package com.borderless.app.domain.model

data class UserProfile(
    val uid: String,
    val displayName: String,
    val language: String = "en",
    val alertFilters: AlertFilters = AlertFilters(),
    val currentRegionId: String? = null,
    val createdAt: String? = null,
    val updatedAt: String? = null
)

data class AlertFilters(
    val critical: Boolean = true,
    val important: Boolean = true,
    val informational: Boolean = true
)
