// Simple Redux store setup for StadiumVerse Intelligence OS
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

type Action = { type: string };
// Simple reducer
const rootReducer = (state = initialState, action: Action) => {
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
