package com.borderless.app.service

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import com.google.android.gms.location.Geofence
import com.google.android.gms.location.GeofencingEvent

class GeofenceBroadcastReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {
        val geofencingEvent = GeofencingEvent.fromIntent(intent) ?: return

        if (geofencingEvent.hasError()) {
            return
        }

        val geofenceTransition = geofencingEvent.geofenceTransition

        if (geofenceTransition == Geofence.GEOFENCE_TRANSITION_ENTER) {
            val triggeringGeofences = geofencingEvent.triggeringGeofences ?: return
            val location = geofencingEvent.triggeringLocation

            for (geofence in triggeringGeofences) {
                val regionId = geofence.requestId

                // Forward to GeofenceService for processing
                val serviceIntent = Intent(context, GeofenceService::class.java).apply {
                    action = GeofenceService.ACTION_GEOFENCE_ENTER
                    putExtra(GeofenceService.EXTRA_REGION_ID, regionId)
                    putExtra(GeofenceService.EXTRA_LATITUDE, location?.latitude ?: 0.0)
                    putExtra(GeofenceService.EXTRA_LONGITUDE, location?.longitude ?: 0.0)
                }
                context.startForegroundService(serviceIntent)
            }
        }
    }
}
