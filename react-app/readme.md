# Run the code
## Backend
1. Open a terminal window, cd to folder `react-app` then run `uvicorn backend.main:app --reload`.
2. Open http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc in browser to monitor the backend.

## Frontend
1. Open another terminal window, cd to folder `react-app` then run `npm stat`.
2. It will auto open the frontend page in browser, if not, go to http://localhost:3000/ to see the frontend.

## ScreenShot
|![screenshot1](/img/screenshot1.png)|![screenshot2](/img/screenshot2.png)|
|-|-|
# File Structure
```bash
react-app
├── backend
│    ├── peewee_app
│    │       ├── crud.py
│    │       ├── database.py
│    │       ├── models.py
│    │       └── schemas.py
│    ├── __init__.py
│    └── main.py
│    
├── node_modules
│	└── .......
├── public
│     └── index.html
├── src
│    ├── components
│    │       ├── AntDesign.css
│    │       ├── AntDesign.tsx
│    │       ├── DropDown.tsx
│    │       ├── Emoji.tsx
│    │       ├── Employees.tsx
│    │       ├── HeadTitle.tsx
│    │       ├── InputForm.tsx
│    │       ├── IsAnt.tsx
│    │       ├── model.ts
│    │       ├── operation.ts
│    │       └── SingleEmployee.tsx
│    ├── App.tsx
│    ├── App.css
│    └── index.tsx
│ 
├── createApp-original-readme.md
├── notes.md
├── package-lock.json
├── package.json
├── readme.md
└── tsconfig.json
```
- `backend`: fastAPI with peewee and postgresql, a copy from [fastapi-postgresql/peewee](/fastapi-postgresql/peewee_app/), simplified some checking logic to be more consistent with frontend.
-  `node_modules`: libraries that used in this app (be ignored when push to git).
- `public/index.html`: essential HTML file.  It only has one div which is `#root`, all of application is going to be put inside of this div.
- `src`: the main part of the application.
    - `components`: different small components that built the page.
    - `index.tsx`: where hte application starts, and will render the content that passed at a certain element. By default, render everything inside of `<App />` component at `#root` element. 
    - `App.tsx` : the app component, the base root of entire application. After `npm start`, every saved changes will refresh and reload automatically.

# Notes
See [`notes.md`](/react-app/notes.md)