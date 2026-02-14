package com.borderless.app.data.local

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey
import com.borderless.app.domain.model.CrossingEvent

@Entity(tableName = "crossing_history")
data class CrossingHistoryEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,

    @ColumnInfo(name = "from_region_id")
    val fromRegionId: String,

    @ColumnInfo(name = "from_region_name")
    val fromRegionName: String,

    @ColumnInfo(name = "to_region_id")
    val toRegionId: String,

    @ColumnInfo(name = "to_region_name")
    val toRegionName: String,

    val latitude: Double,
    val longitude: Double,

    @ColumnInfo(name = "alert_count")
    val alertCount: Int,

    val timestamp: Long
) {
    fun toDomainModel(): CrossingEvent = CrossingEvent(
        id = id.toString(),
        fromRegionId = fromRegionId,
        fromRegionName = fromRegionName,
        toRegionId = toRegionId,
        toRegionName = toRegionName,
        latitude = latitude,
        longitude = longitude,
        alertsDelivered = alertCount,
        timestamp = java.time.Instant.ofEpochMilli(timestamp).toString()
    )
}
