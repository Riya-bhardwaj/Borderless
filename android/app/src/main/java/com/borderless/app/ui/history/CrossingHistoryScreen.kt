package com.borderless.app.ui.history

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.borderless.app.domain.model.CrossingEvent
import com.borderless.app.ui.components.EmptyState

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CrossingHistoryScreen(
    viewModel: CrossingHistoryViewModel = hiltViewModel()
) {
    val crossings by viewModel.crossings.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Crossing History") })
        }
    ) { padding ->
        if (crossings.isEmpty()) {
            EmptyState(
                title = "No Crossings Yet",
                message = "Your boundary crossing history will appear here",
                modifier = Modifier.padding(padding)
            )
        } else {
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(crossings) { crossing ->
                    CrossingHistoryItem(crossing = crossing)
                }
            }
        }
    }
}

@Composable
private fun CrossingHistoryItem(crossing: CrossingEvent) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "${crossing.fromRegionName} → ${crossing.toRegionName}",
                style = MaterialTheme.typography.titleSmall
            )
            Text(
                text = "${crossing.alertsDelivered} alerts delivered",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Text(
                text = crossing.timestamp,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
