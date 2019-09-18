import { Injectable } from '@angular/core';
import { Configuration } from '../projects/swagger-client/src';

@Injectable({
  providedIn: 'root'
})
export class IdentityService {

  constructor() { }

  static getApiConfiguration(): Configuration {
    return new Configuration(
      {
        basePath: "/api/v1",
        username: "kaldi3",
        password: "valid",
        accessToken: "bokvORLZjjHCG7AEQ1oumFHBRHHopsDStsMUvKgSMd",
    });
  }
}
