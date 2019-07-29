import { Component, OnInit, Input } from '@angular/core';
import { TileData, ModelData } from './tile-data';

@Component({
  selector: 'app-tile',
  templateUrl: './tile.component.html',
  styleUrls: ['./tile.component.css']
})
export class TileComponent implements OnInit {
  // TODO check for future details/data that is necessary for the dashboard tiles
  @Input() tileData: TileData;

  constructor() { }

  ngOnInit() {
  }

}