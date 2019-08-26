import { Observable } from 'rxjs';
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
  projectUuid: string;
  training_version: number;

  training: Training;
  decodings: DecodeMessage[];

  project$: Observable<Project>;
  decodings$: Observable<DecodeMessage[]>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public dialog: MatDialog,
    public trainingService: TrainingService,
    public decodeService: DecodeService,
    public projectService: ProjectService
    ) { }

  ngOnInit() {
    this.decodings = [];
    this.projectUuid = this.route.snapshot.paramMap.get('uuid');
    this.project$ = this.projectService.getProjectByUuid(this.projectUuid);
    this.project$.subscribe(project => {
      if (project.trainings.length) {
        project.trainings.forEach(training => {
          this.decodeService.getDecodings(
            this.projectUuid,
            training.version)
            .subscribe(decodings => {
              console.log("Decodings: " + decodings);
              this.decodings.concat(decodings);
            });
        });
      }
    });
  }

  // creates a new training and opens the training page
  createTraining() {
    this.trainingService.createTraining(this.projectUuid)
      .subscribe(training => {
        console.log("Created Training: " + training.version);
        this.training = training;
        // opens training dialog
        this.router.navigate(['/upload/training/' + this.projectUuid + "/" + this.training.version]);
      });
  }

  openTraining(trainingVersion:number) {
    this.router.navigate(['/upload/training/' + this.projectUuid + "/" + trainingVersion]);
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

  openModelOverviewDialog(trainingVersion:number): void {
    const dialogRef = this.dialog.open(ModelOverviewDialog, {
      width: '250px',
      data: [this.project$, trainingVersion]
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

  projectUuid: string;
  trainingVersion: number;

  constructor(
    public router: Router,
    public dialogRef: MatDialogRef<ModelOverviewDialog>,
    @Inject(MAT_DIALOG_DATA) public data: [Observable<Project>, number]) {
      this.trainingVersion = this.data[1];
      this.data[0].subscribe(project => {
        this.projectUuid = project.uuid;
    }); 
  }

  onOkClick(): void {
    this.dialogRef.close();
  }

  onDecodeClick(): void {
    this.router.navigate(['/upload/decoding/' + this.projectUuid + "/" + this.trainingVersion]);
    this.dialogRef.close();
  }
}
