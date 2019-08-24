import { Observable } from 'rxjs';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { SelectionModel } from '@angular/cdk/collections';
import { MatTableDataSource } from '@angular/material/table';

import {
  TrainingService, Training,
  ResourceService, Resource,
  ProjectService, Project
}
from 'swagger-client'

@Component({
  selector: 'app-dashboard',
  templateUrl: './training.upload.component.html',
  styleUrls: ['./training.upload.component.less'],
})

export class TrainingUploadComponent implements OnInit {
  projectUuid:string;
  trainingVersion:number;

  project$:Observable<Project>;
  training$:Observable<Training>;
  resources$:Observable<Array<Resource>>;

  currentTrainingResources:Resource[];
  allResources:MatTableDataSource<Resource>;

  displayedColumns: string[] = ['select', 'name', 'type'];
  show:boolean = true;
  showContentPreview:boolean;
  fileContent: string | ArrayBuffer;

  public historySelection = new SelectionModel<Resource>(true, []);

  constructor(
    private route: ActivatedRoute,
    private trainingService: TrainingService,
    private resourceService: ResourceService,
    private projectService: ProjectService
    ) {
  }
  // TODO post model information to the API: text files, project name, model name, prev model etc..
  ngOnInit() {
    this.projectUuid = this.route.snapshot.paramMap.get('uuid');
    this.trainingVersion =  +this.route.snapshot.paramMap.get('id');

    console.log("Project: " + this.projectUuid + " Trainingsversion: " + this.trainingVersion);

    // init obeservables
    this.training$ = this.trainingService.getTrainingByVersion(this.projectUuid, this.trainingVersion);
    this.project$ = this.projectService.getProjectByUuid(this.projectUuid);
    this.resources$ = this.resourceService.getResource();

    // init all training resources - first view
    this.resources$.subscribe(resources => {
      this.allResources = new MatTableDataSource<Resource>(resources);
    });

    // init current training resources - second view
    this.training$.subscribe(training => {
      console.log("Init: Get Training resource:")
      for(let res of training.resources) {
        console.log(res.name);
      }
      this.currentTrainingResources = training.resources;
    });

    // init preview
    this.fileContent = "";
    this.showContentPreview = false;
  }

  /** Whether the number of selected elements matches the total number of rows. */
  isAllSelected() {
    const numSelected = this.historySelection.selected.length;
    const numRows = this.allResources.data.length;
    return numSelected === numRows;
  }

  /** Selects all rows if they are not all selected; otherwise clear selection. */
  masterToggle() {
    this.isAllSelected() ?
        this.historySelection.clear() :
        this.allResources.data.forEach(row => this.historySelection.select(row));
  }

  /** The label for the checkbox on the passed row */
  checkboxLabel(row?: Resource): string {
    if (!row) {
      return "${this.isAllSelected() ? 'select' : 'deselect'} all";
    }

    return "${this.historySelection.isSelected(row) ? 'deselect' : 'select'} row ${row}";
  }

  // copies selected history elements to current panel
  copyResource() {
    this.historySelection.selected.forEach(resource => {

      console.log("Copied Resource: " + resource.uuid);
      this.currentTrainingResources.push(resource);

      console.log("Assgin resource: " + resource.uuid + "Name: " + resource.name + " to training: " + this.trainingVersion);
      this.trainingService.assignResourceToTraining(
        this.projectUuid,
        this.trainingVersion,
        { resource_uuid: resource.uuid })
      .subscribe(this.currentTrainingResources.push);
    });
  }

  onSelectionChange(ev, selectedResources) {
    console.log(ev);
    if(ev.option.selected === false) {
      this.showContentPreview = false;
      this.fileContent = "";
    } else {
      selectedResources.forEach(element => {
        console.log("Selected: " + element.selected);
        const resource:Resource = element.value;
        this.resourceService.getResourceData(resource.uuid)
          .subscribe(data => {
            console.log("Show preview of resource data: " + data);
            this.showPreview(data);
        });
      });
    }
  }

  showPreview(data:Blob) {
    var reader = new FileReader();
    var me = this;

    reader.readAsText(data);
    reader.onload = function () {
      me.fileContent = reader.result;
    }
    this.showContentPreview = true;
  }

  // removes selected training resources
  remove(selectedResources) {

    selectedResources.forEach(item => {
      const resource:Resource = item.value;
      let index:number = this.currentTrainingResources.findIndex(d => d === resource);

      if(index > -1) {
        this.trainingService.deleteAssignedResourceFromTraining(
          this.projectUuid,
          this.trainingVersion,
          resource.uuid
        ).subscribe(r => {
          console.log("Removed resource: " + r.name + " from training: " + this.projectUuid);
          this.currentTrainingResources.splice(index, 1);
        });
      }
    });
  }

  // uploads file and show preview
  loadFile(file:HTMLInputElement) {
    this.uploadResource(file);
  }

  uploadResource(file) {
    console.log("Uploaded resource: " + file.files[0].name);
    const blobFile:Blob = file.files[0] as Blob;

    // TODO: call TextPrepWorker
    // TODO: set TextPrepWorkerResult as TrainingResource

    this.resourceService.createResource(blobFile)
      .subscribe(resource => {
        console.log("Created Resource: " + resource.uuid);
        this.currentTrainingResources.push(resource);console.log("Assgin resource: " + resource.uuid + "Name: " + resource.name + " to training: " + this.trainingVersion);
        this.trainingService.assignResourceToTraining(
          this.projectUuid,
          this.trainingVersion,
          { resource_uuid: resource.uuid });
    });
  }

  reloadProject() {

    console.log("Reload values on next..");
    this.project$ = this.projectService.getProjectByUuid(this.projectUuid);
    this.training$ = this.trainingService.getTrainingByVersion(this.projectUuid, this.trainingVersion);

    // init current training resources - second view
    this.training$.subscribe(training => {
      this.currentTrainingResources = training.resources;
    });
  }

  startTraining() {
    console.log("Start Training: " + this.trainingVersion + " of Project: " + this.projectUuid);
    console.log(this.project$);
    //this.trainingService.startTrainingByVersion(this.projectUuid, this.trainingVersion);
  }
}
