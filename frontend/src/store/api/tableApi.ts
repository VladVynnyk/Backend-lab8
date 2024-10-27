import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const tableApi = createApi({
  reducerPath: 'tableApi',
  baseQuery: fetchBaseQuery({ baseUrl: import.meta.env.VITE_API_URL }),
  endpoints: (builder) => ({
    getThermometers: builder.query<void, void>({
      query: () => '/thermometers',
    }),
    getUsers: builder.query<void, void>({
      query: () => '/users',
    }),
    getCategoriess: builder.query<void, void>({
      query: () => '/categories',
    }),
    getProperties: builder.query<void, void>({
      query: () => '/properties',
    }),
  }),
});

export const { useGetThermometersQuery, useGetPropertiesQuery, useGetCategoriessQuery, useGetUsersQuery } = tableApi;
