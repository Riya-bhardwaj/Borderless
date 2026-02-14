package com.borderless.app.data.repository

import com.borderless.app.domain.model.GeofenceDefinition
import com.borderless.app.domain.model.Region
import com.borderless.app.domain.model.RegionType
import com.borderless.app.domain.repository.RegionRepository
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.tasks.await
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class RegionRepositoryImpl @Inject constructor(
    private val firestore: FirebaseFirestore
) : RegionRepository {

    private val cachedRegions = MutableStateFlow<List<Region>>(emptyList())

    override suspend fun getRegions(): Result<List<Region>> = runCatching {
        val snapshot = firestore.collection("regions")
            .whereEqualTo("active", true)
            .get()
            .await()

        val regions = snapshot.documents.mapNotNull { doc ->
            val data = doc.data ?: return@mapNotNull null

            @Suppress("UNCHECKED_CAST")
            val geofencesList = (data["geofences"] as? List<Map<String, Any>>)?.mapNotNull { gf ->
                GeofenceDefinition(
                    lat = (gf["lat"] as? Number)?.toDouble() ?: return@mapNotNull null,
                    lng = (gf["lng"] as? Number)?.toDouble() ?: return@mapNotNull null,
                    radiusMeters = (gf["radiusMeters"] as? Number)?.toFloat() ?: 5000f,
                    label = gf["label"] as? String ?: ""
                )
            } ?: emptyList()

            @Suppress("UNCHECKED_CAST")
            val quickFacts = (data["quickFacts"] as? List<String>) ?: emptyList()

            Region(
                id = doc.id,
                name = data["name"] as? String ?: doc.id,
                type = RegionType.fromString(data["type"] as? String ?: "state"),
                parentId = data["parentId"] as? String,
                geofences = geofencesList,
                quickFacts = quickFacts,
                alertCount = 0,
                active = true
            )
        }

        cachedRegions.value = regions
        regions
    }

    override fun observeRegions(): Flow<List<Region>> = cachedRegions.asStateFlow()

    override suspend fun refreshRegions(): Result<Unit> = runCatching {
        getRegions().getOrThrow()
        Unit
    }
}
