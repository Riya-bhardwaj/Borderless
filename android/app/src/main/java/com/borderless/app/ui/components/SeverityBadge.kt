package com.borderless.app.ui.components

import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.borderless.app.domain.model.AlertSeverity
import com.borderless.app.ui.theme.SeverityCritical
import com.borderless.app.ui.theme.SeverityImportant
import com.borderless.app.ui.theme.SeverityInformational

@Composable
fun SeverityBadge(
    severity: AlertSeverity,
    modifier: Modifier = Modifier
) {
    val color = when (severity) {
        AlertSeverity.CRITICAL -> SeverityCritical
        AlertSeverity.IMPORTANT -> SeverityImportant
        AlertSeverity.INFORMATIONAL -> SeverityInformational
    }

    Surface(
        modifier = modifier,
        color = color.copy(alpha = 0.12f),
        shape = MaterialTheme.shapes.small
    ) {
        Text(
            text = severity.displayName(),
            color = color,
            style = MaterialTheme.typography.labelSmall,
            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
        )
    }
}
