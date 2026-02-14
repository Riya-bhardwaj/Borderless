package com.borderless.app.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface CrossingHistoryDao {
    @Insert
    suspend fun insert(crossing: CrossingHistoryEntity): Long

    @Query("SELECT * FROM crossing_history ORDER BY timestamp DESC LIMIT :limit")
    fun getRecentCrossings(limit: Int = 20): Flow<List<CrossingHistoryEntity>>

    @Query("SELECT COUNT(*) FROM crossing_history")
    suspend fun getCount(): Int

    @Query("DELETE FROM crossing_history")
    suspend fun deleteAll()
}
