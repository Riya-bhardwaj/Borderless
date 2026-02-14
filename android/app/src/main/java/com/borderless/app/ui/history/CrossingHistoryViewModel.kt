package com.borderless.app.ui.history

import androidx.lifecycle.ViewModel
import com.borderless.app.domain.model.CrossingEvent
import com.borderless.app.domain.repository.CrossingRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import javax.inject.Inject
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.SharingStarted

@HiltViewModel
class CrossingHistoryViewModel @Inject constructor(
    crossingRepository: CrossingRepository
) : ViewModel() {

    val crossings: StateFlow<List<CrossingEvent>> = crossingRepository
        .observeRecentCrossings(50)
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
}
