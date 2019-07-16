import { Component, OnInit } from '@angular/core';
import { SelectionModel } from '@angular/cdk/collections';
import { MatTableDataSource } from '@angular/material/table';

export interface HistoryFile {
  name: string;
  position: number;
  uploaded: string;
}

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
    this.historySelection.selected.forEach(file => {
       //if(!this.currentFiles.includes(file.name)) this.currentFiles.push(file.name);
       if(!this.uploadedFiles.includes( { name:file.name, selected:true }))
       {
         this.uploadedFiles.push({ name:file.name, selected:true });

         this.currentFiles = this.uploadedFiles
          .filter(item => item.selected)
          .map(item => item.name);
       }
    });
  }

  // removes selected history elements
  remove(files:any) {
    //files.selectedOptions.selected.forEach(file => this.currentFiles.splice(this.currentFiles.indexOf(file)))

    files.selectedOptions.selected.forEach(file => this.uploadedFiles.splice(this.uploadedFiles.indexOf(file)))
  }

  // toggles remove button (disabled if nothing is selected)
  isRemoveDisabled(files:any) {
    return files.selectedOptions.selected.length === 0;
  }

  // toggles save button (dummy disabled, should be enabled if text changed)
  shouldSave() {
    return true;
  }

  /*  loads file from file dialog into current panel
      loads file text into preview
      pre-selects uploaded file in current panel
  */
  loadFile(file:HTMLInputElement, list:any) {

    let fileName = file.files[0].name;
    // add uploaded file to current file list
    this.uploadedFiles.push({ name:fileName, selected:true });

    // selects element in current panel
    this.currentFiles = list.selectedOptions.selected.map(item => item.value);
    this.currentFiles.push(fileName);

    // loads content of uploaded file into preview
    var reader = new FileReader();
    reader.readAsText(file.files[0]);
    var me = this;
    reader.onload = function () {
      me.fileContent = reader.result;
    }

    this.show = false;
  }

  // toggles start and verify button in current panel
  toggle() {
    this.show = !this.show;
  }
}
