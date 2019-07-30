import { Component, OnInit } from '@angular/core';
import { SelectionModel } from '@angular/cdk/collections';
import { MatTableDataSource } from '@angular/material/table';

export interface HistoryFile {
  name: string;
  position: number;
  uploaded: string;
}

export interface FileDetails {
  project: number,
  model: number,
  numberFilesName: string;
  numberFiles: number;
  numberSentencesName: string;
  numberSentences: number;
  numberWordsName: string;
  numberWords: number;
}

// TODO: adapt to information from database
const FILE_DATA: HistoryFile[] = [
  {position: 1, name: 'Kafka1', uploaded: "01.01.1970"},
  {position: 2, name: 'Kant1', uploaded: "01.01.1970"},
  {position: 3, name: 'Text', uploaded: "01.01.1970"},
  {position: 4, name: 'Portal', uploaded: "01.01.1970"},
];

@Component({
  selector: 'app-dashboard',
  templateUrl: './decoding.upload.component.html',
  styleUrls: ['./decoding.upload.component.less'],
})

export class DecodingUploadComponent implements OnInit {

  private fileContent;

  public show:boolean = false;
  public showContentPreview:boolean = false;

  public displayedColumns: string[] = ['select', 'position', 'name', 'uploaded'];

  public dataSource = new MatTableDataSource<HistoryFile>(FILE_DATA);
  public historySelection = new SelectionModel<HistoryFile>(true, []);
  
  public currentFiles: string[] = [];
  public uploadedFiles : { name: string, selected: boolean; }[] = [];

  constructor() {
  }
  // TODO post model information to the API: text files, project name, model name, prev model etc..
  ngOnInit() {
    this.fileContent = "";
    this.showContentPreview = false;
  }

  fileDetails: FileDetails[] = [
    { project: 815, model: 1337, numberFilesName: "Anzahl Dateien: ", numberFiles: 5, numberSentencesName: "Anzahl Sätze: ", numberSentences: 100, numberWordsName: "Anzahl Wörter: ", numberWords: 5000 }
  ]

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

      //if(file !== null) {
        //this.showPreview(file);
        this.showContentPreview = true;
      //}
      
    }
    else {
      this.fileContent = null;
      this.showContentPreview = false;

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

  /** Whether the number of selected elements matches the total number of rows. */
  isAllSelected() {
    const numSelected = this.historySelection.selected.length;
    const numRows = this.dataSource.data.length;
    return numSelected === numRows;
  }

  /** Selects all rows if they are not all selected; otherwise clear selection. */
  masterToggle() {
    this.isAllSelected() ?
        this.historySelection.clear() :
        this.dataSource.data.forEach(row => this.historySelection.select(row));
  }

  /** The label for the checkbox on the passed row */
  checkboxLabel(row?: HistoryFile): string {
    if (!row) {
      return `${this.isAllSelected() ? 'select' : 'deselect'} all`;
    }
    return `${this.historySelection.isSelected(row) ? 'deselect' : 'select'} row ${row.position + 1}`;
  }

  // copies selected history elements to current panel
  copy() {
    // TODO: do not copy text files only unique_word_list and corpuses
    this.historySelection.selected.forEach(file => {
      if(!this.uploadedFiles.includes( { name:file.name, selected:true }))
      {
        this.uploadedFiles.push({ name:file.name, selected:false });

        this.currentFiles = this.uploadedFiles
        .filter(item => item.selected)
        .map(item => item.name);
      }
    });
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

    // loads content of uploaded file into preview
    if(file !== null) {
      this.showPreview(file);
    }
    this.show = false;
  }

  dummyShowUploadedFile(file) {
    let fileName = file.files[0].name;
    // add uploaded file to current file list
    this.uploadedFiles.push({ name:fileName, selected:true });
    
    // selects element in current panel
    this.currentFiles.push(fileName);
    this.currentFiles = this.uploadedFiles.map(item => item.name);
  }

  // toggles start and verify button in current panel
  toggleSave() {
    this.show = !this.show;
  }

  showPreview(file:any) {
    // loads content of uploaded file into preview
    var reader = new FileReader();
    var me = this;
    
    reader.readAsText(file.files[0]);
    reader.onload = function () {
      me.fileContent = reader.result;
    }
  }
}
