# File Structure
```bash
react-app
├── node_modules
│	└── .......
├── public
│     ├── favicon.ico
│     ├── index.html
│     ├── logo192.png
│     ├── logo512.png
│     ├── manifest.json
│     └── robots.txt
├── src
│    ├── App.js
│    └── index.js
├── createApp-original-readme.md
├── package-lock.json
├── package.json
└── readme.md
```
-  `node_modules`: libraries that used in this app (be ignored when push to git).
- `public/index.html`: essential HTML file.  It only has one div which is `#root`, all of application is going to be put inside of this div.
- `src`: the main part of the application.
    - `index.js`: where hte application starts, and will render the content that passed at a certain element. By default, render everything inside of `<App />` component at `#root` element. 
    - `App.js` : the app component, the base root of entire application. After `npm start`, every saved changes will refresh and reload automatically.

