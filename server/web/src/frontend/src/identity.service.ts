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
        username: "kaldi2",
        password: "valid",
        accessToken: "LKBs0c2dmP9AqZgYMDso4eZLVz1yfyaHKRTjCxITYj",
    });
  }
}
