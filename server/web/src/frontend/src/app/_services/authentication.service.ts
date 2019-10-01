import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { map, concatMap } from 'rxjs/operators';

import { User, UserService } from 'swagger-client';
import { IdentityService } from 'src/identity.service';
import { Router } from '@angular/router';

@Injectable({ providedIn: 'root' })
export class AuthenticationService {
    private currentUserSubject: BehaviorSubject<User>;
    public currentUser: Observable<User>;

    constructor(
        private router: Router,
        private userService: UserService) {
        try {
            this.currentUserSubject = new BehaviorSubject<User>(JSON.parse(localStorage.getItem('currentUser')));
            this.currentUser = this.currentUserSubject.asObservable();
            IdentityService.config.accessToken = this.currentUserSubject.value['token'];
        } catch {}

        this.userService.getUser().toPromise()
            .catch(_ => this.logout());
    }

    public get currentUserValue(): User {
        return this.currentUserSubject.value;
    }

    public get currentToken(): string {
        if (this.currentUserSubject.value) {
            return (<object>this.currentUserSubject.value)['token'];
        } else {
            return '';
        }
    }

    login(username: string, password: string) {
        return this.userService.loginUser(username, password)
                .pipe(concatMap(token => {
                    IdentityService.config.accessToken = token;

                    return this.userService.getUser().pipe(map(user => {
                        user['token'] = token;
                        localStorage.setItem('currentUser', JSON.stringify(user));
                        this.currentUserSubject.next(user);
                    }));
                }));
    }

    logout() {
        const _logout = () => {
            // remove user from local storage to log user out
            localStorage.removeItem('currentUser');
            this.currentUserSubject.next(null);
            this.router.navigate(['/login'], { queryParams: { returnUrl: this.router.url }});
        }

        if (this.currentToken) {
            this.userService.logoutUser(this.currentToken).subscribe(() => {
                _logout();
            });
        } else {
            _logout();
        }
    }
}