import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TrainingUploadComponent } from './training.upload.component';

describe('TrainingUploadComponent', () => {
  let component: TrainingUploadComponent;
  let fixture: ComponentFixture<TrainingUploadComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TrainingUploadComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TrainingUploadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
