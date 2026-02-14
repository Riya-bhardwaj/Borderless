package com.borderless.app.di

import android.content.Context
import androidx.room.Room
import com.borderless.app.data.local.BorderlessDatabase
import com.borderless.app.data.local.CrossingHistoryDao
import com.borderless.app.data.local.NotificationStateDao
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): BorderlessDatabase {
        return Room.databaseBuilder(
            context,
            BorderlessDatabase::class.java,
            "borderless.db"
        ).build()
    }

    @Provides
    fun provideCrossingHistoryDao(db: BorderlessDatabase): CrossingHistoryDao {
        return db.crossingHistoryDao()
    }

    @Provides
    fun provideNotificationStateDao(db: BorderlessDatabase): NotificationStateDao {
        return db.notificationStateDao()
    }
}
