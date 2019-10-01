import { Injectable } from '@angular/core';
import { Configuration } from 'swagger-client';

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
