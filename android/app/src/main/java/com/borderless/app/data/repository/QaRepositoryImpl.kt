package com.borderless.app.data.repository

import com.borderless.app.data.remote.BorderlessApi
import com.borderless.app.data.remote.dto.QaRequest
import com.borderless.app.domain.model.QaInteraction
import com.borderless.app.domain.repository.QaRepository
import com.borderless.app.domain.repository.UserRepository
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class QaRepositoryImpl @Inject constructor(
    private val api: BorderlessApi,
    private val userRepository: UserRepository
) : QaRepository {

    override suspend fun askQuestion(
        regionId: String,
        question: String,
        language: String
    ): Result<QaInteraction> = runCatching {
        val token = userRepository.getAuthToken() ?: throw IllegalStateException("Not authenticated")
        val response = api.askQuestion(
            authToken = "Bearer $token",
            request = QaRequest(
                regionId = regionId,
                question = question,
                language = language
            )
        )
        response.toDomainModel()
    }
}
