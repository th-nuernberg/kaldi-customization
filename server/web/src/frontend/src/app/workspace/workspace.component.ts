import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-workspace',
  templateUrl: './workspace.component.html',
  styleUrls: ['./workspace.component.less']
})
export class WorkspaceComponent implements OnInit {
  public workspaces = [
    { name: "Workspace 1", link:"/workspace/_", projects: [{name: "Project 1", link:"/project/_"}, {name: "Project 2", link:"/project/_"}, {name: "Project 3", link:"/project/_"}]},
    { name: "Workspace 2", link:"/workspace/_", projects: [{name: "Project 1", link:"/project/_"}, {name: "Project 2", link:"/project/_"}, {name: "Project 3", link:"/project/_"}]},
    { name: "Workspace 3", link:"/workspace/_", projects: [{name: "Project 1", link:"/project/_"}, {name: "Project 2", link:"/project/_"}, {name: "Project 3", link:"/project/_"}]}
  ]
  constructor() { }

  ngOnInit() {
  }

  // create new workspace => Workspace Wizard -> name, visibility,
  create() {

  }
}
