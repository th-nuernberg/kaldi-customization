import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DecodingOverviewComponent } from './decoding.overview.component';

describe('DecodingOverviewComponent', () => {
  let component: DecodingOverviewComponent;
  let fixture: ComponentFixture<DecodingOverviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DecodingOverviewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DecodingOverviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
