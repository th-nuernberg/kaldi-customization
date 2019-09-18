import { Observable } from 'rxjs';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { SelectionModel } from '@angular/cdk/collections';
import { MatTableDataSource } from '@angular/material/table';
import { MatSnackBar } from '@angular/material';

import {
  Project,
  Resource,
  Training,
  ProjectService,
  ResourceService,
  TrainingService,
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
  currentTrainingResourcesWithCorupus: [Resource, string][];
  allResources:MatTableDataSource<Resource>;

  getCorpusInterval:any;
  displayedColumns: string[] = ['select', 'name', 'type'];
  show:boolean = true;
  showContentPreview:boolean;
  fileContent: string | ArrayBuffer;

  public historySelection = new SelectionModel<Resource>(true, []);

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private trainingService: TrainingService,
    private resourceService: ResourceService,
    private projectService: ProjectService,
    private snackBar: MatSnackBar
    ) {}
  // TODO post model information to the API: text files, project name, model name, prev model etc..
  ngOnInit() {
    this.currentTrainingResources = [];
    this.currentTrainingResourcesWithCorupus = [];

    this.projectUuid = this.route.snapshot.paramMap.get('uuid');
    this.trainingVersion =  +this.route.snapshot.paramMap.get('id');

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
      this.currentTrainingResources = training.resources;
    });

    // init preview
    this.fileContent = "";
    this.showContentPreview = false;

    this.getCorpusInterval = setInterval(
      () => this.getResourceCorpusResult(),
      10000);
  }

  ngOnDestroy() {
    this.currentTrainingResources = [];
    this.currentTrainingResourcesWithCorupus = [];

    clearInterval(this.getCorpusInterval);
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
      this.currentTrainingResources.push(resource);
      this.trainingService.assignResourceToTraining(
        this.projectUuid,
        this.trainingVersion,
        { resource_uuid: resource.uuid })
      .subscribe(this.currentTrainingResources.push);
    });

    this.snackBar.open("Kopiere Ressource in das aktuelle Training...", "", { duration: 3000 });
  }

  onSelectionChange(ev, selectedResources) {
    if(ev.option.selected === false) {
      this.showContentPreview = false;
      this.fileContent = "";
    } else {
      selectedResources.forEach(selectedElement => {
        const selectedResource:Resource = selectedElement.value;
        //console.log("Selected: " + selectedElement.selected);
        for(let item of this.currentTrainingResourcesWithCorupus) {
          const resourceWithCorpus = item[0];
          const corpusContent = item[1];

          if(resourceWithCorpus.uuid == selectedResource.uuid) {
            this.fileContent = corpusContent;
            this.showContentPreview = true;
          }
        }
      });
    }
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
          this.currentTrainingResources.splice(index, 1);
        });
      }
    });

    this.snackBar.open("Lösche Ressource vom aktuellen Training...", "", { duration: 3000 });
  }

  // uploads file and show preview
  loadFile(file:HTMLInputElement) {
    this.uploadResource(file);
  }

  uploadResource(file) {
    const blobFile:Blob = file.files[0] as Blob;

    // creates resource and starts the TextPrepWorker to create the corupus
    this.resourceService.createResource(blobFile)
      .subscribe(resource => {
        this.currentTrainingResources.push(resource);
        this.trainingService.assignResourceToTraining(
          this.projectUuid,
          this.trainingVersion,
          { resource_uuid: resource.uuid })
        .subscribe(this.currentTrainingResources.push);
    });

    this.snackBar.open("Lade neue Ressource hoch...", "", { duration: 3000 });
  }

  reloadProject() {
    this.project$ = this.projectService.getProjectByUuid(this.projectUuid);
    this.training$ = this.trainingService.getTrainingByVersion(this.projectUuid, this.trainingVersion);

    // init current training resources - second view
    this.training$.subscribe(training => {
      this.currentTrainingResources = training.resources;
    });
  }

  getResourceCorpusResult() {
    this.currentTrainingResources.forEach(resource => {
      this.trainingService.getCorpusOfTrainingResource(
        this.projectUuid,
        this.trainingVersion,
        resource.uuid).subscribe(corpus => {
          this.currentTrainingResourcesWithCorupus.push([resource, corpus])
      });
    });
  }

  startTraining() {
    this.trainingService.startTrainingByVersion(this.projectUuid, this.trainingVersion)
    .subscribe(training => {
      this.snackBar.open("Starte Training...", "", { duration: 3000 });
      this.router.navigate(["/upload/training/overview/" + this.projectUuid + "/" + this.trainingVersion]);
    });
  }
}
