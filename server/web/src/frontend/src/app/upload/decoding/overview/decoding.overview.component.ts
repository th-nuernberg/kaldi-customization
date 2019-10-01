import { Observable } from 'rxjs';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';
import {
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

  graphUrl;

  	constructor(
    	private route: ActivatedRoute,
      private router: Router,
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
}
