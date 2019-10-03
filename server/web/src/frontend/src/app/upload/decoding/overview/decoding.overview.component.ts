import { Observable } from 'rxjs';
import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';
import { DomSanitizer } from '@angular/platform-browser';
import {
  Audio,
  DecodeSession,
  Project,
  Training,
  DecodeService,
  LoggingService,
  ProjectService,
  TrainingService,
}
from 'swagger-client';
import AppConstants from  '../../../app.component';

@Component({
  selector: 'app-dashboard',
  templateUrl: './decoding.overview.component.html',
  styleUrls: ['./decoding.overview.component.less']
})

export class DecodingOverviewComponent implements OnInit {
  projectUuid:string;
  sessionUuid:string;
	trainingVersion:number;

	project$:Observable<Project>;
  training$:Observable<Training>;
  decodeSession$:Observable<DecodeSession>;

  decodeSessionLog$:Observable<string>;

  currentlyPlayingAudio? : {
    audio: Audio,
    data: string
  } = null;
  @ViewChild('audioPlayer') audioPlayer;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private sanitizer:DomSanitizer,
    private snackBar: MatSnackBar,
    private trainingService: TrainingService,
    private loggingService: LoggingService,
    private projectService: ProjectService,
    private decodeService: DecodeService
	) { }
	ngOnInit() {
      this.projectUuid = this.route.snapshot.paramMap.get('puuid');
    	this.sessionUuid = this.route.snapshot.paramMap.get('duuid');
    	this.trainingVersion =  +this.route.snapshot.paramMap.get('id');

    	this.project$ = this.projectService.getProjectByUuid(this.projectUuid)
      this.training$ = this.trainingService.getTrainingByVersion(this.projectUuid, this.trainingVersion);
      this.decodeSession$ = this.decodeService.getDecodeSession(this.projectUuid, this.trainingVersion, this.sessionUuid);
      this.decodeSessionLog$ = this.loggingService.getDecodeSessionLog(this.projectUuid, this.trainingVersion, this.sessionUuid);

      /*
        Play audio
        copy to clipboard - transcripts
        download - transcripts
      */
	}

	ngOnDestroy() {	}

	backToProjectOverview() {
  		this.router.navigate(["/project/" + this.projectUuid]);
  }

  downloadLog(data:string, name:string) {
    this.snackBar.open("Lade" + name + " Log herunter...", "", AppConstants.snackBarConfig);

    if(!data) {
      console.error("No data!");
      return;
    }

    let blob = new Blob([data], {type: 'text/plain'});
    let event = document.createEvent('MouseEvent');
    let a = document.createElement('a');

    a.href = URL.createObjectURL(blob);
    a.download = name + '.txt';
    a.dataset.downloadurl = ['text/plain', a.download, a.href].join(':');
    event.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
    a.dispatchEvent(event);
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

  audioData() {
    if (!this.currentlyPlayingAudio)
      return null;

    return this.sanitizer.bypassSecurityTrustResourceUrl(this.currentlyPlayingAudio.data);
  }

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

  stopAudio() {
    this.currentlyPlayingAudio = null;
  }

  isPlaying(audio: Audio) {
    return (this.currentlyPlayingAudio && this.currentlyPlayingAudio.audio.uuid == audio.uuid);
  }
}
