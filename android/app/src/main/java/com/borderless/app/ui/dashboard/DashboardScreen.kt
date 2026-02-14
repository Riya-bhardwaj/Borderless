package com.borderless.app.ui.dashboard

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.borderless.app.ui.components.EmptyState
import com.borderless.app.ui.components.ErrorState
import com.borderless.app.ui.components.LoadingState
import com.borderless.app.ui.components.RegionSummaryCard
import com.borderless.app.ui.theme.SeverityCritical
import com.borderless.app.ui.theme.SeverityImportant
import com.borderless.app.ui.theme.SeverityInformational

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DashboardScreen(
    onViewAlerts: (String) -> Unit,
    viewModel: DashboardViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Borderless") })
        }
    ) { padding ->
        when {
            uiState.isLoading -> LoadingState(modifier = Modifier.padding(padding))
            uiState.error != null -> ErrorState(
                message = uiState.error!!,
                onRetry = viewModel::loadDashboard,
                modifier = Modifier.padding(padding)
            )
            else -> DashboardContent(
                uiState = uiState,
                onViewAlerts = onViewAlerts,
                modifier = Modifier.padding(padding)
            )
        }
    }
}

@Composable
private fun DashboardContent(
    uiState: DashboardUiState,
    onViewAlerts: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    LazyColumn(
        modifier = modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Region summary card
        item {
            if (uiState.currentRegion != null) {
                RegionSummaryCard(region = uiState.currentRegion)
            } else {
                EmptyState(
                    title = "No Region Detected",
                    message = "Enable location to detect your current region"
                )
            }
        }

        // Alert count chips
        if (uiState.totalAlertCount > 0) {
            item {
                Text(
                    text = "Active Alerts",
                    style = MaterialTheme.typography.titleMedium
                )
                Spacer(modifier = Modifier.height(8.dp))
                Row(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    AlertCountChip("Legal", uiState.legalCount, SeverityCritical)
                    AlertCountChip("Cultural", uiState.culturalCount, SeverityImportant)
                    AlertCountChip("Behavioral", uiState.behavioralCount, SeverityInformational)
                }
            }

            // View all alerts button
            item {
                uiState.currentRegion?.let { region ->
                    TextButton(onClick = { onViewAlerts(region.id) }) {
                        Text("View All ${uiState.totalAlertCount} Alerts")
                    }
                }
            }
        }

        // Recent crossings
        if (uiState.recentCrossings.isNotEmpty()) {
            item {
                Text(
                    text = "Recent Crossings",
                    style = MaterialTheme.typography.titleMedium
                )
            }

            items(uiState.recentCrossings) { crossing ->
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { onViewAlerts(crossing.toRegionId) },
                    elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
                ) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Text(
                            text = "${crossing.fromRegionName} → ${crossing.toRegionName}",
                            style = MaterialTheme.typography.titleSmall
                        )
                        Text(
                            text = "${crossing.alertsDelivered} alerts delivered",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun AlertCountChip(
    label: String,
    count: Int,
    color: androidx.compose.ui.graphics.Color
) {
    Surface(
        color = color.copy(alpha = 0.1f),
        shape = MaterialTheme.shapes.small
    ) {
        Column(modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)) {
            Text(
                text = count.toString(),
                style = MaterialTheme.typography.titleLarge,
                color = color
            )
            Text(
                text = label,
                style = MaterialTheme.typography.labelSmall,
                color = color
            )
        }
    }
}
