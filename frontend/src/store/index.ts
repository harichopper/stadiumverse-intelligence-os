// Simple Redux store setup for StadiumVerse AI V2
import { configureStore } from '@reduxjs/toolkit';

// Simple state slice
const initialState = {
  ai: {
    status: 'initializing',
    provider: 'ollama'
  },
  stadium: {
    fans: [],
    metrics: {}
  }
};

// Simple reducer
const rootReducer = (state = initialState, action: any) => {
  switch (action.type) {
    default:
      return state;
  }
};

export const store = configureStore({
  reducer: rootReducer
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;