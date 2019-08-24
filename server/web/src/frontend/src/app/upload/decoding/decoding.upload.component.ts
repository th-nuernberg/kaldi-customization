import { Observable } from 'rxjs';
import {Component, OnInit} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { SelectionModel } from '@angular/cdk/collections';
import { MatSnackBar } from '@angular/material';
import {
  DecodeMessage,
  Project,
  Resource,
  Training,
  DecodeService,
  ProjectService,
  ResourceService,
  TrainingService,
} from 'swagger-client'

@Component({
  selector: 'app-dashboard',
  templateUrl: './decoding.upload.component.html',
  styleUrls: ['./decoding.upload.component.less'],
})
export class DecodingUploadComponent implements OnInit {
  projectUuid: string;
  trainingVersion: number;

  project$:Observable<Project>;
  training$:Observable<Training>;
  //resources$:Observable<Array<Resource>>;
  decodings$:Observable<Array<DecodeMessage>>;

  currentDecodingResources:Blob[];
  
  constructor(
    private route: ActivatedRoute,
    private decodeService: DecodeService,
    private trainingService: TrainingService,
    private resourceService: ResourceService,
    private projectService: ProjectService,
    private snackBar: MatSnackBar) {}

  ngOnInit() {
    this.projectUuid = this.route.snapshot.paramMap.get('uuid');
    this.trainingVersion =  +this.route.snapshot.paramMap.get('id');

    // init obeservables
    this.training$ = this.trainingService.getTrainingByVersion(this.projectUuid, this.trainingVersion);
    this.project$ = this.projectService.getProjectByUuid(this.projectUuid);
    //this.resources$ = this.resourceService.getResource();
    this.decodings$ = this.decodeService.getDecodings(
      this.projectUuid,
      this.trainingVersion);

    this.currentDecodingResources = [];
  }

  // removes selected history elements
  remove(selectedResources) {

    selectedResources.forEach(item => {
      const resource:Blob = item.value;
      let index:number = this.currentDecodingResources.findIndex(d => d === resource);

      if(index > -1) {
          console.log("Removed resource: " + this.currentDecodingResources[index] + " from decoding: " + this.projectUuid);
          this.currentDecodingResources.splice(index, 1);
      }
    });

    this.snackBar.open("Removed resource from training...", "", { duration: 3000 });
  }

  // uploads file and show preview
  loadFile(file:HTMLInputElement) {
    this.uploadAudio(file);
  }

  uploadAudio(file) {
    console.log("Uploaded audio: " + file.files[0].name);
    const audioFile:Blob = file.files[0] as Blob;

    this.decodeService.startDecode(
      this.projectUuid,
      this.trainingVersion,
      audioFile);

    this.currentDecodingResources.push(audioFile);
    this.snackBar.open("Start audio decoding...", "", { duration: 3000 });
  }

  reloadProject() {
    //console.log("Reload values on next..");
    this.project$ = this.projectService.getProjectByUuid(this.projectUuid);
    this.training$ = this.trainingService.getTrainingByVersion(this.projectUuid, this.trainingVersion);
    this.decodings$ = this.decodeService.getDecodings(this.projectUuid, this.trainingVersion);
    let decodingResults = this.decodeService.getDecodeResult(this.projectUuid, this.trainingVersion, "")
  }
}