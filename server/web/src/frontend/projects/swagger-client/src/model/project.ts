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
 */import { AcousticModel } from './acousticModel';
import { TrainingStatus } from './trainingStatus';
import { User } from './user';


export interface Project { 
    uuid?: string;
    name: string;
    owner: User;
    acousticModel: AcousticModel;
    parent?: Project;
    status?: TrainingStatus;
    resources?: Array<any>;
}