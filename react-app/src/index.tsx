import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import NewApp from './NewApp';
import Test from './Test';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
    {/* <Test /> */}
    {/* <NewApp /> */}
  </React.StrictMode>
);