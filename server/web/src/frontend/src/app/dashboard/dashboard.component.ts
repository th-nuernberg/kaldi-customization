import { Component, OnInit } from '@angular/core';
import {
  ProjectService,
  Project,
  GlobalService,
  AcousticModel
} from 'swagger-client';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';;

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.less']
})

export class DashboardComponent implements OnInit {
  public gridProjectTiles: Project[];
  public acousticModels: AcousticModel[];
  public maxCols: 4;

  createProjectSubmitted = false;
  createProjectForm: FormGroup;

  constructor(
    private projectService: ProjectService,
     private globalService: GlobalService,
     private formBuilder: FormBuilder,){
  }

  ngOnInit() {
    this.gridProjectTiles = [];
    this.acousticModels = [];

    this.createProjectForm = this.formBuilder.group({
      projectName: ['', Validators.required],
      modelValue: ['', Validators.required]
    });

    // gets all existing projects
    this.projectService.getProjects().subscribe(project => {
      this.gridProjectTiles = project;
    });

    // get all existing acoustic models
    this.globalService.getAcousticModels().subscribe(model => {
      this.acousticModels = model;
    });
  }

  get f() { return this.createProjectForm.controls; }

  // creates a new project with the passed project name and acoustic model uuid
  createProject() {

    this.createProjectSubmitted = true;

    // stop here if form is invalid
    if (this.createProjectForm.invalid) {
        return;
    }
    const projectName = this.f.projectName.value;
    const acousticModelUuid = this.f.modelValue.value.uuid;
    // console.log("Creates new project: " + projectName + " with uuid: " + acousticModelUuid);
    this.projectService.createProject(
      {
        name: projectName,
        acoustic_model: acousticModelUuid
      }
    )
    .subscribe(project => {
      this.gridProjectTiles.push(project);
      this.createProjectSubmitted = false;
      this.createProjectForm.reset();
     });

  }
}
