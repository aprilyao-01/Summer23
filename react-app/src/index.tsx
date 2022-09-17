import React from 'react';
import ReactDOM from 'react-dom/client';
import IsAnt from './components/IsAnt';


const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <IsAnt />
  </React.StrictMode>
);