import { Component, OnInit, Input } from '@angular/core';
import { TileData } from './tile-data';

@Component({
  selector: 'app-tile',
  templateUrl: './tile.component.html',
  styleUrls: ['./tile.component.css']
})
export class TileComponent implements OnInit {

  @Input() tileData: TileData;

  constructor() { }

  ngOnInit() {
  }

}