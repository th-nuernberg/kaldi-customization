import { Injectable } from '@angular/core';
import { Configuration } from '../projects/swagger-client/src';

@Injectable({
  providedIn: 'root'
})
export class IdentityService {

  constructor() { }

  static config = new Configuration({ basePath: "/api/v1" });

  static getApiConfiguration(): Configuration {
    return IdentityService.config;
  }
}
