package com.borderless.app.service

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import androidx.core.app.NotificationCompat
import com.borderless.app.MainActivity
import com.borderless.app.R
import com.borderless.app.data.local.NotificationStateDao
import com.borderless.app.data.local.NotificationStateEntity
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class NotificationHelper @Inject constructor(
    @ApplicationContext private val context: Context,
    private val notificationStateDao: NotificationStateDao
) {
    init {
        createAlertNotificationChannel()
    }

    suspend fun shouldSuppress(regionId: String): Boolean {
        val state = notificationStateDao.getByRegionId(regionId) ?: return false
        return state.shouldSuppress()
    }

    suspend fun showBoundaryCrossingNotification(
        regionId: String,
        regionName: String,
        alertCount: Int,
        criticalCount: Int
    ) {
        // Update notification state
        val existingState = notificationStateDao.getByRegionId(regionId)
        val now = System.currentTimeMillis()
        val twentyFourHoursMs = 24 * 60 * 60 * 1000L

        val newCount = if (existingState != null && (now - existingState.lastNotifiedAt) < twentyFourHoursMs) {
            existingState.notificationCount + 1
        } else {
            1
        }

        notificationStateDao.upsert(
            NotificationStateEntity(
                regionId = regionId,
                lastNotifiedAt = now,
                notificationCount = newCount
            )
        )

        // Build notification
        val title = "Entering $regionName"
        val body = buildString {
            append("$alertCount alerts available")
            if (criticalCount > 0) {
                append(" ($criticalCount critical)")
            }
        }

        // Deep link to alert detail screen
        val intent = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
            putExtra("navigate_to", "alert_detail/$regionId")
        }

        val pendingIntent = PendingIntent.getActivity(
            context,
            regionId.hashCode(),
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val notification = NotificationCompat.Builder(context, CHANNEL_ALERTS)
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setContentTitle(title)
            .setContentText(body)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .setContentIntent(pendingIntent)
            .build()

        val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        notificationManager.notify(regionId.hashCode(), notification)
    }

    private fun createAlertNotificationChannel() {
        val channel = NotificationChannel(
            CHANNEL_ALERTS,
            "Boundary Alerts",
            NotificationManager.IMPORTANCE_HIGH
        ).apply {
            description = "Alerts when crossing state boundaries"
        }
        val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        notificationManager.createNotificationChannel(channel)
    }

    companion object {
        private const val CHANNEL_ALERTS = "borderless_alerts"
    }
}
