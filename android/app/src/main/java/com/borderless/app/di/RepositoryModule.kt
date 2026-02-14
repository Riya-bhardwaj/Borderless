package com.borderless.app.di

import com.borderless.app.data.repository.AlertRepositoryImpl
import com.borderless.app.data.repository.CrossingRepositoryImpl
import com.borderless.app.data.repository.QaRepositoryImpl
import com.borderless.app.data.repository.RegionRepositoryImpl
import com.borderless.app.data.repository.UserRepositoryImpl
import com.borderless.app.domain.repository.AlertRepository
import com.borderless.app.domain.repository.CrossingRepository
import com.borderless.app.domain.repository.QaRepository
import com.borderless.app.domain.repository.RegionRepository
import com.borderless.app.domain.repository.UserRepository
import dagger.Binds
import dagger.Module
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    @Singleton
    abstract fun bindRegionRepository(impl: RegionRepositoryImpl): RegionRepository

    @Binds
    @Singleton
    abstract fun bindAlertRepository(impl: AlertRepositoryImpl): AlertRepository

    @Binds
    @Singleton
    abstract fun bindUserRepository(impl: UserRepositoryImpl): UserRepository

    @Binds
    @Singleton
    abstract fun bindCrossingRepository(impl: CrossingRepositoryImpl): CrossingRepository

    @Binds
    @Singleton
    abstract fun bindQaRepository(impl: QaRepositoryImpl): QaRepository
}
