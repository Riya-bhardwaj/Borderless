package com.borderless.app.domain.usecase

import com.borderless.app.domain.model.QaInteraction
import com.borderless.app.domain.repository.QaRepository
import javax.inject.Inject

class AskQuestionUseCase @Inject constructor(
    private val qaRepository: QaRepository
) {
    suspend operator fun invoke(
        regionId: String,
        question: String,
        language: String = "en"
    ): Result<QaInteraction> {
        if (question.isBlank()) {
            return Result.failure(IllegalArgumentException("Question cannot be empty"))
        }
        if (question.length > 500) {
            return Result.failure(IllegalArgumentException("Question must be 500 characters or less"))
        }
        return qaRepository.askQuestion(regionId, question, language)
    }
}
