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
from 'swagger-client';
import AppConstants from  '../../app.component';

@Component({
  selector: 'app-dashboard',
  templateUrl: './training.upload.component.html',
  styleUrls: [
    './training.upload.component.less',
    ]
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
      this.trainingService.assignResourceToTraining(
        this.projectUuid,
        this.trainingVersion,
        { resource_uuid: resource.uuid })
      .subscribe(assignedResource => {
        if(this.currentTrainingResources.indexOf(assignedResource) !== -1) {
          return;
        }

        this.currentTrainingResources.push(assignedResource);
       });
    });

    this.snackBar.open("Kopiere Ressource in das aktuelle Training...", "", AppConstants.snackBarConfig);
  }

  // show the selected content of a corpus
  onSelectionChange(ev, selectedResources) {
    if(ev.option.selected === false) {
      this.showContentPreview = false;
      this.fileContent = "";
    } else {
      selectedResources.forEach(selectedElement => {
        const selectedResource:Resource = selectedElement.value;
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

    this.snackBar.open("Lösche Ressource vom aktuellen Training...", "", AppConstants.snackBarConfig);
  }

  // uploads file and show preview
  loadFile(file:HTMLInputElement) {
    this.uploadResource(file);
  }

  // uploads new resource and assigns to training
  uploadResource(file) {
    const blobFile:Blob = file.files[0] as Blob;
    // creates resource and starts the TextPrepWorker to create the corupus
    this.resourceService.createResource(blobFile)
      .subscribe(resource => {
        this.trainingService.assignResourceToTraining(
          this.projectUuid,
          this.trainingVersion,
          { resource_uuid: resource.uuid })
        .subscribe(assignedResource => {
          if(this.currentTrainingResources.indexOf(assignedResource) !== -1) {
            return;
          }

          this.currentTrainingResources.push(assignedResource);
        });
    });

    this.snackBar.open("Lade neue Ressource hoch...", "", AppConstants.snackBarConfig);
  }

  // reloads project, copies existing resources to training or prepares training
  async reloadProject(newResources:boolean=false) {
    if(newResources) {
      await this.copyResource();
    } else {
      await this.prepareTraining();
    }

    this.project$ = this.projectService.getProjectByUuid(this.projectUuid);
    this.training$ = this.trainingService.getTrainingByVersion(this.projectUuid, this.trainingVersion);

    // init current training resources - second view
    this.training$.subscribe(training => {
      this.currentTrainingResources = training.resources;
    });
  }

  // gets the content of all assigned corpuses
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

  // prepares training and executes the text preparation worker
  prepareTraining() {
    this.trainingService.prepareTrainingByVersion(this.projectUuid, this.trainingVersion)
      .subscribe(training => {
        this.snackBar.open("Bereite Training vor...", "", AppConstants.snackBarConfig);
      })
  }

  // starts the training
  startTraining() {
    this.trainingService.startTrainingByVersion(this.projectUuid, this.trainingVersion)
    .subscribe(training => {
      this.snackBar.open("Starte Training...", "", AppConstants.snackBarConfig);
      this.router.navigate(["/upload/training/overview/" + this.projectUuid + "/" + this.trainingVersion]);
    });
  }
}
