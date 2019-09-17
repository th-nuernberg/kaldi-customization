import { Component, OnInit, Input } from '@angular/core';
import { Project, Training } from 'swagger-client';

@Component({
  selector: 'app-tile',
  templateUrl: './tile.component.html',
  styleUrls: ['./tile.component.css']
})
export class TileComponent implements OnInit {
  // TODO check for future details/data that is necessary for the dashboard tiles
  @Input() tileData: Project;

 lastTraining: Training;

  constructor() { }

  ngOnInit() {
    this.lastTraining = this.tileData.trainings[this.tileData.trainings.length-1];
  }

}
