package com.borderless.app.data.local

import androidx.room.Database
import androidx.room.RoomDatabase

@Database(
    entities = [
        CrossingHistoryEntity::class,
        NotificationStateEntity::class
    ],
    version = 1,
    exportSchema = false
)
abstract class BorderlessDatabase : RoomDatabase() {
    abstract fun crossingHistoryDao(): CrossingHistoryDao
    abstract fun notificationStateDao(): NotificationStateDao
}
