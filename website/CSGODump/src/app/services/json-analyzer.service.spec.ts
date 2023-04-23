import { TestBed } from '@angular/core/testing';

import { JsonAnalyzerService } from './json-analyzer.service';

describe('JsonAnalyzerService', () => {
  let service: JsonAnalyzerService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(JsonAnalyzerService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
