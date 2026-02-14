package com.borderless.app.ui.qa

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.borderless.app.domain.model.QaInteraction
import com.borderless.app.domain.model.RiskRating
import com.borderless.app.domain.repository.RegionRepository
import com.borderless.app.domain.repository.UserRepository
import com.borderless.app.domain.usecase.AskQuestionUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class QaUiState(
    val question: String = "",
    val isLoading: Boolean = false,
    val currentAnswer: QaInteraction? = null,
    val error: String? = null,
    val currentRegionId: String? = null,
    val currentRegionName: String? = null,
    val language: String = "en",
    val history: List<QaHistoryItem> = emptyList()
)

data class QaHistoryItem(
    val question: String,
    val answer: QaInteraction
)

@HiltViewModel
class QaViewModel @Inject constructor(
    private val askQuestionUseCase: AskQuestionUseCase,
    private val regionRepository: RegionRepository,
    private val userRepository: UserRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(QaUiState())
    val uiState: StateFlow<QaUiState> = _uiState.asStateFlow()

    init {
        loadContext()
    }

    private fun loadContext() {
        viewModelScope.launch {
            val user = userRepository.getCurrentUser()
            val regions = regionRepository.getRegions()

            val firstRegion = regions.getOrNull()?.firstOrNull()
            _uiState.update {
                it.copy(
                    currentRegionId = firstRegion?.id,
                    currentRegionName = firstRegion?.name,
                    language = user?.language ?: "en"
                )
            }
        }
    }

    fun updateQuestion(question: String) {
        _uiState.update { it.copy(question = question, error = null) }
    }

    fun selectRegion(regionId: String, regionName: String) {
        _uiState.update {
            it.copy(currentRegionId = regionId, currentRegionName = regionName)
        }
    }

    fun askQuestion() {
        val state = _uiState.value
        val regionId = state.currentRegionId ?: return
        val question = state.question.trim()

        if (question.isBlank()) {
            _uiState.update { it.copy(error = "Please enter a question") }
            return
        }

        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null, currentAnswer = null) }

            askQuestionUseCase(regionId, question, state.language)
                .onSuccess { answer ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            currentAnswer = answer,
                            question = "",
                            history = it.history + QaHistoryItem(question, answer)
                        )
                    }
                }
                .onFailure { error ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            error = error.message ?: "Failed to get answer. Please try again."
                        )
                    }
                }
        }
    }

    fun clearError() {
        _uiState.update { it.copy(error = null) }
    }
}
