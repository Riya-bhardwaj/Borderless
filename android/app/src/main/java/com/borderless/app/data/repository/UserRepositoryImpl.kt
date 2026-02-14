package com.borderless.app.data.repository

import com.borderless.app.data.remote.BorderlessApi
import com.borderless.app.data.remote.dto.AlertFiltersDto
import com.borderless.app.data.remote.dto.UserProfileRequest
import com.borderless.app.domain.model.UserProfile
import com.borderless.app.domain.repository.UserRepository
import com.google.firebase.auth.FirebaseAuth
import kotlinx.coroutines.tasks.await
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class UserRepositoryImpl @Inject constructor(
    private val api: BorderlessApi,
    private val firebaseAuth: FirebaseAuth
) : UserRepository {

    private var cachedProfile: UserProfile? = null

    override suspend fun signInAnonymously(): Result<Unit> = runCatching {
        if (firebaseAuth.currentUser == null) {
            firebaseAuth.signInAnonymously().await()
        }
    }

    override suspend fun createOrUpdateProfile(
        displayName: String,
        language: String,
        criticalFilter: Boolean,
        importantFilter: Boolean,
        informationalFilter: Boolean
    ): Result<UserProfile> = runCatching {
        // Ensure we're authenticated first
        if (firebaseAuth.currentUser == null) {
            firebaseAuth.signInAnonymously().await()
        }

        val token = getAuthToken() ?: throw IllegalStateException("Not authenticated")
        val response = api.createOrUpdateProfile(
            authToken = "Bearer $token",
            request = UserProfileRequest(
                displayName = displayName,
                language = language,
                alertFilters = AlertFiltersDto(
                    critical = criticalFilter,
                    important = importantFilter,
                    informational = informationalFilter
                )
            )
        )
        val profile = response.toDomainModel()
        cachedProfile = profile
        profile
    }

    override suspend fun getCurrentUser(): UserProfile? = cachedProfile

    override suspend fun getAuthToken(): String? {
        return firebaseAuth.currentUser?.getIdToken(false)?.await()?.token
    }

    override suspend fun isLoggedIn(): Boolean {
        return firebaseAuth.currentUser != null
    }
}
