package com.borderless.app.ui.alerts

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.borderless.app.domain.model.AlertCategory
import com.borderless.app.domain.model.AlertEntry
import com.borderless.app.domain.usecase.GetAlertsForRegionUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class AlertDetailUiState(
    val regionName: String = "",
    val alerts: List<AlertEntry> = emptyList(),
    val isLoading: Boolean = true,
    val error: String? = null,
    val selectedCategory: AlertCategory? = null,
    val showAll: Boolean = false
) {
    val filteredAlerts: List<AlertEntry>
        get() {
            val categoryFiltered = if (selectedCategory != null) {
                alerts.filter { it.category == selectedCategory }
            } else {
                alerts
            }
            return if (showAll) categoryFiltered else categoryFiltered.take(5)
        }

    val legalCount: Int get() = alerts.count { it.category == AlertCategory.LEGAL }
    val culturalCount: Int get() = alerts.count { it.category == AlertCategory.CULTURAL }
    val behavioralCount: Int get() = alerts.count { it.category == AlertCategory.BEHAVIORAL }
}

@HiltViewModel
class AlertDetailViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val getAlertsForRegionUseCase: GetAlertsForRegionUseCase
) : ViewModel() {

    private val regionId: String = savedStateHandle["regionId"] ?: ""
    private val initialCategory: AlertCategory? = savedStateHandle.get<String>("category")?.let {
        try { AlertCategory.fromString(it) } catch (_: Exception) { null }
    }

    private val _uiState = MutableStateFlow(AlertDetailUiState(selectedCategory = initialCategory))
    val uiState: StateFlow<AlertDetailUiState> = _uiState.asStateFlow()

    init {
        loadAlerts()
    }

    fun loadAlerts() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }

            getAlertsForRegionUseCase(regionId).fold(
                onSuccess = { alerts ->
                    _uiState.update {
                        it.copy(
                            alerts = alerts,
                            isLoading = false,
                            error = null
                        )
                    }
                },
                onFailure = { error ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            error = error.message ?: "Failed to load alerts"
                        )
                    }
                }
            )
        }
    }

    fun selectCategory(category: AlertCategory?) {
        _uiState.update { it.copy(selectedCategory = category) }
    }

    fun toggleShowAll() {
        _uiState.update { it.copy(showAll = !it.showAll) }
    }
}
