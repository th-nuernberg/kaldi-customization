import { Component, OnInit, Input, OnChanges } from '@angular/core';
import { Project, Training } from 'swagger-client';
import { StatusMapperService } from '../../_services';

@Component({
  selector: 'app-tile',
  templateUrl: './tile.component.html',
  styleUrls: ['../dashboard.component.less']
})
export class TileComponent implements OnInit, OnChanges {
  @Input() tileData: Project;
  lastTraining: Training;
  lastTrainingStatus:string;

  constructor() { }

  ngOnChanges() {
    this.lastTrainingStatus = this.lastTraining ? StatusMapperService.convertTrainingStatus(this.lastTraining.status): "";
  }
  ngOnInit() {
    this.lastTraining = this.tileData.trainings[this.tileData.trainings.length-1];
  }
}
