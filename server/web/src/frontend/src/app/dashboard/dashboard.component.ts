import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.less']
})
export class DashboardComponent implements OnInit {

  public projects = [
    { name: "Project 1", link:"/project/_", models: [{name: "Model 1", link:"/project/_"}, {name: "Model 2", link:"/project/_"}, {name: "Model 3", link:"/project/_"}]},
    { name: "Project 2", link:"/project/_", models: [{name: "Model 1", link:"/project/_"}, {name: "Model 2", link:"/project/_"}, {name: "Model 3", link:"/project/_"}]},
    { name: "Project 3", link:"/project/_", models: [{name: "Model 1", link:"/project/_"}, {name: "Model 2", link:"/project/_"}, {name: "Model 3", link:"/project/_"}]} 
  ]
  constructor() { }

  ngOnInit() {
  }
  
  //TODO load all recent executions of training (workspace, project), latest 10
  loadRecentExecutions() {
    // Name - Last Execution
  }
  //TODO load all workspaces
  loadUserWorkspaces() {
    // Name - List of Projects
  }
  //TODO load all project
  loadUserProject() {
    // Name - List of Models
  }
}
