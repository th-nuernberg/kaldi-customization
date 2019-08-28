/**
 * Kaldi Customization Server
 * Kaldi Customization Server.
 *
 * The version of the OpenAPI document: 1.0.2
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


export type AudioStatus = 100 | 150 | 200 | 300 | 320;

export const AudioStatus = {
    Init: 100 as AudioStatus,
    AudioPrep_Pending: 150 as AudioStatus,
    AudioPrep_In_Progress: 200 as AudioStatus,
    AudioPrep_Success: 300 as AudioStatus,
    AudioPrep_Failure: 320 as AudioStatus
};
