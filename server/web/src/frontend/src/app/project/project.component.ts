import { Observable } from 'rxjs';
import { Component, OnInit, Inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';
import {
  TrainingStatus,
  TrainingService,
  Training,
  DecodeService,
  DecodeMessage,
  Project,
  ProjectService }
from 'swagger-client';

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

  graphUrl;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public trainingService: TrainingService,
    public decodeService: DecodeService,
    public projectService: ProjectService,
    private snackBar: MatSnackBar
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
              //console.log("Decodings: " + decodings);
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
        this.snackBar.open("Erstelle neues Training...", "", { duration: 2000 });
        this.router.navigate(['/upload/training/' + this.projectUuid + "/" + this.training.version]);
      });
  }

  openTraining(trainingVersion:number, trainingStatus:TrainingStatus) {
    const success = 300;
    const failure = 320;
    console.log(trainingStatus);
    if(trainingStatus == success)
    {
      this.snackBar.open("Öffne Trainingsübersicht...", "", { duration: 2000 });
      this.router.navigate(['/upload/training/overview/' + this.projectUuid + "/" + trainingVersion]);
    }else if (trainingStatus == failure) {
      this.trainingService.createTraining(this.projectUuid)
      .subscribe(training => {
        this.training = training;
        // opens training dialog
        this.snackBar.open("Erstelle neues Training...", "", { duration: 2000 });
        this.router.navigate(['/upload/training/' + this.projectUuid + "/" + this.training.version]);
      });
    }else {
      this.snackBar.open("Öffne Training...", "", { duration: 2000 });
      this.router.navigate(['/upload/training/' + this.projectUuid + "/" + trainingVersion]);
    }
  }

  createDecode(trainingVersion:number): void {
    this.snackBar.open("Erstelle neues Decoding...", "", { duration: 2000 });
    this.router.navigate(['/upload/decoding/' + this.projectUuid + "/" + trainingVersion]);
  }

  isDownloadTrainingDisabled(trainingStatus:TrainingStatus) {
    let success = 300;

    return trainingStatus != success;
  }

  downloadTraining(trainingVersion:number) {
    this.snackBar.open("Lade Training herunter...", "", { duration: 2000 });
    this.trainingService.downloadModelForTraining(
      this.projectUuid,
      trainingVersion.toString(),
    ).subscribe(blob => {
      this.graphUrl = URL.createObjectURL(blob);

      // calls download dialog
      let a = document.createElement('a');
      a.href = this.graphUrl;
      a.download = 'graphs.zip';
      document.body.appendChild(a);
      a.click();
      setTimeout(() => {
        // cleans up download dialog
        URL.revokeObjectURL(this.graphUrl);
        a.parentNode.removeChild(a);
      }, 5000);
    });
  }
}
