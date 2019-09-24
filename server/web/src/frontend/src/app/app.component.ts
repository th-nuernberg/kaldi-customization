import { Component } from '@angular/core';
import { UserService, ProjectService, User } from 'swagger-client';
import { AuthenticationService } from './_services';
import { Router } from '@angular/router';
import { MatSnackBarConfig } from '@angular/material';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less']
})
export class AppComponent {
  currentUser: User;

  constructor(
    private router: Router,
    private userService: UserService,
    private projectService: ProjectService,
    private authenticationService: AuthenticationService) {
      this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
  }

  logout() {
      this.authenticationService.logout();
      this.router.navigate(['/login']);
  }
}

export default class AppConstants {
  public static snackBarConfig: MatSnackBarConfig = {
    duration: 2000,
    verticalPosition: 'top'
  };
}
