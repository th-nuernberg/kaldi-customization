
export default class LanguageMapperService {

  public static convertLanguage(value: any): string {

    switch(value) {
      case "German": {
        return "Deutsch";
      }
      case "English": {
        return "Englisch";
      }
      default: {
        console.error('missing language type ' + value);
        return value;
      }
    }
  }
}
