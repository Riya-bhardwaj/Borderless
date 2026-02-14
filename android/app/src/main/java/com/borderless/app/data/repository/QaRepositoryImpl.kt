package com.borderless.app.data.repository

import com.borderless.app.domain.model.QaInteraction
import com.borderless.app.domain.repository.AlertRepository
import com.borderless.app.domain.repository.QaRepository
import com.borderless.app.domain.repository.RegionRepository
import com.borderless.app.domain.repository.UserRepository
import com.borderless.app.service.GeminiService
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class QaRepositoryImpl @Inject constructor(
    private val geminiService: GeminiService,
    private val regionRepository: RegionRepository,
    private val alertRepository: AlertRepository,
    private val userRepository: UserRepository
) : QaRepository {

    override suspend fun askQuestion(
        regionId: String,
        question: String,
        language: String
    ): Result<QaInteraction> = runCatching {
        // Fetch region with metadata (quickFacts, type, etc.)
        val regions = regionRepository.getRegions().getOrThrow()
        val region = regions.find { it.id == regionId }
            ?: throw IllegalArgumentException("Region not found: $regionId")

        // Fetch alerts for grounding context
        val alerts = alertRepository.getAlertsForRegion(regionId, language).getOrThrow()

        // Get user profile for personalization
        val userProfile = userRepository.getCurrentUser()

        // Call Gemini directly with all context
        geminiService.askQuestion(
            question = question,
            region = region,
            alerts = alerts,
            language = language,
            userDisplayName = userProfile?.displayName
        ).getOrThrow()
    }
}
