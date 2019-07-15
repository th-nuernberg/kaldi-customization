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

  constructor() { }

  ngOnInit() {
  }

  currentFiles: string[] = [];
  displayedColumns: string[] = ['select', 'position', 'name', 'uploaded'];

  dataSource = new MatTableDataSource<HistoryFile>(FILE_DATA);
  selection = new SelectionModel<HistoryFile>(true, []);

  currentSelection = new SelectionModel<string>(true, [])

  /** Whether the number of selected elements matches the total number of rows. */
  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.dataSource.data.length;
    return numSelected === numRows;
  }

  /** Selects all rows if they are not all selected; otherwise clear selection. */
  masterToggle() {
    this.isAllSelected() ?
        this.selection.clear() :
        this.dataSource.data.forEach(row => this.selection.select(row));
  }

  /** The label for the checkbox on the passed row */
  checkboxLabel(row?: HistoryFile): string {
    if (!row) {
      return `${this.isAllSelected() ? 'select' : 'deselect'} all`;
    }
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.position + 1}`;
  }

  copy() {
    this.selection.selected.forEach(file => {
       if(!this.currentFiles.includes(file.name)) this.currentFiles.push(file.name);
    });
  }

  remove(files:SelectionModel<string>) {
    files.selected.forEach(file => this.currentFiles.splice(this.currentFiles.indexOf(file)))
  }

  isRemoveDisabled(files:SelectionModel<string>) {
    return files.selected.length === 0;
  }

  loadFile(file: HTMLInputElement) {
    console.log(file);
    let fileName = file.files[0].name;
    this.currentFiles.push(fileName);

    var reader = new FileReader();
    reader.readAsText(file.files[0]);
    var me = this;
    reader.onload = function () {
      me.fileContent = reader.result;
    }
  }
}
