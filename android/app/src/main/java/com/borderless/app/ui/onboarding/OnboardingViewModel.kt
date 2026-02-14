package com.borderless.app.ui.onboarding

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.borderless.app.domain.repository.UserRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class OnboardingUiState(
    val displayName: String = "",
    val language: String = "en",
    val criticalFilter: Boolean = true,
    val importantFilter: Boolean = true,
    val informationalFilter: Boolean = true,
    val isLoading: Boolean = false,
    val isComplete: Boolean = false,
    val error: String? = null
)

@HiltViewModel
class OnboardingViewModel @Inject constructor(
    private val userRepository: UserRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(OnboardingUiState())
    val uiState: StateFlow<OnboardingUiState> = _uiState.asStateFlow()

    fun updateDisplayName(name: String) {
        _uiState.update { it.copy(displayName = name, error = null) }
    }

    fun updateLanguage(language: String) {
        _uiState.update { it.copy(language = language) }
    }

    fun toggleCriticalFilter() {
        _uiState.update { it.copy(criticalFilter = !it.criticalFilter) }
    }

    fun toggleImportantFilter() {
        _uiState.update { it.copy(importantFilter = !it.importantFilter) }
    }

    fun toggleInformationalFilter() {
        _uiState.update { it.copy(informationalFilter = !it.informationalFilter) }
    }

    fun signUp() {
        val state = _uiState.value

        if (state.displayName.isBlank()) {
            _uiState.update { it.copy(error = "Please enter your name") }
            return
        }

        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }

            userRepository.createOrUpdateProfile(
                displayName = state.displayName.trim(),
                language = state.language,
                criticalFilter = state.criticalFilter,
                importantFilter = state.importantFilter,
                informationalFilter = state.informationalFilter
            ).onSuccess {
                _uiState.update { it.copy(isLoading = false, isComplete = true) }
            }.onFailure { error ->
                _uiState.update {
                    it.copy(
                        isLoading = false,
                        error = error.message ?: "Sign up failed. Please try again."
                    )
                }
            }
        }
    }

    fun signInAnonymously() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            // Firebase anonymous auth happens at app level
            // Here we just create a minimal profile
            val state = _uiState.value
            val name = state.displayName.ifBlank { "Traveler" }

            userRepository.createOrUpdateProfile(
                displayName = name,
                language = state.language,
                criticalFilter = true,
                importantFilter = true,
                informationalFilter = true
            ).onSuccess {
                _uiState.update { it.copy(isLoading = false, isComplete = true) }
            }.onFailure { error ->
                _uiState.update {
                    it.copy(
                        isLoading = false,
                        error = error.message ?: "Failed to create profile"
                    )
                }
            }
        }
    }
}
