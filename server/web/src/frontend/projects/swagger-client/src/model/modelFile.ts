/**
 * Kaldi Customization Server
 * Kaldi Customization Server.
 *
 * OpenAPI spec version: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 */import { FileStatus } from './fileStatus';
import { FileType } from './fileType';


export interface ModelFile { 
    name: string;
    status?: FileStatus;
    fileType: FileType;
}