
export default class LanguageMapperService {

 /**
  * Converts the used model language into German.
  * @param value The model value, currently in English
  */
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
