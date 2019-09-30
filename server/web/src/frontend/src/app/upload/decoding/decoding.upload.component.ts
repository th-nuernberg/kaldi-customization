import { Observable } from 'rxjs';
import {Component, OnInit, ViewChild} from '@angular/core';
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
  DecodeSession
} from 'swagger-client'
import AppConstants from  '../../app.component';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-dashboard',
  templateUrl: './decoding.upload.component.html',
  styleUrls: ['./decoding.upload.component.less'],
})
export class DecodingUploadComponent implements OnInit {

  projectUuid: string;
  trainingVersion: number;
  decodeSessionUuid: string;

  project$:Observable<Project>;
  training$:Observable<Training>;
  audios$:Observable<Array<Audio>>;
  decodeSession$: Observable<DecodeSession>;

  currentAudios:Array<Audio>;
  allAudios:MatTableDataSource<Audio>;

  displayedColumns:Array<string> = ['select', 'name'];

  currentlyPlayingAudio? : {
    audio: Audio,
    data: string
  } = null;
  @ViewChild('audioPlayer') audioPlayer;

  public historySelection = new SelectionModel<Audio>(true, []);

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private sanitizer:DomSanitizer,
    private decodeService: DecodeService,
    private trainingService: TrainingService,
    private projectService: ProjectService,
    private snackBar: MatSnackBar) {}

  ngOnInit() {
    this.currentAudios = [];

    this.projectUuid = this.route.snapshot.paramMap.get('puuid');
    this.trainingVersion =  +this.route.snapshot.paramMap.get('id');
    this.decodeSessionUuid = this.route.snapshot.paramMap.get('duuid');

    // init obeservables
    this.training$ = this.trainingService.getTrainingByVersion(this.projectUuid, this.trainingVersion);
    this.project$ = this.projectService.getProjectByUuid(this.projectUuid);
    this.audios$ = this.decodeService.getAllAudio();
    this.decodeSession$ = this.decodeService.getDecodeSession(this.projectUuid, this.trainingVersion, this.decodeSessionUuid);

    this.audios$.subscribe(audios => {
      this.allAudios = new MatTableDataSource<Audio>(audios);
    })

  }

  audioData() {
    if (!this.currentlyPlayingAudio)
      return null;

    return this.sanitizer.bypassSecurityTrustResourceUrl(this.currentlyPlayingAudio.data);
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
    this.historySelection.selected.forEach(selectedAudio => {
      this.snackBar.open("Kopiere Audio Datein in aktuelle Spracherkennung...", "", AppConstants.snackBarConfig);
      console.log("Assgin audio to decode");
      this.decodeService.assignAudioToCurrentSession(
        this.projectUuid,
        this.trainingVersion,
        { audio_uuid: selectedAudio.uuid }
      ).subscribe(decodeAudio => {
        if(this.currentAudios.indexOf(selectedAudio) !== -1) {
          return;
        }
        console.log("Copy assigned audio");
        this.currentAudios.push(selectedAudio);
      });
    });
  }

  // removes selected training resources
  remove(selectedAudio) {

    selectedAudio.forEach(item => {
      const audio:Audio = item.value;
      let index:number = this.currentAudios.findIndex(d => d === audio);

      if(index > -1) {
        this.decodeService.unassignAudioToCurrentSession(
          this.projectUuid,
          this.trainingVersion,
          audio.uuid
        ).subscribe(r => {
          this.currentAudios.splice(index, 1);
        });
      }
    });

    this.snackBar.open("Lösche Audio Datei von aktueller Spracherkennung...", "", AppConstants.snackBarConfig);
  }

  triggerAudio(event, audio) {
    event.stopPropagation();

    if (this.isPlaying(audio)) {
      this.currentlyPlayingAudio = null;
    } else {
      this.decodeService.getAudioData(audio.uuid)
        .subscribe(data => {
          const audioData = URL.createObjectURL(data);
          if (this.currentlyPlayingAudio) {
            URL.revokeObjectURL(this.currentlyPlayingAudio.data);
          }

          this.currentlyPlayingAudio = {
            audio: audio,
            data: audioData
          };

          setTimeout(() => this.audioPlayer.nativeElement.play(), 0);
        });
      }
  }

  stopAudio() {
    this.currentlyPlayingAudio = null;
  }

  isPlaying(audio: Audio) {
    return (this.currentlyPlayingAudio && this.currentlyPlayingAudio.audio.uuid == audio.uuid);
  }

  // uploads file and show preview
  loadFile(file:HTMLInputElement) {
    this.uploadAudio(file);
  }

  uploadAudio(file) {
    const blobFile:Blob = file.files[0] as Blob;

    this.decodeService.uploadAudio(blobFile)
      .subscribe(audio => {
        this.decodeService.assignAudioToCurrentSession(
        this.projectUuid,
        this.trainingVersion,
        { audio_uuid: audio.uuid }
      ).subscribe(decodeAudio => {
        if(this.currentAudios.indexOf(audio) !== -1) {
          return;
        }

        this.currentAudios.push(audio)
      });
    });

    this.snackBar.open("Lade Audio Datei hoch...", "", AppConstants.snackBarConfig);
  }

  startDecode() {
    this.currentAudios.forEach(decodeAudio => {
      this.decodeService.startDecode(
        this.projectUuid,
        this.trainingVersion,
        this.decodeSessionUuid
      ).subscribe(session => {
        this.snackBar.open("Starte Spracherkennung", "", AppConstants.snackBarConfig);
        this.router.navigate(["/upload/decoding/overview/" + this.projectUuid + "/" + this.trainingVersion + "/" + this.decodeSessionUuid]);
      });
    })
  }

  async reloadDecoding() {
    await this.copyAudio();

    this.project$ = this.projectService.getProjectByUuid(this.projectUuid);
    this.training$ = this.trainingService.getTrainingByVersion(this.projectUuid, this.trainingVersion);
  }
}
