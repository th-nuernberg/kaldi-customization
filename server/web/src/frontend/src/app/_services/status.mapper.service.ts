import {
  AudioStatus,
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

  public static convertResourceStatus(value: any): string {
    const upload = "Upload";
    const textPrep = "Textvorbereitung";

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

  public static convertTrainingStatus(value: any): string {
    const training = "Training";
    switch(+value) {
      case TrainingStatus.Init: {
        return training + this._isInitialized;
      }
      case TrainingStatus.Trainable: {
        return training + this._isTrainingable;
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
}
