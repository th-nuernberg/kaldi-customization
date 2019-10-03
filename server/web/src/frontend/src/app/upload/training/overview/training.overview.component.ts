import { Observable } from 'rxjs';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';
import {
  DataPrepStats,
  Project,
  Training,
  LoggingService,
  ProjectService,
  TrainingService,
}
from 'swagger-client';
import AppConstants from  '../../../app.component';

@Component({
  selector: 'app-dashboard',
  templateUrl: './training.overview.component.html',
  styleUrls: [
    './training.overview.component.less'
  ]
})

export class TrainingOverviewComponent implements OnInit {
	projectUuid:string;
	trainingVersion:number;

	project$:Observable<Project>;
  training$:Observable<Training>;

  preparationLog$:Observable<string>;
  resourceLog$:Observable<string>;
  trainingLog$:Observable<string>;

  trainingStats$:Observable<DataPrepStats>;

  graphUrl;

  	constructor(
    	private route: ActivatedRoute,
      private router: Router,
      private snackBar: MatSnackBar,
	    private trainingService: TrainingService,
	    private loggingService: LoggingService,
	    private projectService: ProjectService,
	) { }
	ngOnInit() {
    	this.projectUuid = this.route.snapshot.paramMap.get('uuid');
    	this.trainingVersion =  +this.route.snapshot.paramMap.get('id');

    	this.project$ = this.projectService.getProjectByUuid(this.projectUuid)
    	this.training$ = this.trainingService.getTrainingByVersion(this.projectUuid, this.trainingVersion);

      this.preparationLog$ = this.loggingService.getPerparationLog(this.projectUuid, this.trainingVersion);
      this.resourceLog$ = this.loggingService.getResourceLog(this.projectUuid);
      this.trainingLog$ = this.loggingService.getTrainingLog(this.projectUuid, this.trainingVersion);

      this.trainingStats$ = this.loggingService.getTrainingStats(this.projectUuid, this.trainingVersion);
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
