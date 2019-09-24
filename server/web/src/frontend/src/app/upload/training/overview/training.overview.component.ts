import { Observable } from 'rxjs';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import {
  Project,
  Resource,
  Training,
  ProjectService,
  ResourceService,
  TrainingService,
}
from 'swagger-client'

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

  	constructor(
    	private route: ActivatedRoute,
  		private router: Router,
	    private trainingService: TrainingService,
	    private resourceService: ResourceService,
	    private projectService: ProjectService,
	) { }
	ngOnInit() {
    	this.projectUuid = this.route.snapshot.paramMap.get('uuid');
    	this.trainingVersion =  +this.route.snapshot.paramMap.get('id');

    	this.project$ = this.projectService.getProjectByUuid(this.projectUuid)
    	this.training$ = this.trainingService.getTrainingByVersion(this.projectUuid, this.trainingVersion);

	}

	ngOnDestroy() {	}

	backToProjectOverview() {
  		this.router.navigate(["/project/" + this.projectUuid]);
	}
}
