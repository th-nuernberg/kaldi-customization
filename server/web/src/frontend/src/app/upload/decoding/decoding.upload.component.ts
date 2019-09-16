import { Observable } from 'rxjs';
import {Component, OnInit} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { SelectionModel } from '@angular/cdk/collections';
import { MatTableDataSource } from '@angular/material/table';
import { MatSnackBar } from '@angular/material';
import {
  Audio,
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
  audios$:Observable<Array<Audio>>;

  currentAudios:Audio[];
  allAudios:MatTableDataSource<Audio>;

  displayedColumns:string[] = ['select', 'name'];

  public historySelection = new SelectionModel<Audio>(true, []);

  constructor(
    private route: ActivatedRoute,
    private decodeService: DecodeService,
    private trainingService: TrainingService,
    private resourceService: ResourceService,
    private projectService: ProjectService,
    private snackBar: MatSnackBar) {}

  ngOnInit() {
    this.currentAudios = [];

    this.projectUuid = this.route.snapshot.paramMap.get('uuid');
    this.trainingVersion =  +this.route.snapshot.paramMap.get('id');

    // init obeservables
    this.training$ = this.trainingService.getTrainingByVersion(this.projectUuid, this.trainingVersion);
    this.project$ = this.projectService.getProjectByUuid(this.projectUuid);
    //this.resources$ = this.resourceService.getResource();
    this.audios$ = new Observable<Array<Audio>>();//this.decodeService.getAllAudio();

    // TODO: get audio files that are added to a decode
    this.audios$.subscribe(audios => {
      console.log(audios);
       this.currentAudios = [];
       this.allAudios = new MatTableDataSource<Audio>();
    })

  }

/** Whether the number of selected elements matches the total number of rows. */
  isAllSelected() {
    const numSelected = this.historySelection.selected.length;
    const numRows = this.allAudios.data.length;
    return numSelected === numRows;
  }

  /** Selects all rows if they are not all selected; otherwise clear selection. */
  masterToggle() {
    this.isAllSelected() ?
        this.historySelection.clear() :
        this.allAudios.data.forEach(row => this.historySelection.select(row));
  }

  /** The label for the checkbox on the passed row */
  checkboxLabel(row?: Resource): string {
    if (!row) {
      return "${this.isAllSelected() ? 'select' : 'deselect'} all";
    }

    return "${this.historySelection.isSelected(row) ? 'deselect' : 'select'} row ${row}";
  }

  // copies selected history elements to current panel
  copyAudio() {
    this.historySelection.selected.forEach(audio => {
      this.currentAudios.push(audio);
      console.log("Assgin resource: " + audio.uuid + "Name: " + audio.name + " to Decode");
      // TODO: change to assignAudioToDecode()
      /*this.trainingService.assignResourceToTraining(
        this.projectUuid,
        this.trainingVersion,
        { resource_uuid: resource.uuid })
      .subscribe(this.currentTrainingResources.push);*/
    });

    this.snackBar.open("Kopiere Audio Datein ins aktuelle Decoding...", "", { duration: 3000 });
  }

  // removes selected training resources
  remove(selectedAudio) {

    selectedAudio.forEach(item => {
      const audio:Audio = item.value;
      let index:number = this.currentAudios.findIndex(d => d === audio);

      if(index > -1) {
        // TODO deleteAssignedResourceFromTraining
        this.decodeService.deleteAudioByUuid(
          audio.uuid
        ).subscribe(r => {
          console.log("Removed audio: " + r.name + " from decode");
          this.currentAudios.splice(index, 1);
        });
      }
    });

    this.snackBar.open("Lösche Audio Datei vom aktuelle Decoding...", "", { duration: 3000 });
  }

  // uploads file and show preview
  loadFile(file:HTMLInputElement) {
    this.uploadAudio(file);
  }

  uploadAudio(file) {
    console.log("Uploaded audio: " + file.files[0].name);
    const blobFile:Blob = file.files[0] as Blob;

    this.decodeService.uploadAudio(blobFile)
      .subscribe(audio => {
        // TODO assign audio to decode!!!
    });
    // creates resource and starts the TextPrepWorker to create the corupus
    /*this.resourceService.createResource(blobFile)
      .subscribe(resource => {
        console.log("Created Resource: " + resource.uuid);
        this.currentTrainingResources.push(resource);
        //console.log("Assgin resource: " + resource.uuid + "Name: " + resource.name + " to training: " + this.trainingVersion);
        this.trainingService.assignResourceToTraining(
          this.projectUuid,
          this.trainingVersion,
          { resource_uuid: resource.uuid })
        .subscribe(this.currentTrainingResources.push);
    });*/

    this.snackBar.open("Lade Audio Datei hoch...", "", { duration: 3000 });
  }

  reloadProject() {
    //console.log("Reload values on next..");
    this.project$ = this.projectService.getProjectByUuid(this.projectUuid);
    this.training$ = this.trainingService.getTrainingByVersion(this.projectUuid, this.trainingVersion);
  }
}
