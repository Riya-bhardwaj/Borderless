package com.borderless.app.data.remote.dto

data class DeviceTokenRequest(
    val token: String,
    val platform: String = "android"
)
