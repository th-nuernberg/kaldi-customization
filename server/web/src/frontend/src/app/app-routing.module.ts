import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ProjectComponent } from './project/project.component';
import { CoverComponent } from './cover/cover.component';
import { UploadComponent } from './upload/upload.component';
import { AccountComponent } from './account/account.component';

const routes: Routes = [
  { path: '', component: CoverComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'project/:uuid', component: ProjectComponent },
  { path: 'upload/:uuid', component: UploadComponent },
  { path: 'account',   component: AccountComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
