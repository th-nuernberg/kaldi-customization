import { Component, OnInit } from '@angular/core';

import { TileData } from './tile/tile-data';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.less']
})
export class DashboardComponent implements OnInit {

  gridTiles: TileData[];
  maxCols: 4;

  constructor(){}

  ngOnInit() {
    this.gridTiles = [];
  }
  
  newProject() {
    this.gridTiles.push( 
        {
          projectName: "Foobar",
          projectNumber: this.gridTiles.length + 1,
          comments: "Bla bla bla",
          status: "What happened?",
          cols: 1,
          rows: 1,
        });
  }
}
