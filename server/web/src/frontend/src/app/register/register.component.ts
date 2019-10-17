import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

import { AlertService, AuthenticationService } from '../_services';
import { User, UserService } from 'swagger-client';

@Component({
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.less']
})
export class RegisterComponent implements OnInit {
    registerForm: FormGroup;
    loading = false;
    submitted = false;
    returnUrl: string;
    errorMessage: string;

    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private authenticationService: AuthenticationService,
        private userService: UserService
    ) {
        // redirect to home if already logged in
        if (this.authenticationService.currentUserValue) {
            this.router.navigate(['/dashboard']);
        }
    }

    ngOnInit() {
        this.registerForm = this.formBuilder.group({
            username: ['', Validators.required],
            email: ['', [Validators.required, Validators.email]],
            password: ['', Validators.required]
        });

        // get return url from route parameters or default to '/'
        this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/login';
    }

    // convenience getter for easy access to form fields
    get f() { return this.registerForm.controls; }

    /**
     * Registers a new user.
     */
    onSubmit() {
        this.submitted = true;

        // stop here if form is invalid
        if (this.registerForm.invalid) {
            return;
        }

        this.loading = true;
        this.userService.createUser({
            username: this.f.username.value,
            email: this.f.email.value,
            password: this.f.password.value,
        })
            .pipe(first())
            .subscribe(
                data => {
                    this.router.navigate([this.returnUrl]);
                },
                error => {
                    this.errorMessage = 'Benutzername oder Email schon vergeben';
                    this.loading = false;
                });
    }
}
