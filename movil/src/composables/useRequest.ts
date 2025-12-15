import axios, { type AxiosRequestConfig, type AxiosResponse } from 'axios';
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

interface RequestOptions {
  url: string;
  data?: any;
  headers?: { [key: string]: string };
}

type HttpRequestResponse<T = any> = AxiosResponse<T>;

async function makeRequest<T = any>(
  method: HttpMethod,
  url: string,
  data?: any,
  headers?: { [key: string]: string }
): Promise<HttpRequestResponse<T>> {
  const axiosConfig: AxiosRequestConfig = {
    method,
    url,
    headers,
    data,
  };
  return await axios<T>(axiosConfig);
}

const httpRequest = {
  get<T = any>(url: string, options?: RequestOptions) {
    return makeRequest<T>('GET', url, options?.data, options?.headers);
  },
  post<T = any>(url: string, data?: any, headers?: { [key: string]: string }) {
    return makeRequest<T>('POST', url, data, headers);
  },
  put<T = any>(url: string, data?: any, headers?: { [key: string]: string }) {
    return makeRequest<T>('PUT', url, data, headers);
  },
  patch<T = any>(url: string, data?: any, headers?: { [key: string]: string }) {
    return makeRequest<T>('PATCH', url, data, headers);
  },
  delete<T = any>(url: string, data?: any, headers?: { [key: string]: string }) {
    return makeRequest<T>('DELETE', url, data, headers);
  },
};

export default httpRequest;
