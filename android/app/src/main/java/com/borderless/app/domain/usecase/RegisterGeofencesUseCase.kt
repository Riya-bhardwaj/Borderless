package com.borderless.app.domain.usecase

import android.content.Context
import com.borderless.app.domain.repository.RegionRepository
import com.borderless.app.service.GeofenceService
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject

class RegisterGeofencesUseCase @Inject constructor(
    private val regionRepository: RegionRepository,
    @ApplicationContext private val context: Context
) {
    suspend operator fun invoke(): Result<Unit> {
        return regionRepository.getRegions().map { regions ->
            if (regions.isNotEmpty()) {
                GeofenceService.startMonitoring(context)
            }
        }
    }
}
