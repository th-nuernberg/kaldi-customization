/**
 * Kaldi Customization Server
 * Kaldi Customization Server.
 *
 * The version of the OpenAPI document: 1.5.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
/* tslint:disable:no-unused-variable member-ordering */

import { Inject, Injectable, Optional }                      from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams,
         HttpResponse, HttpEvent }                           from '@angular/common/http';
import { CustomHttpUrlEncodingCodec }                        from '../encoder';

import { Observable }                                        from 'rxjs';

import { TrainingStats } from '../model/trainingStats';

import { BASE_PATH, COLLECTION_FORMATS }                     from '../variables';
import { Configuration }                                     from '../configuration';


@Injectable({
  providedIn: 'root'
})
export class LoggingService {

    protected basePath = 'http://localhost:8080/api/v1';
    public defaultHeaders = new HttpHeaders();
    public configuration = new Configuration();

    constructor(protected httpClient: HttpClient, @Optional()@Inject(BASE_PATH) basePath: string, @Optional() configuration: Configuration) {

        if (configuration) {
            this.configuration = configuration;
            this.configuration.basePath = configuration.basePath || basePath || this.basePath;

        } else {
            this.configuration.basePath = basePath || this.basePath;
        }
    }

    /**
     * @param consumes string[] mime-types
     * @return true: consumes contains 'multipart/form-data', false: otherwise
     */
    private canConsumeForm(consumes: string[]): boolean {
        const form = 'multipart/form-data';
        for (const consume of consumes) {
            if (form === consume) {
                return true;
            }
        }
        return false;
    }


    /**
     * Get Training Log
     * Returns the log of a preparation
     * @param project_uuid UUID of the project
     * @param training_version Training version of the project
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public getPerparationLog(project_uuid: string, training_version: number, observe?: 'body', reportProgress?: boolean): Observable<string>;
    public getPerparationLog(project_uuid: string, training_version: number, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<string>>;
    public getPerparationLog(project_uuid: string, training_version: number, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<string>>;
    public getPerparationLog(project_uuid: string, training_version: number, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {
        if (project_uuid === null || project_uuid === undefined) {
            throw new Error('Required parameter project_uuid was null or undefined when calling getPerparationLog.');
        }
        if (training_version === null || training_version === undefined) {
            throw new Error('Required parameter training_version was null or undefined when calling getPerparationLog.');
        }

        let headers = this.defaultHeaders;

        // authentication (oauth) required
        if (this.configuration.accessToken) {
            const accessToken = typeof this.configuration.accessToken === 'function'
                ? this.configuration.accessToken()
                : this.configuration.accessToken;
            headers = headers.set('Authorization', 'Bearer ' + accessToken);
        }

        // to determine the Accept header
        const httpHeaderAccepts: string[] = [
            'text/plain'
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected !== undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
        ];

        return this.httpClient.get(`${this.configuration.basePath}/project/${encodeURIComponent(String(project_uuid))}/training/${encodeURIComponent(String(training_version))}/prepare/log`,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress,
                responseType: 'text'
            }
        );
    }

    /**
     * Find resource by UUID
     * Returns the log of a resource
     * @param resource_uuid UUID of resource to return
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public getResourceLog(resource_uuid: string, observe?: 'body', reportProgress?: boolean): Observable<string>;
    public getResourceLog(resource_uuid: string, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<string>>;
    public getResourceLog(resource_uuid: string, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<string>>;
    public getResourceLog(resource_uuid: string, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {
        if (resource_uuid === null || resource_uuid === undefined) {
            throw new Error('Required parameter resource_uuid was null or undefined when calling getResourceLog.');
        }

        let headers = this.defaultHeaders;

        // authentication (oauth) required
        if (this.configuration.accessToken) {
            const accessToken = typeof this.configuration.accessToken === 'function'
                ? this.configuration.accessToken()
                : this.configuration.accessToken;
            headers = headers.set('Authorization', 'Bearer ' + accessToken);
        }

        // to determine the Accept header
        const httpHeaderAccepts: string[] = [
            'text/plain'
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected !== undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
        ];

        return this.httpClient.get(`${this.configuration.basePath}/resource/${encodeURIComponent(String(resource_uuid))}/log`,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress,
                responseType: 'text'
            }
        );
    }

    /**
     * Get Training Log
     * Returns the log of a training
     * @param project_uuid UUID of the project
     * @param training_version Training version of the project
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public getTrainingLog(project_uuid: string, training_version: number, observe?: 'body', reportProgress?: boolean): Observable<string>;
    public getTrainingLog(project_uuid: string, training_version: number, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<string>>;
    public getTrainingLog(project_uuid: string, training_version: number, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<string>>;
    public getTrainingLog(project_uuid: string, training_version: number, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {
        if (project_uuid === null || project_uuid === undefined) {
            throw new Error('Required parameter project_uuid was null or undefined when calling getTrainingLog.');
        }
        if (training_version === null || training_version === undefined) {
            throw new Error('Required parameter training_version was null or undefined when calling getTrainingLog.');
        }

        let headers = this.defaultHeaders;

        // authentication (oauth) required
        if (this.configuration.accessToken) {
            const accessToken = typeof this.configuration.accessToken === 'function'
                ? this.configuration.accessToken()
                : this.configuration.accessToken;
            headers = headers.set('Authorization', 'Bearer ' + accessToken);
        }

        // to determine the Accept header
        const httpHeaderAccepts: string[] = [
            'text/plain'
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected !== undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
        ];

        return this.httpClient.get(`${this.configuration.basePath}/project/${encodeURIComponent(String(project_uuid))}/training/${encodeURIComponent(String(training_version))}/train/log`,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress,
                responseType: 'text'
            }
        );
    }

    /**
     * Get Training Stats
     * Returns the stats to be reviewed before training
     * @param project_uuid UUID of the project
     * @param training_version Training version of the project
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public getTrainingStats(project_uuid: string, training_version: number, observe?: 'body', reportProgress?: boolean): Observable<TrainingStats>;
    public getTrainingStats(project_uuid: string, training_version: number, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<TrainingStats>>;
    public getTrainingStats(project_uuid: string, training_version: number, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<TrainingStats>>;
    public getTrainingStats(project_uuid: string, training_version: number, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {
        if (project_uuid === null || project_uuid === undefined) {
            throw new Error('Required parameter project_uuid was null or undefined when calling getTrainingStats.');
        }
        if (training_version === null || training_version === undefined) {
            throw new Error('Required parameter training_version was null or undefined when calling getTrainingStats.');
        }

        let headers = this.defaultHeaders;

        // authentication (oauth) required
        if (this.configuration.accessToken) {
            const accessToken = typeof this.configuration.accessToken === 'function'
                ? this.configuration.accessToken()
                : this.configuration.accessToken;
            headers = headers.set('Authorization', 'Bearer ' + accessToken);
        }

        // to determine the Accept header
        const httpHeaderAccepts: string[] = [
            'application/json'
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected !== undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
        ];

        return this.httpClient.get<TrainingStats>(`${this.configuration.basePath}/project/${encodeURIComponent(String(project_uuid))}/training/${encodeURIComponent(String(training_version))}/stats`,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

}
