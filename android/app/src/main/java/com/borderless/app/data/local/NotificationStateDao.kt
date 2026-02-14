package com.borderless.app.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

@Dao
interface NotificationStateDao {
    @Query("SELECT * FROM notification_state WHERE region_id = :regionId")
    suspend fun getByRegionId(regionId: String): NotificationStateEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(state: NotificationStateEntity)

    @Query("UPDATE notification_state SET notification_count = 0 WHERE last_notified_at < :cutoffTime")
    suspend fun resetExpiredSuppressions(cutoffTime: Long)

    @Query("DELETE FROM notification_state")
    suspend fun deleteAll()
}
