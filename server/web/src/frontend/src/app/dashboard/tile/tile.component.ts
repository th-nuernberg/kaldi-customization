import { Component, OnInit, Input, OnChanges } from '@angular/core';
import { Project, Training, TrainingService, TrainingStatus } from 'swagger-client';
import { StatusMapperService } from '../../_services';
import { Router } from '@angular/router';

@Component({
  selector: 'app-tile',
  templateUrl: './tile.component.html',
  styleUrls: ['../dashboard.component.less', './tile.component.less']
})
export class TileComponent implements OnInit, OnChanges {
  @Input() project: Project;
  lastTraining: Training;
  lastTrainingStatus: string;

  constructor(
    private router: Router,
    public trainingService: TrainingService
  ) { }

  ngOnChanges() {
    this.lastTrainingStatus = this.lastTraining ? StatusMapperService.convertTrainingStatus(this.lastTraining.status): "";
  }
  ngOnInit() {
    this.lastTraining = this.project.trainings[this.project.trainings.length-1];
  }

  openTraining() {
    if (this.lastTraining.status >= TrainingStatus.Training_Pending) {
      this.router.navigate(['/upload/training/overview/' + this.project.uuid + "/" + this.lastTraining.version]);
    } else {
      this.router.navigate(['/upload/training/' + this.project.uuid + "/" + this.lastTraining.version]);
    }
  }

  // creates a new training and opens the training page
  createTraining() {
    this.trainingService.createTraining(this.project.uuid)
      .subscribe(training =>
        this.router.navigate(['/upload/training/' + this.project.uuid + "/" + training.version])
      );
  }
}
