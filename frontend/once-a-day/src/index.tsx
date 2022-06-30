import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";
import './index.css';
import { URL } from './constants'
import NewsApp from './news/NewsApp';
import HomeApp from './home/HomeApp';
import { ConfirmAccount, CreateAccount, Login, SelectSubscription } from "./home/Forms";
import reportWebVitals from './reportWebVitals';
import Ana from './ana';

const isLocal = true

Ana.setup()

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  // TODO: StrictMode is calling double renders (and mounts, API calls etc.)
  // <React.StrictMode>
      <BrowserRouter >
        <Routes>
          <Route path={URL.ROOT} element={<HomeApp/>}/>
          <Route path={URL.NEWS_BASE} element={<NewsApp isLocal={isLocal} />}/>
          <Route path={URL.LOGIN} element={<Login />}/>
          <Route path={URL.CREATE_ACCOUNT} element={<CreateAccount/>}/> 
          <Route path={URL.SUBSCRIPTIONS} element={<SelectSubscription/>}/> 
          <Route path={URL.CONFIRM_ACCOUNT} element={<ConfirmAccount/>}/>
        </Routes>
    </BrowserRouter>
  // </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
