import { Component, OnInit } from '@angular/core';

import { TileData } from './tile/tile-data';

export interface TrainingModel {
  name:string;
  value: string;
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.less']
})
export class DashboardComponent implements OnInit {
  // TODO: add function to load existing projects/models on component init!
  // TODO: implement API calls: get Project, Post Project

  gridTiles: TileData[];
  maxCols: 4;
  newProjectName: string;

  selectedPrevTrain: string;
  prevTrainedModels: TrainingModel[] = [
    { name: "Default Kaldi", value: "default" },
    { name: "Kaldi 1", value: "advanced" },
    { name: "Kaldi 2", value: "advanced" },
  ];

  constructor(){}

  ngOnInit() {
    this.gridTiles = [];
    this.selectedPrevTrain = "";
    this.newProjectName = "";
  }
  
  onKey(event) {
    this.newProjectName = event.target.value;
  }

  newProject() {
    // TODO: New Project should create a new model automatically
    // TODO: Opens automatically the model overview

    let index = Math.floor(Math.random() * 3) + 1
    let rndStatus = "What happened?";
    console.log(this.newProjectName);
    if(index === 1) {
      rndStatus = "Running";
    }
    else {
      rndStatus = "Done";
    }

    if(this.newProjectName === "") {
      this.newProjectName = "Project name placeholder ";
    }

    if(this.selectedPrevTrain === "") {
      this.selectedPrevTrain = "Prev trained model placeholder";
    }

    this.gridTiles.push( 
        {
          projectName: this.newProjectName,
          projectNumber: this.gridTiles.length + 1,
          previousTrainedModel: this.selectedPrevTrain,
          comments: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
          status: rndStatus,
          cols: 1,
          rows: 1,
        });
  }
}
