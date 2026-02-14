package com.borderless.app.ui.dashboard

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.location.Location
import androidx.core.content.ContextCompat
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.borderless.app.domain.model.AlertCategory
import com.borderless.app.domain.model.AlertEntry
import com.borderless.app.domain.model.AlertSeverity
import com.borderless.app.domain.model.CrossingEvent
import com.borderless.app.domain.model.Region
import com.borderless.app.domain.model.RegionType
import com.borderless.app.domain.repository.AlertRepository
import com.borderless.app.domain.repository.CrossingRepository
import com.borderless.app.domain.repository.RegionRepository
import com.borderless.app.domain.repository.UserRepository
import com.borderless.app.service.NotificationHelper
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.Priority
import com.google.android.gms.tasks.CancellationTokenSource
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await
import android.util.Log
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

    val alertRegionId: String get() {
        val region = currentRegion ?: return ""
        return if (region.type == RegionType.CITY) region.parentId ?: region.id else region.id
    }

    val topLegalAlert: AlertEntry? get() = alerts.firstOrNull { it.category == AlertCategory.LEGAL }
    val topCulturalAlert: AlertEntry? get() = alerts.firstOrNull { it.category == AlertCategory.CULTURAL }
    val topBehavioralAlert: AlertEntry? get() = alerts.firstOrNull { it.category == AlertCategory.BEHAVIORAL }

    val highlights: List<AlertEntry> get() {
        val bySeverity = alerts.groupBy { it.severity }
        val picked = mutableListOf<AlertEntry>()
        val severities = listOf(AlertSeverity.CRITICAL, AlertSeverity.IMPORTANT, AlertSeverity.INFORMATIONAL)
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
    @ApplicationContext private val context: Context,
    private val regionRepository: RegionRepository,
    private val alertRepository: AlertRepository,
    private val crossingRepository: CrossingRepository,
    private val userRepository: UserRepository,
    private val locationClient: FusedLocationProviderClient,
    private val notificationHelper: NotificationHelper
) : ViewModel() {

    private val _uiState = MutableStateFlow(DashboardUiState())
    val uiState: StateFlow<DashboardUiState> = _uiState.asStateFlow()

    init {
        loadDashboard()
        observeCrossings()
        scheduleDemoNotifications()
    }

    private fun scheduleDemoNotifications() {
        viewModelScope.launch {
            // Simulate: user is in Bangalore, then travels

            delay(8_000) // 8 seconds after app open
            notificationHelper.showPushAlertNotification(
                title = "Welcome to Bangalore!",
                body = "19 local tips available — try the Masala Dosa at Vidyarthi Bhavan!",
                regionId = "karnataka",
                severity = "important"
            )

            delay(15_000) // 23 seconds
            notificationHelper.showPushAlertNotification(
                title = "Entering Maharashtra",
                body = "Plastic bags are strictly banned here. Fines up to ₹25,000. Carry a cloth bag.",
                regionId = "maharashtra",
                severity = "critical"
            )

            delay(12_000) // 35 seconds
            notificationHelper.showPushAlertNotification(
                title = "You're in Mumbai!",
                body = "17 tips & local info available. Don't miss the Vada Pav at Ashok Vada Pav, Dadar!",
                regionId = "maharashtra",
                severity = "informational"
            )

            delay(15_000) // 50 seconds
            notificationHelper.showPushAlertNotification(
                title = "Entering Delhi NCR",
                body = "Odd-Even vehicle rule is active. Check if your plate number is allowed today.",
                regionId = "delhi",
                severity = "critical"
            )

            delay(12_000) // 62 seconds
            notificationHelper.showPushAlertNotification(
                title = "Air Quality Alert — Delhi",
                body = "AQI is above 300. Wear an N95 mask outdoors and avoid morning walks.",
                regionId = "delhi",
                severity = "critical"
            )
        }
    }

    fun loadDashboard() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }

            if (!userRepository.isLoggedIn()) {
                userRepository.signInAnonymously()
            }

            val user = userRepository.getCurrentUser()
            val language = user?.language ?: "en"

            regionRepository.getRegions().fold(
                onSuccess = { regions ->
                    // Hardcode Bangalore for demo
                    val currentRegion = regions.firstOrNull { it.id == "bangalore" }
                        ?: regions.firstOrNull { it.type == RegionType.STATE }

                    _uiState.update {
                        it.copy(
                            regions = regions,
                            currentRegion = currentRegion,
                            language = language,
                            isLoading = false
                        )
                    }

                    if (currentRegion != null) {
                        // Alerts are stored under state, so use parentId for cities
                        val alertRegionId = if (currentRegion.type == RegionType.CITY) {
                            currentRegion.parentId ?: currentRegion.id
                        } else {
                            currentRegion.id
                        }
                        loadAlertsForRegion(alertRegionId, language)
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

    private suspend fun detectCurrentRegion(regions: List<Region>): Region? {
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION)
            != PackageManager.PERMISSION_GRANTED &&
            ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_COARSE_LOCATION)
            != PackageManager.PERMISSION_GRANTED
        ) {
            return null
        }

        val location = try {
            // Try current location first (most accurate), fall back to last location
            val currentLoc = locationClient.getCurrentLocation(
                Priority.PRIORITY_HIGH_ACCURACY,
                CancellationTokenSource().token
            ).await()
            Log.d("Borderless", "Current location: ${currentLoc?.latitude}, ${currentLoc?.longitude}")
            if (currentLoc != null) {
                currentLoc
            } else {
                val lastLoc = locationClient.lastLocation.await()
                Log.d("Borderless", "Last location: ${lastLoc?.latitude}, ${lastLoc?.longitude}")
                lastLoc
            }
        } catch (e: Exception) {
            Log.e("Borderless", "Failed to get location", e)
            null
        } ?: return null

        Log.d("Borderless", "Using location: ${location.latitude}, ${location.longitude}")

        // Log all regions and their geofences for debugging
        for (region in regions) {
            Log.d("Borderless", "Region: ${region.id}, geofences: ${region.geofences.size}")
            for (gf in region.geofences) {
                val results = FloatArray(1)
                Location.distanceBetween(location.latitude, location.longitude, gf.lat, gf.lng, results)
                Log.d("Borderless", "  ${gf.label}: center=(${gf.lat},${gf.lng}), radius=${gf.radiusMeters}m, distance=${results[0]}m, inside=${results[0] <= gf.radiusMeters}")
            }
        }

        // Find the region whose geofence contains this location
        val found = findRegionForLocation(location, regions)
        Log.d("Borderless", "Detected region: ${found?.id}")
        return found
    }

    private fun findRegionForLocation(location: Location, regions: List<Region>): Region? {
        var bestRegion: Region? = null
        var bestDistance = Float.MAX_VALUE

        for (region in regions) {
            for (geofence in region.geofences) {
                val results = FloatArray(1)
                Location.distanceBetween(
                    location.latitude, location.longitude,
                    geofence.lat, geofence.lng,
                    results
                )
                val distance = results[0]

                // User is inside this geofence
                if (distance <= geofence.radiusMeters && distance < bestDistance) {
                    bestDistance = distance
                    bestRegion = region
                }
            }
        }

        // If not inside any geofence, find the nearest region
        if (bestRegion == null) {
            var nearestDistance = Float.MAX_VALUE
            for (region in regions) {
                for (geofence in region.geofences) {
                    val results = FloatArray(1)
                    Location.distanceBetween(
                        location.latitude, location.longitude,
                        geofence.lat, geofence.lng,
                        results
                    )
                    if (results[0] < nearestDistance) {
                        nearestDistance = results[0]
                        bestRegion = region
                    }
                }
            }
        }

        return bestRegion
    }

    fun selectRegion(region: Region) {
        _uiState.update { it.copy(currentRegion = region) }
        viewModelScope.launch {
            val alertRegionId = if (region.type == RegionType.CITY) {
                region.parentId ?: region.id
            } else {
                region.id
            }
            loadAlertsForRegion(alertRegionId, _uiState.value.language)
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
