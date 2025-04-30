import { configureStore } from "@reduxjs/toolkit";
import myObjectReducer from "./myObjectReducer";




export const store =  configureStore({
  reducer: {
    object1: myObjectReducer,
  }
});
