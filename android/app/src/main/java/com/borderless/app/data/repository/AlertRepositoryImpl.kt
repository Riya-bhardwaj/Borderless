package com.borderless.app.data.repository

import com.borderless.app.domain.model.AlertCategory
import com.borderless.app.domain.model.AlertEntry
import com.borderless.app.domain.model.AlertSeverity
import com.borderless.app.domain.repository.AlertRepository
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.tasks.await
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AlertRepositoryImpl @Inject constructor(
    private val firestore: FirebaseFirestore
) : AlertRepository {

    override suspend fun getAlertsForRegion(
        regionId: String,
        language: String,
        severity: String?
    ): Result<List<AlertEntry>> = runCatching {
        var query = firestore.collection("regions")
            .document(regionId)
            .collection("alerts")
            .whereEqualTo("active", true)

        if (severity != null) {
            query = query.whereEqualTo("severity", severity)
        }

        val snapshot = query.get().await()

        val alerts = snapshot.documents.mapNotNull { doc ->
            val data = doc.data ?: return@mapNotNull null

            @Suppress("UNCHECKED_CAST")
            val tags = (data["tags"] as? List<String>) ?: emptyList()

            AlertEntry(
                id = doc.id,
                category = AlertCategory.fromString(data["category"] as? String ?: "behavioral"),
                severity = AlertSeverity.fromString(data["severity"] as? String ?: "informational"),
                title = data["title"] as? String ?: "",
                description = data["description"] as? String ?: "",
                source = data["source"] as? String ?: "",
                tags = tags
            )
        }.sortedBy { it.severity.sortOrder }

        alerts
    }
}
