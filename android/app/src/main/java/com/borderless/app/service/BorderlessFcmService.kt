package com.borderless.app.service

import android.util.Log
import com.borderless.app.domain.repository.UserRepository
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch
import javax.inject.Inject

@AndroidEntryPoint
class BorderlessFcmService : FirebaseMessagingService() {

    @Inject
    lateinit var notificationHelper: NotificationHelper

    @Inject
    lateinit var userRepository: UserRepository

    private val serviceScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    override fun onNewToken(token: String) {
        super.onNewToken(token)
        Log.d(TAG, "FCM token refreshed")

        serviceScope.launch {
            try {
                if (userRepository.isLoggedIn()) {
                    userRepository.registerDeviceToken(token)
                    Log.d(TAG, "FCM token registered with backend")
                }
            } catch (e: Exception) {
                Log.e(TAG, "Failed to register FCM token", e)
            }
        }
    }

    override fun onMessageReceived(message: RemoteMessage) {
        super.onMessageReceived(message)
        Log.d(TAG, "FCM message received: ${message.data}")

        val data = message.data
        val title = data["title"] ?: message.notification?.title ?: "New Alert"
        val body = data["body"] ?: message.notification?.body ?: "You have a new alert"
        val regionId = data["regionId"] ?: return
        val severity = data["severity"] ?: "informational"

        notificationHelper.showPushAlertNotification(
            title = title,
            body = body,
            regionId = regionId,
            severity = severity
        )
    }

    companion object {
        private const val TAG = "BorderlessFcm"
    }
}
