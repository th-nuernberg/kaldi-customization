import { Component, OnInit } from '@angular/core';
import { SelectionModel } from '@angular/cdk/collections';
import { MatTableDataSource } from '@angular/material/table';

export interface HistoryFile {
  name: string;
  position: number;
  uploaded: string;
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
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.less'],
})

export class UploadComponent implements OnInit {

  private fileContent;

  public show:boolean = false;
  public displayedColumns: string[] = ['select', 'position', 'name', 'uploaded'];

  public dataSource = new MatTableDataSource<HistoryFile>(FILE_DATA);
  public historySelection = new SelectionModel<HistoryFile>(true, []);
  public currentSelection = new SelectionModel<string>(true, [])
  public currentFiles: string[] = [];
  public uploadedFiles : { name: string, selected: boolean; }[] = [];

  constructor() {
  }

  ngOnInit() {
  }

  // enables single selection for current panel list
  handleSelection(event, file) {
    // TODO: show and clean preview content of selected file
    console.log(event);
    if (event.option.selected) {
      event.source.deselectAll();      
      event.option._setSelected(true);      
      this.showPreview(file);
    }
    else {
      this.fileContent = null;
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
  remove(files:any) {
    // TODO: find more generic solution
    files.selectedOptions.selected.forEach(file => this.uploadedFiles.splice(this.uploadedFiles.indexOf(file)));
  }

  // toggles remove button (disabled if nothing is selected)
  isRemoveDisabled(files:any) {
    // TODO find more generic solution
    return files.selectedOptions.selected.length === 0;
  }

  // toggles save button (dummy disabled, should be enabled if text changed)
  shouldSave() {
    // TODO toggles, when user changed the content of the selected file
    return true;
  }

  // uploads file and show preview
  loadFile(file:HTMLInputElement, list:any) {

    // TODO: API - TPW Results as uploaded files in current file list
    this.sendFileToAPI();
    let api_result = this.getResultFromAPI();
    this.dummyShowUploadedFile(file, list)

    // loads content of uploaded file into preview
    this.showPreview(file)
    this.show = false;
  }

  sendFileToAPI() {}
  getResultFromAPI() {}

  dummyShowUploadedFile(file, list) {
    let fileName = file.files[0].name;
    // add uploaded file to current file list
    this.uploadedFiles.push({ name:fileName, selected:true });

    // selects element in current panel
    this.currentFiles = list.selectedOptions.selected.map(item => item.value);
    this.currentFiles.push(fileName);
  }

  // toggles start and verify button in current panel
  toggle() {
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
