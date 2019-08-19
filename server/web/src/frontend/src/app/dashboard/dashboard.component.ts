import { Component, OnInit } from '@angular/core';
import {
  ProjectService,
  Project,
  GlobalService,
  AcousticModel
} from 'swagger-client';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.less']
})

export class DashboardComponent implements OnInit {
  public gridProjectTiles: Project[];
  public acousticModels: AcousticModel[];
  public maxCols: 4;

  constructor(private projectService: ProjectService, private globalService: GlobalService){

  }

  ngOnInit() {
    this.gridProjectTiles = [];
    this.acousticModels = [];

    this.projectService.getProjects().subscribe(project => {
      this.gridProjectTiles = project;
    });

    // get all existing acoustic models
    this.globalService.getAcousticModels().subscribe(model => {
      this.acousticModels = model;
    });
  }



  createProject(projectName: string, acousticModelUuid: string) {
    if(projectName === "") {
      projectName = "Project Name placeholder";
    }

    // todo: make selection of acoustic model mandatory!!!
    if(acousticModelUuid === "") {
      acousticModelUuid = "Acoustic Model placeholder";
    }
    console.log(projectName, acousticModelUuid);
    console.log("Creates new project...");

    this.projectService.createProject(
      {
        name: projectName,
        acousticModel: acousticModelUuid
      }
    )
    .subscribe(this.gridProjectTiles.push);
  }
}
