package com.borderless.app.data.local

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "notification_state")
data class NotificationStateEntity(
    @PrimaryKey
    @ColumnInfo(name = "region_id")
    val regionId: String,

    @ColumnInfo(name = "last_notified_at")
    val lastNotifiedAt: Long,

    @ColumnInfo(name = "notification_count")
    val notificationCount: Int
) {
    fun shouldSuppress(): Boolean {
        val twentyFourHoursMs = 24 * 60 * 60 * 1000L
        val now = System.currentTimeMillis()
        return notificationCount >= 2 && (now - lastNotifiedAt) < twentyFourHoursMs
    }
}
