import { Observable } from 'rxjs';
import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { SelectionModel } from '@angular/cdk/collections';
import { MatTableDataSource } from '@angular/material/table';
import { MatSnackBar, MatSelectionList, MatListOption } from '@angular/material';

import {
  Project,
  Resource,
  Training,
  TrainingStatus,
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
  getTrainingStatusInterval:any;
  displayedColumns: string[] = ['select', 'name', 'type'];

  showContentPreview:boolean;
  fileContent: string | ArrayBuffer;
  canStartTraining:boolean = false;

  public historySelection = new SelectionModel<Resource>(true, []);

  @ViewChild(MatSelectionList) selectionList: MatSelectionList;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private trainingService: TrainingService,
    private resourceService: ResourceService,
    private projectService: ProjectService,
    private snackBar: MatSnackBar
    ) {}

  ngOnInit() {
    this.selectionList.selectedOptions = new SelectionModel<MatListOption>(false);
    this.currentTrainingResources = [];
    this.currentTrainingResourcesWithCorupus = [];

    this.projectUuid = this.route.snapshot.paramMap.get('uuid');
    this.trainingVersion =  +this.route.snapshot.paramMap.get('id');

    // init obeservables
    this.training$ = this.trainingService.getTrainingByVersion(this.projectUuid, this.trainingVersion);
    this.project$ = this.projectService.getProjectByUuid(this.projectUuid);
    this.resources$ = this.resourceService.getResource();

    // init current training resources - second view
    this.training$.subscribe(training => {
      this.currentTrainingResources = training.resources;
    });

    // init all training resources - first view
    this.resources$.subscribe(resources => {
      this.allResources = new MatTableDataSource<Resource>(resources);

      // pre selects resources that are already assigned to training
      this.allResources.data.forEach(row => {

        this.currentTrainingResources.forEach(resource => {
          if(resource.uuid == row.uuid) {
            this.historySelection.select(row);
          }
        });
      });
    });

    // init preview
    this.fileContent = "";
    this.showContentPreview = false;

    this.getCorpusInterval = setInterval(
      () => this.getResourceCorpusResult(),
      10000);

    this.getTrainingStatusInterval = setInterval(
      () => this.getTrainingStatus(),
      5000);
  }

  ngOnDestroy() {
    this.currentTrainingResources = [];
    this.currentTrainingResourcesWithCorupus = [];

    clearInterval(this.getCorpusInterval);
    clearInterval(this.getTrainingStatusInterval);
  }

  /**
   * Checks if all table checkboxes are selected.
   */
  isAllSelected() {
    const numSelected = this.historySelection.selected.length;
    const numRows = this.allResources.data.length;
    return numSelected === numRows;
  }

  /**
   * Master toggles all checkboxes of the table.
   */
  masterToggle() {
    this.isAllSelected() ?
        this.historySelection.clear() :
        this.allResources.data.forEach(row => this.historySelection.select(row));
  }

  /**
   * Gets the label of the checkbox value.
   * @param row The row of the table.
   */
  checkboxLabel(row?: Resource): string {
    if (!row) {
      return "${this.isAllSelected() ? 'select' : 'deselect'} all";
    }

    return "${this.historySelection.isSelected(row) ? 'deselect' : 'select'} row ${row}";
  }

  /**
   * Copies the selected resource files to the current training.
   */
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

  /**
   * Shows the corpus content of the selected resource
   * @param ev The selection event.
   * @param selectedResources The selected training resource.
   */
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

  /**
   * Removes the selected training resources from the training.
   * @param selectedResources
   */
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

  /**
   * Uploads a new resource file to the training session
   * @param file The training resource file.
   */
  loadFile(file:HTMLInputElement) {
    this.uploadResource(file);
  }

  /**
   * Uploads a new resource file to the training session
   * @param file The training resource file.
   */
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

  /**
   * Reloads the training page manually.
   * @param newResources Flag to copy resource or prepare training.
   */
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

  /**
   * Gets the corpus content.
   */
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

  /**
   * Prepares the current training by starting the data preparation.
   */
  prepareTraining() {
    this.trainingService.prepareTrainingByVersion(this.projectUuid, this.trainingVersion)
      .subscribe(training => {
        this.snackBar.open("Bereite Training vor...", "", AppConstants.snackBarConfig);
      })
  }

  /**
   * Gets the current training status.
   */
  getTrainingStatus() {
    this.training$.subscribe(training => {
      this.canStartTraining = training.status == TrainingStatus.Training_DataPrep_Success;
    });
  }

  /**
   * Starts the current training.
   */
  startTraining() {
    this.trainingService.startTrainingByVersion(this.projectUuid, this.trainingVersion)
    .subscribe(training => {
      this.snackBar.open("Starte Training...", "", AppConstants.snackBarConfig);
      this.router.navigate(["/upload/training/overview/" + this.projectUuid + "/" + this.trainingVersion]);
    });
  }
}
