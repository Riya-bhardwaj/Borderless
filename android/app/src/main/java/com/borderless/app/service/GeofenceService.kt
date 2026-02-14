package com.borderless.app.service

import android.Manifest
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.IBinder
import androidx.core.app.ActivityCompat
import androidx.core.app.NotificationCompat
import com.borderless.app.R
import com.borderless.app.domain.model.GeofenceDefinition
import com.borderless.app.domain.repository.AlertRepository
import com.borderless.app.domain.repository.CrossingRepository
import com.borderless.app.domain.repository.RegionRepository
import com.google.android.gms.location.Geofence
import com.google.android.gms.location.GeofencingClient
import com.google.android.gms.location.GeofencingRequest
import com.google.android.gms.location.LocationServices
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel
import kotlinx.coroutines.launch
import javax.inject.Inject

@AndroidEntryPoint
class GeofenceService : Service() {

    @Inject lateinit var regionRepository: RegionRepository
    @Inject lateinit var alertRepository: AlertRepository
    @Inject lateinit var crossingRepository: CrossingRepository
    @Inject lateinit var notificationHelper: NotificationHelper

    private lateinit var geofencingClient: GeofencingClient
    private val serviceScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private var currentRegionId: String? = null

    override fun onCreate() {
        super.onCreate()
        geofencingClient = LocationServices.getGeofencingClient(this)
        createNotificationChannel()
        startForeground(FOREGROUND_NOTIFICATION_ID, createForegroundNotification())
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_START_MONITORING -> {
                serviceScope.launch { registerGeofences() }
            }
            ACTION_GEOFENCE_ENTER -> {
                val regionId = intent.getStringExtra(EXTRA_REGION_ID) ?: return START_STICKY
                val lat = intent.getDoubleExtra(EXTRA_LATITUDE, 0.0)
                val lng = intent.getDoubleExtra(EXTRA_LONGITUDE, 0.0)
                serviceScope.launch { handleGeofenceEnter(regionId, lat, lng) }
            }
        }
        return START_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        serviceScope.cancel()
        super.onDestroy()
    }

    private suspend fun registerGeofences() {
        val regionsResult = regionRepository.getRegions()
        val regions = regionsResult.getOrNull() ?: return

        val geofences = mutableListOf<Geofence>()

        for (region in regions) {
            for (geofenceDef in region.geofences) {
                geofences.add(createGeofence(region.id, geofenceDef))
            }
        }

        if (geofences.isEmpty()) return

        val geofencingRequest = GeofencingRequest.Builder()
            .setInitialTrigger(GeofencingRequest.INITIAL_TRIGGER_ENTER)
            .addGeofences(geofences)
            .build()

        val pendingIntent = getGeofencePendingIntent()

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
            != PackageManager.PERMISSION_GRANTED
        ) {
            return
        }

        geofencingClient.addGeofences(geofencingRequest, pendingIntent)
    }

    private fun createGeofence(regionId: String, def: GeofenceDefinition): Geofence {
        return Geofence.Builder()
            .setRequestId(regionId)
            .setCircularRegion(def.lat, def.lng, def.radiusMeters)
            .setExpirationDuration(Geofence.NEVER_EXPIRE)
            .setTransitionTypes(Geofence.GEOFENCE_TRANSITION_ENTER)
            .build()
    }

    private fun getGeofencePendingIntent(): PendingIntent {
        val intent = Intent(this, GeofenceBroadcastReceiver::class.java)
        return PendingIntent.getBroadcast(
            this,
            0,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_MUTABLE
        )
    }

    private suspend fun handleGeofenceEnter(regionId: String, latitude: Double, longitude: Double) {
        // Check notification suppression
        if (notificationHelper.shouldSuppress(regionId)) return

        val previousRegionId = currentRegionId
        currentRegionId = regionId

        // Fetch alerts for the new region
        val alertsResult = alertRepository.getAlertsForRegion(regionId)
        val alerts = alertsResult.getOrNull() ?: return

        // Log crossing
        val regions = regionRepository.getRegions().getOrNull() ?: return
        val toRegion = regions.find { it.id == regionId }
        val fromRegion = if (previousRegionId != null) regions.find { it.id == previousRegionId } else null

        crossingRepository.logCrossing(
            fromRegionId = fromRegion?.id ?: "unknown",
            fromRegionName = fromRegion?.name ?: "Unknown",
            toRegionId = regionId,
            toRegionName = toRegion?.name ?: regionId,
            latitude = latitude,
            longitude = longitude,
            alertsDelivered = alerts.size
        )

        // Show notification
        val criticalCount = alerts.count { it.severity.sortOrder == 0 }
        notificationHelper.showBoundaryCrossingNotification(
            regionId = regionId,
            regionName = toRegion?.name ?: regionId,
            alertCount = alerts.size,
            criticalCount = criticalCount
        )
    }

    private fun createNotificationChannel() {
        val channel = NotificationChannel(
            CHANNEL_FOREGROUND,
            "Location Monitoring",
            NotificationManager.IMPORTANCE_LOW
        ).apply {
            description = "Monitors location for boundary crossings"
        }
        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        notificationManager.createNotificationChannel(channel)
    }

    private fun createForegroundNotification(): Notification {
        return NotificationCompat.Builder(this, CHANNEL_FOREGROUND)
            .setContentTitle("Borderless Active")
            .setContentText("Monitoring for boundary crossings")
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setOngoing(true)
            .build()
    }

    companion object {
        const val ACTION_START_MONITORING = "com.borderless.app.START_MONITORING"
        const val ACTION_GEOFENCE_ENTER = "com.borderless.app.GEOFENCE_ENTER"
        const val EXTRA_REGION_ID = "extra_region_id"
        const val EXTRA_LATITUDE = "extra_latitude"
        const val EXTRA_LONGITUDE = "extra_longitude"

        private const val FOREGROUND_NOTIFICATION_ID = 1001
        private const val CHANNEL_FOREGROUND = "borderless_foreground"

        fun startMonitoring(context: Context) {
            val intent = Intent(context, GeofenceService::class.java).apply {
                action = ACTION_START_MONITORING
            }
            context.startForegroundService(intent)
        }
    }
}
