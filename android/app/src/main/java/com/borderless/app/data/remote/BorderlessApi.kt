package com.borderless.app.data.remote

import com.borderless.app.data.remote.dto.AlertsResponse
import com.borderless.app.data.remote.dto.CrossingRequest
import com.borderless.app.data.remote.dto.CrossingResponse
import com.borderless.app.data.remote.dto.CrossingsListResponse
import com.borderless.app.data.remote.dto.QaRequest
import com.borderless.app.data.remote.dto.QaResponse
import com.borderless.app.data.remote.dto.RegionsResponse
import com.borderless.app.data.remote.dto.UserProfileRequest
import com.borderless.app.data.remote.dto.UserProfileResponse
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query

interface BorderlessApi {

    @GET("regions")
    suspend fun getRegions(
        @Header("Authorization") authToken: String
    ): RegionsResponse

    @GET("regions/{regionId}/alerts")
    suspend fun getAlerts(
        @Header("Authorization") authToken: String,
        @Path("regionId") regionId: String,
        @Query("language") language: String? = null,
        @Query("severity") severity: String? = null
    ): AlertsResponse

    @POST("qa")
    suspend fun askQuestion(
        @Header("Authorization") authToken: String,
        @Body request: QaRequest
    ): QaResponse

    @POST("users/profile")
    suspend fun createOrUpdateProfile(
        @Header("Authorization") authToken: String,
        @Body request: UserProfileRequest
    ): UserProfileResponse

    @POST("crossings")
    suspend fun logCrossing(
        @Header("Authorization") authToken: String,
        @Body request: CrossingRequest
    ): CrossingResponse

    @GET("crossings")
    suspend fun getCrossings(
        @Header("Authorization") authToken: String,
        @Query("limit") limit: Int? = null
    ): CrossingsListResponse
}
