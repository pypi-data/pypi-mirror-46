import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { JsonpModule } from '@angular/http';
import { HttpClientModule } from '@angular/common/http';
import { SimpleNotificationsModule } from 'angular2-notifications';
import { AppComponent } from './app.component';
import { routing,
        appRoutingProviders } from './app.routing';

// top level modules
import { LoginModule } from './login/login.module';
import { ShakeCastModule } from './shakecast/shakecast.module';
import { ShakeCastAdminModule } from './shakecast-admin/shakecast-admin.module';

// navbar
import { NavComponent } from './nav/nav.component';
// page title
import { TitleComponent } from './title/title.component';
import { TitleService } from './title/title.service';

import { NotificationsService } from 'angular2-notifications';

// General services used by multiple modules
import { UserService } from './login/user.service';
import { EarthquakeService } from './shakecast/pages/earthquakes/earthquake.service';
import { FacilityService } from './shakecast-admin/pages/facilities/facility.service';
import { NotificationService } from './shakecast/pages/dashboard/notification-dash/notification.service';
import { SharedModule } from './shared/shared.module';
import { MapService } from './shared/maps/map.service';
import { ScreenDimmerService } from './shared/screen-dimmer/screen-dimmer.service';
import { GroupService } from './shakecast-admin/pages/groups/group.service';
import { UsersService } from './shakecast-admin/pages/users/users.service';
import { TimeService } from './shakecast-admin/pages/config/time.service';
import { PanelService } from './shared/panels/panel.service';

import { StickToTopService } from './shared/directives/stick-to-top.service';
import { MessagingComponent } from './messaging/messaging.component';
import { MessagesService } from './shared/messages.service';
import { CookieService } from './shared/cookie.service';

import { LoadingService } from './loading/loading.service';
import { LoadingComponent } from './loading/loading.component';

@NgModule({
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    SimpleNotificationsModule.forRoot(),
    routing,
    HttpClientModule,
    JsonpModule,
    LoginModule,
    SharedModule
  ],
  declarations: [
    AppComponent,
    NavComponent,
    TitleComponent,
    MessagingComponent,
    LoadingComponent
  ],
  providers: [
    appRoutingProviders,
    UserService,
    EarthquakeService,
    FacilityService,
    MapService,
    StickToTopService,
    ScreenDimmerService,
    NotificationService,
    GroupService,
    UsersService,
    TimeService,
    TitleService,
    MessagesService,
    CookieService,
    LoadingService,
    NotificationsService,
    PanelService
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule {
}
