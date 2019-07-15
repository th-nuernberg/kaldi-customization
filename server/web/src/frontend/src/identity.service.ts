import { Injectable } from '@angular/core';
import { Configuration } from 'swagger-client';

@Injectable({
  providedIn: 'root'
})
export class IdentityService {

  constructor() { }

  static getApiConfiguration(): Configuration {
    return new Configuration({
      apiKeys: {
      },
    });
  }
}
