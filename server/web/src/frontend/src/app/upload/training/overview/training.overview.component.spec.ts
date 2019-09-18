import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TrainingOverviewComponent } from './training.overview.component';

describe('TrainingOverviewComponent', () => {
  let component: TrainingOverviewComponent;
  let fixture: ComponentFixture<TrainingOverviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TrainingOverviewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TrainingOverviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
