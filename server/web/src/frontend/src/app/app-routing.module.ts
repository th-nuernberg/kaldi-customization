import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ProjectComponent } from './project/project.component';
import { CoverComponent } from './cover/cover.component';
import { DecodingUploadComponent } from './upload/decoding/decoding.upload.component';
import { TrainingUploadComponent } from './upload/training/training.upload.component';
import { AccountComponent } from './account/account.component';

const routes: Routes = [
  { path: '', component: CoverComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'project/:uuid', component: ProjectComponent },
  { path: 'upload/decoding/:uuid', component: DecodingUploadComponent },
  { path: 'upload/training/:uuid', component: TrainingUploadComponent },
  { path: 'account',   component: AccountComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
