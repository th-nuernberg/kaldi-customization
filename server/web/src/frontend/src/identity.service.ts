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
        username: "kaldi",
        password: "valid",
        accessToken: "qprh9NFxUPowrosvoXsTn7nEGkKESFiLlApkCBuPwO"
    });
  }
}
