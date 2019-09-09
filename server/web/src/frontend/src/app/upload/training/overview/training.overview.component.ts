import { Observable } from 'rxjs';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';


@Component({
  selector: 'app-dashboard',
  templateUrl: './training.overview.component.html',
  styleUrls: ['./training.overview.component.less'],
})

export class TrainingOverviewComponent implements OnInit {


  constructor(
    ) {}
  ngOnInit() {
  }

  ngOnDestroy() {
  }
}
