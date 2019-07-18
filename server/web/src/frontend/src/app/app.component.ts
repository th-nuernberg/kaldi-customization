import { Component } from '@angular/core';
import { PetService, Pet } from 'swagger-client';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less']
})
export class AppComponent {
  constructor(petService: PetService) {
    petService
      .addPet({
        name: "Test",
        photoUrls: ["about:blank"]})
      .subscribe(console.log);
  }
}
