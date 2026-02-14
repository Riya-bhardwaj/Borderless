package com.borderless.app.ui.navigation

import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.List
import androidx.compose.material.icons.filled.QuestionAnswer
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.navArgument
import com.borderless.app.ui.alerts.AlertDetailScreen
import com.borderless.app.ui.dashboard.DashboardScreen
import com.borderless.app.ui.history.CrossingHistoryScreen
import com.borderless.app.ui.onboarding.OnboardingScreen
import com.borderless.app.ui.qa.QaScreen
import com.borderless.app.ui.settings.SettingsScreen
import com.borderless.app.ui.theme.BorderlessMotion

object Routes {
    const val ONBOARDING = "onboarding"
    const val DASHBOARD = "dashboard"
    const val ALERT_DETAIL = "alert_detail/{regionId}"
    const val QA = "qa"
    const val HISTORY = "history"
    const val SETTINGS = "settings"
    const val LOCATION_PERMISSION = "location_permission"

    fun alertDetail(regionId: String) = "alert_detail/$regionId"
}

data class BottomNavItem(
    val route: String,
    val label: String,
    val icon: ImageVector
)

val bottomNavItems = listOf(
    BottomNavItem(Routes.DASHBOARD, "Dashboard", Icons.Filled.Home),
    BottomNavItem(Routes.QA, "Q&A", Icons.Filled.QuestionAnswer),
    BottomNavItem(Routes.HISTORY, "History", Icons.Filled.List),
    BottomNavItem(Routes.SETTINGS, "Settings", Icons.Filled.Settings)
)

@Composable
fun BorderlessNavHost(
    navController: NavHostController,
    isLoggedIn: Boolean,
    modifier: Modifier = Modifier
) {
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route

    val showBottomBar = currentRoute in bottomNavItems.map { it.route }

    Scaffold(
        bottomBar = {
            if (showBottomBar) {
                NavigationBar {
                    bottomNavItems.forEach { item ->
                        NavigationBarItem(
                            icon = { Icon(item.icon, contentDescription = item.label) },
                            label = { Text(item.label) },
                            selected = navBackStackEntry?.destination?.hierarchy?.any {
                                it.route == item.route
                            } == true,
                            onClick = {
                                navController.navigate(item.route) {
                                    popUpTo(Routes.DASHBOARD) { saveState = true }
                                    launchSingleTop = true
                                    restoreState = true
                                }
                            }
                        )
                    }
                }
            }
        },
        modifier = modifier
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = if (isLoggedIn) Routes.DASHBOARD else Routes.ONBOARDING,
            enterTransition = { BorderlessMotion.navEnter },
            exitTransition = { BorderlessMotion.navExit },
            popEnterTransition = { BorderlessMotion.navPopEnter },
            popExitTransition = { BorderlessMotion.navPopExit },
            modifier = Modifier.padding(innerPadding)
        ) {
            composable(Routes.ONBOARDING) {
                OnboardingScreen(
                    onComplete = {
                        navController.navigate(Routes.DASHBOARD) {
                            popUpTo(Routes.ONBOARDING) { inclusive = true }
                        }
                    }
                )
            }

            composable(
                Routes.DASHBOARD,
                enterTransition = { BorderlessMotion.fadeThroughEnter },
                exitTransition = { BorderlessMotion.fadeThroughExit }
            ) {
                DashboardScreen(
                    onViewAlerts = { regionId ->
                        navController.navigate(Routes.alertDetail(regionId))
                    }
                )
            }

            composable(
                route = Routes.ALERT_DETAIL,
                arguments = listOf(
                    navArgument("regionId") { type = NavType.StringType }
                )
            ) { backStackEntry ->
                val regionId = backStackEntry.arguments?.getString("regionId") ?: return@composable
                AlertDetailScreen(
                    regionId = regionId,
                    onBackClick = { navController.popBackStack() }
                )
            }

            composable(
                Routes.QA,
                enterTransition = { BorderlessMotion.fadeThroughEnter },
                exitTransition = { BorderlessMotion.fadeThroughExit }
            ) {
                QaScreen()
            }

            composable(
                Routes.HISTORY,
                enterTransition = { BorderlessMotion.fadeThroughEnter },
                exitTransition = { BorderlessMotion.fadeThroughExit }
            ) {
                CrossingHistoryScreen()
            }

            composable(
                Routes.SETTINGS,
                enterTransition = { BorderlessMotion.fadeThroughEnter },
                exitTransition = { BorderlessMotion.fadeThroughExit }
            ) {
                SettingsScreen()
            }
        }
    }
}
