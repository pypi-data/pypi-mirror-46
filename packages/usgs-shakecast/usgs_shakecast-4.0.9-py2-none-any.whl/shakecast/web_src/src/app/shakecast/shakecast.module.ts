import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { ShakeCastComponent } from './shakecast.component';
import { routing } from './shakecast.routing';

import { DashboardComponent } from './pages/dashboard/dashboard.component'
import { NotificationDashComponent } from './pages/dashboard/notification-dash/notification-dash.component'

import { EarthquakeListComponent } from './pages/earthquakes/earthquake-list.component'
import { EarthquakeFilter } from './pages/earthquakes/earthquake-filter/earthquake-filter.component'

import { UserProfileComponent } from './pages/user-profile/user-profile.component'

import { SharedModule } from '../shared/shared.module'

@NgModule({
  imports: [
    FormsModule,
    CommonModule,
    routing,
    SharedModule
  ],
  declarations: [
    ShakeCastComponent,
    DashboardComponent,
    NotificationDashComponent,
    EarthquakeFilter,
    UserProfileComponent
  ],
  providers: [
  ]
})
export class ShakeCastModule {
}