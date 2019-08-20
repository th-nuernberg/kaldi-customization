import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ProjectComponent } from './project/project.component';
import { CoverComponent } from './cover/cover.component';
import { DecodingUploadComponent } from './upload/decoding/decoding.upload.component';
import { TrainingUploadComponent } from './upload/training/training.upload.component';
import { AccountComponent } from './account/account.component';
import { LoginComponent } from './login/login.component';
import { AuthGuard } from './_guards/auth.guard';

const routes: Routes = [
  { path: '', component: CoverComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard] },
  { path: 'project/:uuid', component: ProjectComponent, canActivate: [AuthGuard] },
  { path: 'upload/decoding/:uuid', component: DecodingUploadComponent, canActivate: [AuthGuard] },
  { path: 'upload/training/:uuid/:id', component: TrainingUploadComponent, canActivate: [AuthGuard] },
  { path: 'account',   component: AccountComponent, canActivate: [AuthGuard] },
  { path: 'login', component: LoginComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
