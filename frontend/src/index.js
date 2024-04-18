import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import {
  createHashRouter,
  RouterProvider,
  Route,
  Link,
} from "react-router-dom";
import SearchPage from './SearchPage';


const router = createHashRouter([
  {
    path: "/",
    element: (
      <App/>
    ),
  },
  {
    path: "search",
    element: <SearchPage/>,
  },
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
