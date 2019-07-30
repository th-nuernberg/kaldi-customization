import { BrowserModule } from '@angular/platform-browser';
import { FlexLayoutModule } from '@angular/flex-layout';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CommonModule } from '@angular/common';
import { TransferHttpCacheModule } from '@nguniversal/common';
import { HttpClientModule } from '@angular/common/http';
import { NgtUniversalModule } from '@ng-toolkit/universal';
import { FormsModule } from '@angular/forms';
import {
  MatButtonModule,
  MatCheckboxModule,
  MatCardModule,
  MatIconModule,
  MatToolbarModule,
  MatSidenavModule,
  MatListModule,
  MatTabsModule,
  MatSelectModule,
  MatDividerModule,
  MatInputModule,
  MatTableModule,
} from '@angular/material';

import { MatDialogModule } from '@angular/material/dialog';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ProjectComponent, ModelOverviewDialog } from './project/project.component';
import { CoverComponent } from './cover/cover.component';
import { UploadComponent } from './upload/upload.component';
import { AccountComponent } from './account/account.component';

import { TileComponent } from './dashboard/tile/tile.component';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    ProjectComponent,
    CoverComponent,
    UploadComponent,
    AccountComponent,
    TileComponent,
    ModelOverviewDialog
  ],
  imports: [
    BrowserModule.withServerTransition({ appId: 'serverApp' }),
    AppRoutingModule,
    CommonModule,
    TransferHttpCacheModule,
    HttpClientModule,
    NgtUniversalModule,
    FlexLayoutModule,
    MatIconModule,
    MatToolbarModule,
    MatSidenavModule,
    MatButtonModule,
    MatCardModule,
    MatCheckboxModule,
    MatListModule,
    MatTabsModule,
    MatInputModule,
    MatDividerModule,
    MatTableModule,
    MatSelectModule,
    FormsModule,
    MatDialogModule,
  ],
  providers: [],
  entryComponents: [
    ModelOverviewDialog
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
