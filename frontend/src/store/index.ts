import { configureStore } from '@reduxjs/toolkit';
import {tableApi} from "./api/tableApi.ts";
// Додайте інші редюсери, якщо потрібно

const store = configureStore({
  reducer: {
    [tableApi.reducerPath]: tableApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(tableApi.middleware),
});

export default store;
