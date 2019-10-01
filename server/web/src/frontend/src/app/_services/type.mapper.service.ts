import {
  ResourceType,
  AcousticModelType
} from 'swagger-client'

export default class TypeMapperService {

  public static convertAcousticModelType(value: any): string {
    const HMM = "HMM";
    switch(+value) {
      case AcousticModelType.HMM_GMM: {
        return HMM + "-GMM";
      }
      case AcousticModelType.HMM_DNN: {
        return HMM + "-DNN";
      }
      case AcousticModelType.HMM_RNN: {
        return HMM + "-RNN";
      }
      default: {
        console.error('missing type code for acoustic model ' + value);
        return value;
      }
    }
  }

  public static convertResourceType(value: any): string {
    switch(+value) {
      case ResourceType.html: {
        return "HTML";
      }
      case ResourceType.docx: {
        return "DOCX";
      }
      case ResourceType.txt: {
        return "TXT";
      }
      case ResourceType.pdf: {
        return "PDF";
      }
      case ResourceType.png: {
        return "PNG";
      }
      case ResourceType.jpg: {
        return "JPG";
      }
      default: {
        console.error('missing type code for resource ' + value);
        return value;
      }
    }
  }
}
