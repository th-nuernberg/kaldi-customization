import { Pipe, PipeTransform } from '@angular/core';
import { StatusMapperService } from './_services';

@Pipe({
    name: 'message'
})
export class StatusMessagePipe implements PipeTransform {
    constructor() {}

    public transform(value: any, type: string): string {
        if (value == null) {
            return null;
        }

        switch (type) {
            case 'audio': return StatusMapperService.convertAudioStatus(value);
            case 'resource': return StatusMapperService.convertResourceStatus(value);
            case 'training': return StatusMapperService.convertTrainingStatus(value);
            case 'decodeAudioSession': return StatusMapperService.convertDecodeAudioSessionStatus(value);
            default: throw new Error(`Invalid status message type specified: ${type}`);
	    }
    }
}
