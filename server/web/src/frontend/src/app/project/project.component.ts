import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

export interface TrainingsModel {
  name: string;
  fileResultName: string;
  date: string;
  link: string;
  texte: string;
}

@Component({
  selector: 'app-project',
  templateUrl: './project.component.html',
  styleUrls: ['./project.component.less']
})
export class ProjectComponent implements OnInit {
  uuid: string;

  /* TODO
    - create new model +  open model view
    - get user data
    - get project/model information -> using an existing model
    - get status of project / model training
    - provide direct file download: model & decoded text
    - provide detailed model info
  */

  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
    this.uuid = this.route.snapshot.paramMap.get('uuid');
  }

  models: TrainingsModel[] =  [
    {
      name: "Model 1",
      fileResultName: "model1.pdf",
      date: "01.01.1970",
      link: "/upload/_",
      texte: "Reißverschlussverfahren"
    },
    {
      name: "Model 2",
      fileResultName: "model2.pdf",
      date: "01.01.1970",
      link: "/upload/_",
      texte: "Bla bla bla Mr. Freeman"
    },
    {
      name: "Model 3",
      fileResultName: "model3.pdf",
      date: "01.01.1970",
      link: "/upload/_",
      texte: "Moin moin und Hallo!"
    }
  ];

}
