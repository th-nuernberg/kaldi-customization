import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';

export interface Environment {
  project: number;
  model: number;
  prevModel: string;
  modelStatus: string,
  date: string,
  numberAudio: number;
  listAudio: string[]
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './decoding.upload.component.html',
  styleUrls: ['./decoding.upload.component.less'],
})
export class DecodingUploadComponent implements OnInit {
  firstFormGroup: FormGroup;
  secondFormGroup: FormGroup;
  
  environment: Environment[] = [
    { 
      project: 1,
      model: 4,
      prevModel: "default",
      modelStatus: "Done",
      date: "01.07.1970",
      numberAudio: 1,
      listAudio: [ "foo.wav" ],
    },
  ];

  public currentFiles: string[] = [];
  public uploadedFiles : { name: string, selected: boolean; }[] = [];

  constructor(private _formBuilder: FormBuilder) {}

  ngOnInit() {
    this.firstFormGroup = this._formBuilder.group({
      firstCtrl: ['', Validators.required]
    });
    this.secondFormGroup = this._formBuilder.group({
      secondCtrl: ['', Validators.required]
    });
  }

  // enables single selection for current panel list
  handleSelection(event) {
    // TODO: show and clean preview content of selected file
    console.log(event);
    if (event.option.selected) {
      event.source.deselectAll();      
      event.option._setSelected(true);

      // update select in uploaded file list
      let selectedItemName: string;
      event.source.selectedOptions.selected.forEach(s => {
        if (s.selected === true) {
          selectedItemName = s.value;
        }
      });

      this.uploadedFiles.forEach(f => {
        if(f.name === selectedItemName) {
          f.selected = true;
        }
      });
    }
    else {
      // update deselect in uploaded file list
      let selectedItemName: string;
      event.source.selectedOptions.selected.forEach(s => {
        if (s.selected === false) {
          selectedItemName = s.value;
        }
      });

      this.uploadedFiles.forEach(f => {
        if(f.name === selectedItemName) {
          f.selected = false;
        }
      });
    }
  }

  // removes selected history elements
  remove() {
    let delecteCount = 1;
    this.uploadedFiles.forEach(file => {      
      if(file.selected === true) {
        let index = this.uploadedFiles.indexOf(file);
        console.log("Name: " + file.name + " selected: " + file.selected + " Index: " + index);
        this.uploadedFiles.splice(index, delecteCount);
      }
    });
  }

  // toggles remove button (disabled if nothing is selected)
  isRemoveDisabled() {
    // return true => disables button | return false => enables button
    let isDisabled: Boolean = true;
    this.uploadedFiles.forEach(file => {
        if(file.selected === true) {
        isDisabled = false; 
      } 
    });

    return isDisabled;
  }

  // uploads file and show preview
  loadFile(file:HTMLInputElement) {

    // TODO: API - TPW Results as uploaded files in current file list
    this.dummyShowUploadedFile(file);
  }

  dummyShowUploadedFile(file) {
    let fileName = file.files[0].name;
    // add uploaded file to current file list
    this.uploadedFiles.push({ name:fileName, selected:true });
    
    // selects element in current panel
    this.currentFiles.push(fileName);
    this.currentFiles = this.uploadedFiles.map(item => item.name);
  }

}