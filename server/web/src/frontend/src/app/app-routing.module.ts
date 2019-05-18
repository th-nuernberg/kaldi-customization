import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { WorkspaceComponent } from './workspace/workspace.component';
import { ProjectComponent } from './project/project.component';
import { CoverComponent } from './cover/cover.component';
import { AccountComponent } from './account/account.component';

const routes: Routes = [
  { path: '', component: CoverComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'workspace/:uuid', component: WorkspaceComponent },
  { path: 'project/:uuid', component: ProjectComponent },
  { path: 'account',   component: AccountComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
