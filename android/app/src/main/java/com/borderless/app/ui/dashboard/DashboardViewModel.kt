package com.borderless.app.ui.dashboard

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.borderless.app.domain.model.AlertCategory
import com.borderless.app.domain.model.AlertEntry
import com.borderless.app.domain.model.AlertSeverity
import com.borderless.app.domain.model.CrossingEvent
import com.borderless.app.domain.model.Region
import com.borderless.app.domain.repository.AlertRepository
import com.borderless.app.domain.repository.CrossingRepository
import com.borderless.app.domain.repository.RegionRepository
import com.borderless.app.domain.repository.UserRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class DashboardUiState(
    val currentRegion: Region? = null,
    val regions: List<Region> = emptyList(),
    val alerts: List<AlertEntry> = emptyList(),
    val recentCrossings: List<CrossingEvent> = emptyList(),
    val isLoading: Boolean = true,
    val error: String? = null,
    val language: String = "en"
) {
    val legalCount: Int get() = alerts.count { it.category == AlertCategory.LEGAL }
    val culturalCount: Int get() = alerts.count { it.category == AlertCategory.CULTURAL }
    val behavioralCount: Int get() = alerts.count { it.category == AlertCategory.BEHAVIORAL }
    val totalAlertCount: Int get() = alerts.size

    val topLegalAlert: AlertEntry? get() = alerts.firstOrNull { it.category == AlertCategory.LEGAL }
    val topCulturalAlert: AlertEntry? get() = alerts.firstOrNull { it.category == AlertCategory.CULTURAL }
    val topBehavioralAlert: AlertEntry? get() = alerts.firstOrNull { it.category == AlertCategory.BEHAVIORAL }

    val highlights: List<AlertEntry> get() {
        val bySeverity = alerts.groupBy { it.severity }
        val picked = mutableListOf<AlertEntry>()
        val severities = listOf(AlertSeverity.CRITICAL, AlertSeverity.IMPORTANT, AlertSeverity.INFORMATIONAL)
        // Round-robin across severities to get a balanced mix
        var round = 0
        while (picked.size < 5) {
            var added = false
            for (sev in severities) {
                val pool = bySeverity[sev] ?: continue
                if (round < pool.size && picked.size < 5) {
                    picked.add(pool[round])
                    added = true
                }
            }
            if (!added) break
            round++
        }
        return picked
    }
}

@HiltViewModel
class DashboardViewModel @Inject constructor(
    private val regionRepository: RegionRepository,
    private val alertRepository: AlertRepository,
    private val crossingRepository: CrossingRepository,
    private val userRepository: UserRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(DashboardUiState())
    val uiState: StateFlow<DashboardUiState> = _uiState.asStateFlow()

    init {
        loadDashboard()
        observeCrossings()
    }

    fun loadDashboard() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }

            // Ensure user is authenticated before reading Firestore
            if (!userRepository.isLoggedIn()) {
                userRepository.signInAnonymously()
            }

            val user = userRepository.getCurrentUser()
            val language = user?.language ?: "en"

            regionRepository.getRegions().fold(
                onSuccess = { regions ->
                    val currentRegion = if (user?.currentRegionId != null) {
                        regions.find { it.id == user.currentRegionId }
                    } else {
                        regions.firstOrNull { it.type == com.borderless.app.domain.model.RegionType.STATE }
                    }

                    _uiState.update {
                        it.copy(
                            regions = regions,
                            currentRegion = currentRegion,
                            language = language,
                            isLoading = false
                        )
                    }

                    // Load alerts for current region
                    if (currentRegion != null) {
                        loadAlertsForRegion(currentRegion.id, language)
                    }
                },
                onFailure = {
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            error = "Unable to load regions. Make sure the backend is deployed and try again."
                        )
                    }
                }
            )
        }
    }

    fun selectRegion(region: Region) {
        _uiState.update { it.copy(currentRegion = region) }
        viewModelScope.launch {
            loadAlertsForRegion(region.id, _uiState.value.language)
        }
    }

    fun setLanguage(language: String) {
        _uiState.update { it.copy(language = language) }
        val currentRegion = _uiState.value.currentRegion
        if (currentRegion != null) {
            viewModelScope.launch {
                loadAlertsForRegion(currentRegion.id, language)
            }
        }
    }

    private suspend fun loadAlertsForRegion(regionId: String, language: String) {
        alertRepository.getAlertsForRegion(regionId, language).fold(
            onSuccess = { alerts ->
                _uiState.update { it.copy(alerts = alerts) }
            },
            onFailure = { /* Keep existing alerts on failure */ }
        )
    }

    private fun observeCrossings() {
        viewModelScope.launch {
            crossingRepository.observeRecentCrossings(5).collect { crossings ->
                _uiState.update { it.copy(recentCrossings = crossings) }
            }
        }
    }
}
