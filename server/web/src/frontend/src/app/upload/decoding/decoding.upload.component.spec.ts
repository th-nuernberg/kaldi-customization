import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DecodingUploadComponent } from './decoding.upload.component';

describe('DecodingUploadComponent', () => {
  let component: DecodingUploadComponent;
  let fixture: ComponentFixture<DecodingUploadComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DecodingUploadComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DecodingUploadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
