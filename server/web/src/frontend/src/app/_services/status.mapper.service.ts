import {
  AudioStatus,
  DecodeSessionStatus,
  ResourceStatus,
  TrainingStatus
} from 'swagger-client'

export default class StatusMapperService {

  static readonly _isInitialized = " ist initialisiert";
  static readonly _isReady = " ist bereit";
  static readonly _isPending = " steht noch aus";
  static readonly _isInProcess = " ist in Bearbeitung";
  static readonly _isInProgress = " ist in Bearbeitung";
  static readonly _wasSuccessful = " war erfolgreich";
  static readonly _hasFailed = " ist fehlgeschlagen";
  static readonly _isTrainingable = " ist trainierbar";

  /**
  * Converts the audio status code into text into text.
  * @param value The audio status code
  */
  public static convertAudioStatus(value: any): string {
    const audioPrep = "Audiovorbereitung";
    switch(+value) {
      case AudioStatus.Init: {
        return audioPrep + this._isInitialized;
      }
      case AudioStatus.AudioPrep_Pending: {
        return audioPrep + this._isPending;
      }
      case AudioStatus.AudioPrep_In_Progress: {
        return audioPrep + this._isInProgress;
      }
      case AudioStatus.AudioPrep_Success: {
        return audioPrep + this._wasSuccessful;
      }
      case AudioStatus.AudioPrep_Failure: {
        return audioPrep + this._hasFailed;
      }
      default: {
        console.error('missing status code for audio ' + value);
        return value;
      }
    }
  }

  /**
  * Converts the resource status code into text.
  * @param value The resource status code.
  */
  public static convertResourceStatus(value: any): string {
    const upload = "Upload";
    const textPrep = "Textaufbereitung";

    switch(+value) {
      case ResourceStatus.Upload_InProgress: {
        return upload + this._isInProgress;
      }
      case ResourceStatus.Upload_Failure: {
        return upload + this._hasFailed;
      }
      case ResourceStatus.TextPreparation_Ready: {
        return textPrep + this._isReady;
      }
      case ResourceStatus.TextPreparation_Pending: {
        return textPrep + this._isPending;
      }
      case ResourceStatus.TextPreparation_InProcess: {
        return textPrep + this._isInProcess;
      }
      case ResourceStatus.TextPreparation_Failure: {
        return textPrep + this._hasFailed;
      }
      case ResourceStatus.TextPreparation_Success: {
        return textPrep + this._wasSuccessful;
      }
      default: {
        console.error('missing status code for resource ' + value);
        return value;
      }
    }
  }

  /**
  * Converts the training status code into text.
  * @param value The training status code.
  */
  public static convertTrainingStatus(value: any): string {
    const training = "Training";
    const textPrep = "Textaufbereitung";
    const dataPrep = "Datenaufbereitung";
    switch(+value) {
      case TrainingStatus.Init: {
        return training + this._isInitialized;
      }
      case TrainingStatus.TextPrep_Pending: {
        return textPrep + this._isPending;
      }
      case TrainingStatus.TextPrep_Failure: {
        return textPrep +  this._hasFailed;
      }
      case TrainingStatus.Trainable: {
        return training + this._isTrainingable;
      }
      case TrainingStatus.Training_DataPrep_Pending: {
        return dataPrep +  this._isPending;
      }
      case TrainingStatus.Training_DataPrep_InProgress: {
        return dataPrep + this._isInProgress;
      }
      case TrainingStatus.Training_DataPrep_Success: {
        return dataPrep + this._wasSuccessful;
      }
      case TrainingStatus.Training_DataPrep_Failure: {
        return dataPrep + this._hasFailed;
      }
      case TrainingStatus.Training_Pending: {
        return training + this._isPending;
      }
      case TrainingStatus.Training_In_Progress: {
        return training + this._isInProgress;
      }
      case TrainingStatus.Training_Success: {
        return training + this._wasSuccessful;
      }
      case TrainingStatus.Training_Failure: {
        return training + this._hasFailed;
      }
      default: {
        console.error('missing status code for training ' + value);
        return value;
      }
    }
  }

  /**
  * Converts the decode audio session status code into text.
  * @param value The decode audio session status code.
  */
  public static convertDecodeAudioSessionStatus(value: any): string {
    const decodeAudioSession = "Spracherkennungssession";

    switch(+value) {
      case DecodeSessionStatus.Init: {
        return decodeAudioSession +  this._isInitialized;
      }
      case DecodeSessionStatus.Decoding_Pending: {
        return decodeAudioSession + this._isPending;
      }
      case DecodeSessionStatus.Decoding_InProgress: {
        return decodeAudioSession + this._isInProgress;
      }
      case DecodeSessionStatus.Decoding_Success: {
        return decodeAudioSession + this._wasSuccessful;
      }
      case DecodeSessionStatus.Decoding_Failure: {
        return decodeAudioSession + this._hasFailed;
      }
      default: {
        console.error('missing status code for training ' + value);
        return value;
      }
    }
  }
}
