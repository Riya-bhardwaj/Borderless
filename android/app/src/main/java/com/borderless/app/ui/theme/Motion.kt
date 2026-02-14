package com.borderless.app.ui.theme

import androidx.compose.animation.EnterTransition
import androidx.compose.animation.ExitTransition
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally

/**
 * Material 3 motion tokens for consistent animation across the app.
 */
object BorderlessMotion {
    // Duration tokens (ms)
    const val DURATION_SHORT = 150
    const val DURATION_MEDIUM = 300
    const val DURATION_LONG = 500

    // Navigation transitions
    val navEnter: EnterTransition = fadeIn(tween(DURATION_MEDIUM)) +
        slideInHorizontally(tween(DURATION_MEDIUM)) { it / 4 }

    val navExit: ExitTransition = fadeOut(tween(DURATION_SHORT)) +
        slideOutHorizontally(tween(DURATION_MEDIUM)) { -it / 4 }

    val navPopEnter: EnterTransition = fadeIn(tween(DURATION_MEDIUM)) +
        slideInHorizontally(tween(DURATION_MEDIUM)) { -it / 4 }

    val navPopExit: ExitTransition = fadeOut(tween(DURATION_SHORT)) +
        slideOutHorizontally(tween(DURATION_MEDIUM)) { it / 4 }

    // Fade-through for tab switches
    val fadeThroughEnter: EnterTransition = fadeIn(tween(DURATION_MEDIUM))
    val fadeThroughExit: ExitTransition = fadeOut(tween(DURATION_SHORT))
}
