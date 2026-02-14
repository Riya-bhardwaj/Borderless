package com.borderless.app.domain.repository

import com.borderless.app.domain.model.UserProfile

interface UserRepository {
    suspend fun signInAnonymously(): Result<Unit>

    suspend fun createOrUpdateProfile(
        displayName: String,
        language: String,
        criticalFilter: Boolean,
        importantFilter: Boolean,
        informationalFilter: Boolean
    ): Result<UserProfile>

    suspend fun getCurrentUser(): UserProfile?
    suspend fun getAuthToken(): String?
    suspend fun isLoggedIn(): Boolean
}
