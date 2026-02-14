package com.borderless.app.data.repository

import com.borderless.app.data.remote.BorderlessApi
import com.borderless.app.domain.model.Region
import com.borderless.app.domain.repository.RegionRepository
import com.borderless.app.domain.repository.UserRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class RegionRepositoryImpl @Inject constructor(
    private val api: BorderlessApi,
    private val userRepository: UserRepository
) : RegionRepository {

    private val cachedRegions = MutableStateFlow<List<Region>>(emptyList())

    override suspend fun getRegions(): Result<List<Region>> = runCatching {
        val token = userRepository.getAuthToken() ?: throw IllegalStateException("Not authenticated")
        val response = api.getRegions("Bearer $token")
        val regions = response.regions.map { it.toDomainModel() }
        cachedRegions.value = regions
        regions
    }

    override fun observeRegions(): Flow<List<Region>> = cachedRegions.asStateFlow()

    override suspend fun refreshRegions(): Result<Unit> = runCatching {
        getRegions().getOrThrow()
        Unit
    }
}
