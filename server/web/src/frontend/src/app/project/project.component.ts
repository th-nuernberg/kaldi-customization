import { Component, OnInit, Inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import {
  TrainingService,
  Training,
  DecodeService,
  DecodeMessage,
  Project,
  ProjectService }
from 'swagger-client';

export interface ModelOverviewDialogData {
  id: number,
  project: string,
  prevModel: string,
  status: string,
}

export interface TrainingsModel {
  name: string;
  fileResultName: string;
  date: string;
  link: string;
  texte: string;
}

@Component({
  selector: 'app-project',
  templateUrl: './project.component.html',
  styleUrls: ['./project.component.less']
})
export class ProjectComponent implements OnInit {
  uuid: string;
  project: Project;
  newTraining: Training;
  training_version: number;
  decodings: DecodeMessage[];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public dialog: MatDialog,
    public trainingService: TrainingService,
    public decodeService: DecodeService,
    public projectService: ProjectService
    ) { }

  ngOnInit() {
    this.uuid = this.route.snapshot.paramMap.get('uuid');
    console.log("Passed uuid: " + this.uuid);

    this.projectService.getProjectByUuid(this.uuid)
      .subscribe(project => {
        console.log(project);
        this.project = project;

        if (project.trainings.length) {
          // get all decodings of a project/training
          this.decodeService.getDecodings(
            this.project.uuid,
            this.project.trainings[0].version)
            .subscribe(decodings => {
              console.log("Decodings: " + decodings);
              this.decodings =decodings;
            });
        }
      });
  }

  // creates a new training and opens the training page
  createTraining() {
    this.trainingService.createTraining(this.uuid)
      .subscribe(training => {
        console.log("Created Training: " + training.version);
        this.newTraining = training;
        // opens training dialog
        this.router.navigate(['/upload/training/' +this.project.uuid + "/" + this.newTraining.version]);
      });
  }

  models: TrainingsModel[] =  [
    {
      name: "Model 1",
      fileResultName: "model1.pdf",
      date: "01.01.1970",
      link: "/upload/_/decoding",
      texte: "Reißverschlussverfahren"
    }
];

  openModelOverviewDialog(): void {
    const dialogRef = this.dialog.open(ModelOverviewDialog, {
      width: '250px',
      data: {id: 1337, project: "Project 0815", prevModel: "default", status: "Running" }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }
}

@Component({
  selector: 'model.overview.dialog',
  templateUrl: 'model.overview.dialog.html',
})
export class ModelOverviewDialog {

  constructor(
    public dialogRef: MatDialogRef<ModelOverviewDialog>,
    @Inject(MAT_DIALOG_DATA) public data: ModelOverviewDialogData) {}

  onOkClick(): void {
    this.dialogRef.close();
  }
}
