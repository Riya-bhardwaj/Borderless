package com.borderless.app.domain.repository

import com.borderless.app.domain.model.Region
import kotlinx.coroutines.flow.Flow

interface RegionRepository {
    suspend fun getRegions(): Result<List<Region>>
    fun observeRegions(): Flow<List<Region>>
    suspend fun refreshRegions(): Result<Unit>
}
