package com.borderless.app.ui.settings

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.borderless.app.domain.model.AlertFilters
import com.borderless.app.domain.model.UserProfile
import com.borderless.app.domain.repository.UserRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class SettingsUiState(
    val language: String = "en",
    val alertFilters: AlertFilters = AlertFilters(),
    val isSaving: Boolean = false,
    val userProfile: UserProfile? = null
)

@HiltViewModel
class SettingsViewModel @Inject constructor(
    private val userRepository: UserRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(SettingsUiState())
    val uiState: StateFlow<SettingsUiState> = _uiState.asStateFlow()

    init {
        loadSettings()
    }

    private fun loadSettings() {
        viewModelScope.launch {
            val user = userRepository.getCurrentUser()
            if (user != null) {
                _uiState.update {
                    it.copy(
                        language = user.language,
                        alertFilters = user.alertFilters,
                        userProfile = user
                    )
                }
            }
        }
    }

    fun setLanguage(language: String) {
        _uiState.update { it.copy(language = language) }
        saveSettings()
    }

    fun toggleCriticalFilter() {
        _uiState.update {
            it.copy(alertFilters = it.alertFilters.copy(critical = !it.alertFilters.critical))
        }
        saveSettings()
    }

    fun toggleImportantFilter() {
        _uiState.update {
            it.copy(alertFilters = it.alertFilters.copy(important = !it.alertFilters.important))
        }
        saveSettings()
    }

    fun toggleInformationalFilter() {
        _uiState.update {
            it.copy(alertFilters = it.alertFilters.copy(informational = !it.alertFilters.informational))
        }
        saveSettings()
    }

    private fun saveSettings() {
        viewModelScope.launch {
            _uiState.update { it.copy(isSaving = true) }
            val state = _uiState.value
            val user = state.userProfile ?: return@launch

            userRepository.createOrUpdateProfile(
                displayName = user.displayName,
                language = state.language,
                criticalFilter = state.alertFilters.critical,
                importantFilter = state.alertFilters.important,
                informationalFilter = state.alertFilters.informational
            )
            _uiState.update { it.copy(isSaving = false) }
        }
    }

    companion object {
        val SUPPORTED_LANGUAGES = listOf(
            "en" to "English",
            "hi" to "Hindi",
            "kn" to "Kannada",
            "ta" to "Tamil",
            "mr" to "Marathi"
        )
    }
}
