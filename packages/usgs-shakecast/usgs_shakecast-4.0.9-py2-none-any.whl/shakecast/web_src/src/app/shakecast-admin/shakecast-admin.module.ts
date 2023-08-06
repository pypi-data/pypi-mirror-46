import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

import { ShakeCastAdminComponent } from './shakecast-admin.component';
import { routing } from './shakecast-admin.routing';

import { FacilitiesComponent } from './pages/facilities/facilities.component';
import { FacilityFilter } from './pages/facilities/facility-filter/facility-filter.component';

import { GroupsComponent } from './pages/groups/groups.component';
import { GroupListComponent } from './pages/groups/group-list.component';

import { UsersComponent } from './pages/users/users.component';
import { UserListComponent } from './pages/users/user-list.component';

import { ConfigComponent } from './pages/config/config.component';
import { ConfigService } from './pages/config/config.service';

import { UploadComponent } from './upload/upload.component';
import { UploadService } from './upload/upload.service';

import { NotificationsComponent } from './pages/notifications/notifications.component';
import { NotificationHTMLService } from './pages/notifications/notification.service';

import { UpdateComponent } from './update/update.component';
import { UpdateService } from './update/update.service';

import { ScenariosComponent } from './pages/scenarios/scenarios.component';
import { ScenarioSearchComponent } from './pages/scenarios/scenario-search/scenario-search.component';

import { SharedModule } from '../shared/shared.module';

// ng2-file-upload
import { FileUploadModule } from 'ng2-file-upload';

@NgModule({
  imports: [
    FormsModule,
    routing,
    SharedModule,
    FileUploadModule
  ],
  declarations: [
    ShakeCastAdminComponent,
    FacilitiesComponent,
    FacilityFilter,
    GroupsComponent,
    GroupListComponent,
    UsersComponent,
    UserListComponent,
    ConfigComponent,
    UploadComponent,
    NotificationsComponent,
    UpdateComponent,
    ScenariosComponent,
    ScenarioSearchComponent
  ],
  providers: [
    ConfigService,
    UploadService,
    NotificationHTMLService,
    UpdateService
  ]
})
export class ShakeCastAdminModule {
}