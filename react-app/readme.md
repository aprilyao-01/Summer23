# React
React is a JavaScript library for building user interfaces.


## Begin
### Create a New React App using `Create React App`
`Create React App` is the best way to start building a new **single-page application** in React. 
Required: `Node >= 14.0.0` and `npm >= 5.6`.

1. Check if `Node` installed by run  `$ node -v` in terminal. If doesn't show version or show error, then go to https://nodejs.org/en/ and install first.
2. Run `$ npx create-react-app .` which use the current folder and create application inside of it. To specify the target folder, replace the `.` with target folder name. After a long time waiting, it will shows `Success! Created react-app at <folder path>` which means the app is created successfully.
3. Inside that directory, you can run several commands:
    - `npm start` to starts the **development** server (i.e. runs the app in the development mode). Recommend begin with this command.
    - `npm run build`: Bundles the app into static files for **production**.
    - `npm test`: Starts the test runner.
    - `npm run eject`: Removes this tool and copies build dependencies, configuration files
    and scripts into the app directory. If you do this, you can’t go back!
4. Runs the app in the development mode by `$ npm start` and open [http://localhost:3000](http://localhost:3000) to view it in browser.

`Create React App` doesn’t handle backend logic or databases; it just creates a frontend build pipeline, so it can be used with any backend. A readme file is auto created after run the command, see [createApp-original-readme](/react-app/createApp-original-readme.md).

### Add React to a Website
## File Structure
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
│    ├── App.css
│    ├── App.js
│    ├── App.test.js
│    ├── index.css
│    ├── index.js
│    ├── logo.svg
│    ├── reportWebVitals.js
│    └── setupTests.js
├── createApp-original-readme.md
├── package-lock.json
├── package.json
└── readme.md
```