package com.borderless.app.ui.components

import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.borderless.app.domain.model.RiskRating
import com.borderless.app.ui.theme.RiskCritical
import com.borderless.app.ui.theme.RiskHigh
import com.borderless.app.ui.theme.RiskLow
import com.borderless.app.ui.theme.RiskMedium

@Composable
fun RiskRatingChip(
    riskRating: RiskRating,
    modifier: Modifier = Modifier
) {
    val color = when (riskRating) {
        RiskRating.CRITICAL -> RiskCritical
        RiskRating.HIGH -> RiskHigh
        RiskRating.MEDIUM -> RiskMedium
        RiskRating.LOW -> RiskLow
    }

    Surface(
        modifier = modifier,
        color = color.copy(alpha = 0.12f),
        shape = MaterialTheme.shapes.small
    ) {
        Text(
            text = "${riskRating.displayName()} Risk",
            color = color,
            style = MaterialTheme.typography.labelMedium,
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp)
        )
    }
}
