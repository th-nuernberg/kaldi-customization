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
import AppConstants from  '../app.component';

const DUMMY_DECODES: DecodeMessage[] = [
  {
    uuid: "550e8400-e29b-11d4-a716-446655440000",
    transcripts: [
      new Object("und die mühsam am auch liegt auf die diesen klicken einem texten zu produzieren"),
      new Object("und die mühsam am auch liegt auf die diesen klicken einem texten zu produzieren"),
      new Object("und die mühsam am auch liegt auf die diesen klicken einem texten zu produzieren")
    ],
    audio: {
      uuid: "550e8400-e29b-11d4-a716-446655440000",
      name: "text.wav",
      status: 300
    }
  },
  {
    uuid: "550e8400-e29b-11d4-a716-446655440000",
    transcripts: [
      new Object("und die mühsam am auch liegt auf die diesen klicken einem texten zu produzieren")
    ],
    audio: {
      uuid: "550e8400-e29b-11d4-a716-446655440000",
      name: "text2.wav",
      status: 300
    }
  },
  {
    uuid: "550e8400-e29b-11d4-a716-446655440000",
    transcripts: [
      new Object("und die mühsam am auch liegt auf die diesen klicken einem texten zu produzieren")
    ],
    audio: {
      uuid: "550e8400-e29b-11d4-a716-446655440000",
      name: "text3.wav",
      status: 300
    }
  },
];

@Component({
  selector: 'app-project',
  templateUrl: './project.component.html',
  styleUrls: ['./project.component.less']
})
export class ProjectComponent implements OnInit {
  projectUuid: string;

  training: Training;
  currentDecodings: DecodeMessage[];

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
    ) {}

  ngOnInit() {
    this.currentDecodings = DUMMY_DECODES;

    this.projectUuid = this.route.snapshot.paramMap.get('uuid');
    this.project$ = this.projectService.getProjectByUuid(this.projectUuid);

    this.project$.subscribe(project => {
      if (project.trainings.length) {
        project.trainings.forEach(training => {
          // TODO what about decodings$ observable solution
          this.decodeService.getDecodings(
            this.projectUuid,
            training.version)
            .subscribe(decodings => {
              //this.currentDecodings.concat(decodings);
          });
        });
      }
    });
  }

  // creates a new training and opens the training page
  createTraining() {
    this.trainingService.createTraining(this.projectUuid)
      .subscribe(training => {
        this.training = training;
        // opens training dialog
        this.snackBar.open("Erstelle neues Training...", "", AppConstants.snackBarConfig);
        this.router.navigate(['/upload/training/' + this.projectUuid + "/" + this.training.version]);
      });
  }

  openTraining(trainingVersion:number, trainingStatus:TrainingStatus) {
    if(trainingStatus == TrainingStatus.Training_Success)
    {
      this.snackBar.open("Öffne Trainingsübersicht...", "", AppConstants.snackBarConfig);
      this.router.navigate(['/upload/training/overview/' + this.projectUuid + "/" + trainingVersion]);
    }else if (trainingStatus == TrainingStatus.Training_Failure) {
      this.trainingService.createTraining(this.projectUuid)
      .subscribe(training => {
        this.training = training;
        // opens training dialog
        this.snackBar.open("Erstelle neues Training...", "", AppConstants.snackBarConfig);
        this.router.navigate(['/upload/training/' + this.projectUuid + "/" + this.training.version]);
      });
    }else {
      this.snackBar.open("Öffne Training...", "", AppConstants.snackBarConfig);
      this.router.navigate(['/upload/training/' + this.projectUuid + "/" + trainingVersion]);
    }
  }

  createDecode(trainingVersion:number): void {
    this.snackBar.open("Erstelle neue Spracherkennung...", "", AppConstants.snackBarConfig);
    this.router.navigate(['/upload/decoding/' + this.projectUuid + "/" + trainingVersion]);
  }

  isDownloadTrainingDisabled(trainingStatus:TrainingStatus) {
    return trainingStatus != TrainingStatus.Training_Success;
  }

  downloadTraining(trainingVersion:number) {
    this.snackBar.open("Lade Training herunter...", "", AppConstants.snackBarConfig);
    this.trainingService.downloadModelForTraining(
      this.projectUuid,
      trainingVersion,
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

  downloadTranscript(data, name:string) {
    let fileName = name.split('.').slice(0, -1).join('.');
    this.snackBar.open("Lade" + fileName + " Transkript herunter...", "", AppConstants.snackBarConfig);

    if(!data) {
      console.error("No data!");
      return;
    }

    let blob = new Blob([data], {type: 'text/plain'});
    let event = document.createEvent('MouseEvent');
    let a = document.createElement('a');

    a.href = URL.createObjectURL(blob);
    a.download = fileName + '.txt';
    a.dataset.downloadurl = ['text/plain', a.download, a.href].join(':');
    event.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
    a.dispatchEvent(event);
  }

  copyToClipboard(text) {
    let tempTextArea = document.createElement('textarea');
    tempTextArea.style.position = 'fixed';
    tempTextArea.style.left = '0';
    tempTextArea.style.top = '0';
    tempTextArea.style.opacity = '0';
    tempTextArea.value = text;

    document.body.appendChild(tempTextArea);
    tempTextArea.select();
    tempTextArea.focus();
    document.execCommand('copy');
    document.body.removeChild(tempTextArea);
  }
}
