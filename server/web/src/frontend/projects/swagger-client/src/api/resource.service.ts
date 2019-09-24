/**
 * Kaldi Customization Server
 * Kaldi Customization Server.
 *
 * The version of the OpenAPI document: 1.1.0
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

import { Resource } from '../model/resource';

import { BASE_PATH, COLLECTION_FORMATS }                     from '../variables';
import { Configuration }                                     from '../configuration';


@Injectable({
  providedIn: 'root'
})
export class ResourceService {

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
     * Create/Upload a new resource
     * 
     * @param upfile File object that needs to be uploaded
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public createResource(upfile: Blob, observe?: 'body', reportProgress?: boolean): Observable<Resource>;
    public createResource(upfile: Blob, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<Resource>>;
    public createResource(upfile: Blob, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<Resource>>;
    public createResource(upfile: Blob, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {
        if (upfile === null || upfile === undefined) {
            throw new Error('Required parameter upfile was null or undefined when calling createResource.');
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
            'multipart/form-data'
        ];

        const canConsumeForm = this.canConsumeForm(consumes);

        let formParams: { append(param: string, value: any): any; };
        let useForm = false;
        let convertFormParamsToString = false;
        // use FormData to transmit files using content-type "multipart/form-data"
        // see https://stackoverflow.com/questions/4007969/application-x-www-form-urlencoded-or-multipart-form-data
        useForm = canConsumeForm;
        if (useForm) {
            formParams = new FormData();
        } else {
            formParams = new HttpParams({encoder: new CustomHttpUrlEncodingCodec()});
        }

        if (upfile !== undefined) {
            formParams = formParams.append('upfile', <any>upfile) as any || formParams;
        }

        return this.httpClient.post<Resource>(`${this.configuration.basePath}/resource`,
            convertFormParamsToString ? formParams.toString() : formParams,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Returns a list of available resources
     * 
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public getResource(observe?: 'body', reportProgress?: boolean): Observable<Array<Resource>>;
    public getResource(observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<Array<Resource>>>;
    public getResource(observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<Array<Resource>>>;
    public getResource(observe: any = 'body', reportProgress: boolean = false ): Observable<any> {

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

        return this.httpClient.get<Array<Resource>>(`${this.configuration.basePath}/resource`,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Find resource by UUID
     * Returns a single resource
     * @param resource_uuid UUID of resource to return
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public getResourceByUuid(resource_uuid: string, observe?: 'body', reportProgress?: boolean): Observable<Resource>;
    public getResourceByUuid(resource_uuid: string, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<Resource>>;
    public getResourceByUuid(resource_uuid: string, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<Resource>>;
    public getResourceByUuid(resource_uuid: string, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {
        if (resource_uuid === null || resource_uuid === undefined) {
            throw new Error('Required parameter resource_uuid was null or undefined when calling getResourceByUuid.');
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

        return this.httpClient.get<Resource>(`${this.configuration.basePath}/resource/${encodeURIComponent(String(resource_uuid))}`,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Returns the resource content
     * Returns the resource content
     * @param resource_uuid UUID of resource to return
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public getResourceData(resource_uuid: string, observe?: 'body', reportProgress?: boolean): Observable<Blob>;
    public getResourceData(resource_uuid: string, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<Blob>>;
    public getResourceData(resource_uuid: string, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<Blob>>;
    public getResourceData(resource_uuid: string, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {
        if (resource_uuid === null || resource_uuid === undefined) {
            throw new Error('Required parameter resource_uuid was null or undefined when calling getResourceData.');
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
            'application/pdf',
            'image/png',
            'text/html',
            'text/plain',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'image/jpeg'
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected !== undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
        ];

        return this.httpClient.get(`${this.configuration.basePath}/resource/${encodeURIComponent(String(resource_uuid))}/data`,
            {
                responseType: "blob",
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

}
