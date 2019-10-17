import { Observable } from 'rxjs';
import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';
import {
  Audio,
  TrainingStatus,
  TrainingService,
  DecodeService,
  DecodeSession,
  DecodeSessionStatus,
  Project,
  ProjectService,
}
from 'swagger-client';
import AppConstants from  '../app.component';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-project',
  templateUrl: './project.component.html',
  styleUrls: ['./project.component.less']
})
export class ProjectComponent implements OnInit {

  graphUrl;
  projectUuid: string;
  project$: Observable<Project>;

  decodings: Map<number, Array<DecodeSession>>;
  currentDecodeSessionOfTraining: Map<number, DecodeSession>;

  currentlyPlayingAudio? : {
    audio: Audio,
    data: string
  } = null;
  @ViewChild('audioPlayer') audioPlayer;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private sanitizer:DomSanitizer,
    public trainingService: TrainingService,
    public decodeService: DecodeService,
    public projectService: ProjectService,
    private snackBar: MatSnackBar
    ) {}

  ngOnInit() {
    this.currentDecodeSessionOfTraining = new Map();
    this.decodings = new Map();

    this.projectUuid = this.route.snapshot.paramMap.get('uuid');
    this.project$ = this.projectService.getProjectByUuid(this.projectUuid);

    this.project$.subscribe(project => {
      if (project.trainings.length) {
        project.trainings.forEach(training => {

          this.decodeService.getAllDecodeSessions(project.uuid, training.version)
            .subscribe(decodeSessions => {
              this.decodings.set(training.version, decodeSessions);
          });

          this.decodeService.getCurrentDecodeSession(
            this.projectUuid,
            training.version
          ).subscribe(session => {
            if(session != null) {
              this.currentDecodeSessionOfTraining.set(training.version, session);
            }
          })
        });
      }
    });
  }

  /**
   * Transforms the playing audio data into a secure resource url.
   */
  audioData() {
    if (!this.currentlyPlayingAudio)
      return null;

    return this.sanitizer.bypassSecurityTrustResourceUrl(this.currentlyPlayingAudio.data);
  }

  /**
   * Starts the selected audio file.
   * @param event The passed event of the audio player.
   * @param audio The selected audio file.
   */
  triggerAudio(event, audio) {
    event.stopPropagation();

    if (this.isPlaying(audio)) {
      this.currentlyPlayingAudio = null;
    } else {
      this.decodeService.getAudioData(audio.uuid)
        .subscribe(data => {
          const audioData = URL.createObjectURL(data);
          if (this.currentlyPlayingAudio) {
            URL.revokeObjectURL(this.currentlyPlayingAudio.data);
          }

          this.currentlyPlayingAudio = {
            audio: audio,
            data: audioData
          };

          setTimeout(() => this.audioPlayer.nativeElement.play(), 0);
        });
      }
  }

  /**
  * Stops the running audio file.
  */
  stopAudio() {
    this.currentlyPlayingAudio = null;
  }

  /**
  * Checks if the selected audio file is playing
  * @param audio The selected audio file.
  */
  isPlaying(audio: Audio) {
    return (this.currentlyPlayingAudio && this.currentlyPlayingAudio.audio.uuid == audio.uuid);
  }

  /**
  * Creates a new training and opens the training page.
  */
  createTraining() {
    this.trainingService.createTraining(this.projectUuid)
      .subscribe(training => {
        // opens training dialog
        this.snackBar.open("Erstelle neues Training...", "", AppConstants.snackBarConfig);
        this.router.navigate(['/upload/training/' + this.projectUuid + "/" + training.version]);
      });
  }

  /**
  * Opens the specific training or with a successful training the training overview.
  * @param trainingVersion The training version of the selected training.
  * @param trainingStatus The training status of the selected training.
  */
  openTraining(trainingVersion:number, trainingStatus:TrainingStatus) {
    if(trainingStatus == TrainingStatus.Training_Success)
    {
      this.snackBar.open("Öffne Trainingsübersicht...", "", AppConstants.snackBarConfig);
      this.router.navigate(['/upload/training/overview/' + this.projectUuid + "/" + trainingVersion]);
    }else if (trainingStatus == TrainingStatus.Training_Failure) {
      this.trainingService.createTraining(this.projectUuid)
      .subscribe(training => {
        // opens training dialog
        this.snackBar.open("Erstelle neues Training...", "", AppConstants.snackBarConfig);
        this.router.navigate(['/upload/training/' + this.projectUuid + "/" + training.version]);
      });
    }else {
      this.snackBar.open("Öffne Training...", "", AppConstants.snackBarConfig);
      this.router.navigate(['/upload/training/' + this.projectUuid + "/" + trainingVersion]);
    }
  }

   /**
  * Checks if the training was successful.
  * @param trainingStatus The current training status.
  */
  wasTrainingSuccessful(trainingStatus:TrainingStatus) {
    return trainingStatus != TrainingStatus.Training_Success;
  }

  /**
  * Downloads the results and the content of a specific training.
  * @param trainingVersion The training version.
  */
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

  /**
  * Creates a new decode session of a specific training.
  * @param event The passed event.
  * @param trainingVersion The specific training version.
  */
  createDecode(event, trainingVersion:number): void {

    event.stopPropagation();
    let currentSession = this.currentDecodeSessionOfTraining.get(trainingVersion);
    if(currentSession != null) {
      this.snackBar.open("Öffne laufende Spracherkennung...", "", AppConstants.snackBarConfig);
      this.router.navigate(['/upload/decoding/' + this.projectUuid + "/" + trainingVersion + "/" + currentSession.session_uuid]);
    } else {
      this.decodeService.createDecodeSession(
        this.projectUuid,
        trainingVersion
      ).subscribe(session => {
        this.snackBar.open("Erstelle neue Spracherkennung...", "", AppConstants.snackBarConfig);
        this.router.navigate(['/upload/decoding/' + this.projectUuid + "/" + trainingVersion + "/" + session.session_uuid]);
      });
    }
  }

  /**
   * Checks if decoding session was succesful.
   * @param sessionStatus Status of the decoding session
   */
  wasDecodingSessionSuccessful(sessionStatus:DecodeSessionStatus) {
    return sessionStatus != DecodeSessionStatus.Decoding_Success;
  }

  /**
   * Downloads the created transcript of the decoded audio file.
   * @param data The data of the transcript.
   * @param name The name of the transcript file.
   */
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

  /**
   * Copies the content to the clipboard.
   * @param text The content of the data.
   */
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

  /**
   * Opens the decode session overview.
   * @param trainingVersion The specific training version.
   * @param decodeSessionUuid The specific decode session.
   */
  openDecodeSessionOverview(trainingVersion:number, decodeSessionUuid: string) {

    this.snackBar.open("Öffne Spracherkennung Übersicht...", "", AppConstants.snackBarConfig);
    this.router.navigate(['/upload/decoding/overview/' + this.projectUuid + "/" + trainingVersion + "/" + decodeSessionUuid]);
  }
}
