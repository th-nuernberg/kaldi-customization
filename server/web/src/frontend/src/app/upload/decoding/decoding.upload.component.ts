import { Observable } from 'rxjs';
import {Component, OnInit} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { SelectionModel } from '@angular/cdk/collections';
import { MatTableDataSource } from '@angular/material/table';
import { MatSnackBar } from '@angular/material';
import {
  Audio,
  Project,
  Resource,
  Training,
  DecodeService,
  ProjectService,
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
    private router: Router,
    private decodeService: DecodeService,
    private trainingService: TrainingService,
    private projectService: ProjectService,
    private snackBar: MatSnackBar) {}

  ngOnInit() {
    this.currentAudios = [];

    this.projectUuid = this.route.snapshot.paramMap.get('uuid');
    this.trainingVersion =  +this.route.snapshot.paramMap.get('id');

    // init obeservables
    this.training$ = this.trainingService.getTrainingByVersion(this.projectUuid, this.trainingVersion);
    this.project$ = this.projectService.getProjectByUuid(this.projectUuid);
    this.audios$ = new Observable<Array<Audio>>(); //this.decodeService.getAllAudio();

    // TODO: get audio files that are added to a decode
    this.audios$.subscribe(audios => {
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
      this.snackBar.open("Kopiere Audio Datein in aktuelle Spracherkennung...", "", { duration: 3000 });
      /*this.decodeService.assign_audio_to_training(
        this.projectUuid,
        this.trainingVersion,
        { audio_uuid: audio.uuid }
      ).subscribe(this.currentAudios.push);*/
    });
  }

  // removes selected training resources
  remove(selectedAudio) {

    selectedAudio.forEach(item => {
      const audio:Audio = item.value;
      let index:number = this.currentAudios.findIndex(d => d === audio);

      if(index > -1) {
        this.decodeService.deleteAudioByUuid(
          audio.uuid
        ).subscribe(r => {

          this.currentAudios.splice(index, 1);
        });
      }
    });

    this.snackBar.open("Lösche Audio Datei von aktueller Spracherkennung...", "", { duration: 3000 });
  }

  playAudioData(audio) {
    let audioData:Blob;
    this.decodeService.getAudioData(audio.uuid)
      .subscribe(data => audioData = data);

    return audioData;
  }

  // uploads file and show preview
  loadFile(file:HTMLInputElement) {
    this.uploadAudio(file);
  }

  uploadAudio(file) {
    const blobFile:Blob = file.files[0] as Blob;

    this.decodeService.uploadAudio(blobFile)
      .subscribe(audio => {
        /*
        this.currentAudios.push(audio);
        this.decodeService.assignAudioToTraining(
        this.projectUuid,
        this.trainingVersion,
        { audio_uuid: audio.uuid }
      ).subscribe(this.currentAudios.push);*/
    });

    this.snackBar.open("Lade Audio Datei hoch...", "", { duration: 3000 });
  }

  startDecode() {
    this.decodeService.startDecode(
      this.projectUuid,
      this.trainingVersion,
      { audio_uuid: "" }
    ).subscribe(decode =>
      this.snackBar.open("Starte Spracherkennung", "", { duration: 3000 }));
      this.router.navigate(["/upload/training/overview/" + this.projectUuid + "/" + this.trainingVersion]);
  }

  reloadDecoding() {
    this.project$ = this.projectService.getProjectByUuid(this.projectUuid);
    this.training$ = this.trainingService.getTrainingByVersion(this.projectUuid, this.trainingVersion);
  }
}
