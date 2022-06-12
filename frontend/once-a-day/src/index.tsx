import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";
import './index.css';
import HomeApp from './home/HomeApp';
import NewsApp from './news/NewsApp';
import { CreateAccount, Login } from "./home/Forms";

import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
const isLocal = false
root.render(
  <React.StrictMode>
      <BrowserRouter>
        <Routes>
          {/* <Route path= "/" element={<HomeApp/>}/> */}
          <Route path= "/" element={<NewsApp isLocal={isLocal} />}/>
          <Route path= "/news" element={<NewsApp isLocal={isLocal} />}/>
          <Route path= "/login" element={<Login />}/>
          <Route path= "/create-account" element={<CreateAccount/>}/> 
        </Routes>
    </BrowserRouter>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
