package com.borderless.app.domain.repository

import com.borderless.app.domain.model.QaInteraction

interface QaRepository {
    suspend fun askQuestion(
        regionId: String,
        question: String,
        language: String = "en"
    ): Result<QaInteraction>
}
