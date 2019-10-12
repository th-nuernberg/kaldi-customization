import { Pipe, PipeTransform } from '@angular/core';
import { LanguageMapperService } from './_services';

@Pipe({
    name: 'language'
})
export class LanguageMessagePipe implements PipeTransform {
    constructor() {}

    public transform(value: any, type: string): string {
      if (value == null) {
          return null;
      }

      switch (type) {
        case 'language': return LanguageMapperService.convertLanguage(value);
        default: throw new Error(`Invalid language type specified: ${type}`);
    }
  }
}
