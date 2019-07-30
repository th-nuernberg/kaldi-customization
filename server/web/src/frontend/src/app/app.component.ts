import { Component } from '@angular/core';
import { UserService, ProjectService } from '../../projects/swagger-client/src';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less']
})
export class AppComponent {
  constructor(userService: UserService, projectService: ProjectService) {
    
  }
}
