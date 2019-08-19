import { Component, OnInit } from '@angular/core';
import { ProjectService, Project } from 'swagger-client'

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.less']
})

export class DashboardComponent implements OnInit {
  public gridProjectTiles: Project[];
  public maxCols: 4;

  constructor(private projectService: ProjectService){

  }

  ngOnInit() {
    this.gridProjectTiles = [];
    this.projectService.getProjects().subscribe(project => {
      this.gridProjectTiles = project;
    });
  }

  createProject(projectName: string, acousticModel: string) {
    if(projectName === "") {
      projectName = "Project Name placeholder";
    }

    if(acousticModel === "") {
      acousticModel = "Acoustic Model placeholder";
    }
    console.log(projectName, acousticModel);
    console.log("Creates new project...");

    this.projectService.createProject(
      {
        name: projectName,
        acousticModel: acousticModel
      }
    )
    .subscribe(this.gridProjectTiles.push);
  }
}
