package com.borderless.app.ui.alerts

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
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.borderless.app.domain.model.AlertCategory
import com.borderless.app.ui.components.AlertCard
import com.borderless.app.ui.components.EmptyState
import com.borderless.app.ui.components.ErrorState
import com.borderless.app.ui.components.LoadingState

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AlertDetailScreen(
    regionId: String,
    onBackClick: () -> Unit,
    viewModel: AlertDetailViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(uiState.regionName.ifEmpty { "Alerts" }) },
                navigationIcon = {
                    IconButton(onClick = onBackClick) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        when {
            uiState.isLoading -> LoadingState(
                message = "Loading alerts...",
                modifier = Modifier.padding(padding)
            )
            uiState.error != null -> ErrorState(
                message = uiState.error!!,
                onRetry = viewModel::loadAlerts,
                modifier = Modifier.padding(padding)
            )
            uiState.alerts.isEmpty() -> EmptyState(
                title = "No Alerts",
                message = "No alerts available for this region",
                modifier = Modifier.padding(padding)
            )
            else -> AlertDetailContent(
                uiState = uiState,
                onCategorySelected = viewModel::selectCategory,
                onToggleShowAll = viewModel::toggleShowAll,
                modifier = Modifier.padding(padding)
            )
        }
    }
}

@Composable
private fun AlertDetailContent(
    uiState: AlertDetailUiState,
    onCategorySelected: (AlertCategory?) -> Unit,
    onToggleShowAll: () -> Unit,
    modifier: Modifier = Modifier
) {
    LazyColumn(
        modifier = modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        // Category filter chips
        item {
            Row(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                FilterChip(
                    selected = uiState.selectedCategory == null,
                    onClick = { onCategorySelected(null) },
                    label = { Text("All (${uiState.alerts.size})") }
                )
                FilterChip(
                    selected = uiState.selectedCategory == AlertCategory.LEGAL,
                    onClick = { onCategorySelected(AlertCategory.LEGAL) },
                    label = { Text("Legal (${uiState.legalCount})") }
                )
                FilterChip(
                    selected = uiState.selectedCategory == AlertCategory.CULTURAL,
                    onClick = { onCategorySelected(AlertCategory.CULTURAL) },
                    label = { Text("Cultural (${uiState.culturalCount})") }
                )
                FilterChip(
                    selected = uiState.selectedCategory == AlertCategory.BEHAVIORAL,
                    onClick = { onCategorySelected(AlertCategory.BEHAVIORAL) },
                    label = { Text("Behavioral (${uiState.behavioralCount})") }
                )
            }
        }

        item { Spacer(modifier = Modifier.height(8.dp)) }

        // Alert cards
        items(uiState.filteredAlerts) { alert ->
            AlertCard(alert = alert)
        }

        // Show more / Show less
        if (uiState.alerts.size > 5) {
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    TextButton(onClick = onToggleShowAll) {
                        Text(
                            text = if (uiState.showAll) "Show Less" else "View All ${uiState.alerts.size} Alerts",
                            style = MaterialTheme.typography.labelLarge
                        )
                    }
                }
            }
        }
    }
}
