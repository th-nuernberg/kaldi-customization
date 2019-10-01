import { Pipe, PipeTransform } from '@angular/core';
import { TypeMapperService } from './_services';

@Pipe({
    name: 'type'
})
export class TypeMessagePipe implements PipeTransform {
    constructor() {}

    public transform(value: any, type: string): string {
      if (value == null) {
          return null;
      }

      switch (type) {
        case 'acousticModel': return TypeMapperService.convertAcousticModelType(value);
        case 'resource': return TypeMapperService.convertResourceType(value);
        default: throw new Error(`Invalid type message type specified: ${type}`);
    }
  }
}
