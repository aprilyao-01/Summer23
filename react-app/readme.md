# README Part
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

# Notes Part
## React
React is a JavaScript library for building user interfaces.

## Begin
### Create a New React App using `Create React App`
`Create React App` is the best way to start building a new **single-page application** in React. 
Required: `Node >= 14.0.0` and `npm >= 5.6`.

1. Check if `Node` installed by run  `$ node -v` in terminal. If doesn't show version or show error, then go to https://nodejs.org/en/ and install first.
2. Run `$ npx create-react-app .` which use the current folder and create application inside of it. To specify the target folder, replace the `.` with target folder name. After a long time waiting, it will shows `Success! Created react-app at <folder path>` which means the app is created successfully.
    - Or run `$npx create-react-app . --template typescript` to create a new  React app project with TS.
3. Inside that directory, you can run several commands:
    - `npm start` to starts the **development** server (i.e. runs the app in the development mode). Recommend begin with this command.
    - `npm run build`: Bundles the app into static files for **production**.
    and scripts into the app directory. If you do this, you can’t go back!
4. Runs the app in the development mode by `$ npm start` and open [http://localhost:3000](http://localhost:3000) to view it in browser.

5. To get blank application :
    1. Only keep `index.js` and `App.js` and delete others in `src` folder.
    2. Change function body in `App.js` to `return null`.
    3. Delete all not relevant import.

`Create React App` doesn’t handle backend logic or databases; it just creates a frontend build pipeline, so it can be used with any backend. A readme file is auto created after run the command, see [createApp-original-readme](/react-app/createApp-original-readme.md).

### Add React to a Website
<!-- TODO -->



## JSX
### What is JSX and why use it
``` jsx
const element = <h1>Hello, world!</h1>;
```
JSX like above tag syntax is neither a string nor HTML, it's a syntax extension to JS. It describes what the UI should look like. React *doesn’t require* using JSX, but it's helpful as a visual aid when working with UI inside the JS code. It also allows React to show more useful error and warning messages.

### How to use JSX
*See https://reactjs.org/docs/introducing-jsx.html for examples.*

1. **Any** valid JS expression can be put inside the curly braces { } in JSX.

2. After compilation, JSX expressions become regular JS function calls and evaluate to JS objects, which means JSX can be used inside of `if` statements and `for` loops, `assign` it to variables, accept it as `arguments`, and `return` it from functions.

3. Can use **quotes " "** to specify string literals as attributes or use **curly braces { }** to embed a JS expression in an attribute. But **not** both in the same attribute.

4. JSX tags may `contain children`, and if a tag is empty, can close it immediately with `/>`, like XML.

5. It is safe to **embed user input** in JSX. React DOM *escapes* any values embedded in JSX before rendering them by default. Ensures that you can never inject anything that’s not explicitly written in your application. Everything is converted to a *string* before being rendered, helps prevent XSS (cross-site-scripting) attacks.

6. Babel compiles JSX down to **`React.createElement()`** calls, which will performs a few checks to help write bug-free code but essentially it creates an object. These objects are called **“React elements”** that describes what you want to see on the screen. React reads these objects and uses them to construct the DOM and keep it up to date.

## Elements, Components, Props, State and Lifecycle
### Elements
Elements are the smallest building blocks of React apps. An element describes what you want to see on the screen. React DOM takes care of updating the DOM to match the React elements.
```jsx
const element = <h1>Hello, world</h1>;
```
To render a React element, first pass the DOM element to `ReactDOM.createRoot()`, then pass the React element to `root.render()`:
```HTML
<!-- in HTML file -->
<div id="root"></div>
```
```jsx
// in JS file
const root = ReactDOM.createRoot(
  document.getElementById('root')
);
const element = <h1>Hello, world</h1>;
root.render(element);
```
React elements are **immutable**. Once you create an element, you can’t change its children or attributes. So, the only way to update the UI is to create a *new* element, and pass it to `root.render()`.
Also, React DOM compares the element and its children to the previous one, and **only** applies the DOM updates **necessary** to bring the DOM to the desired state.


### Components
Components let developer split the UI into **independent**, **reusable** pieces, and think about each piece in isolation. Conceptually, components are like JS functions. They accept arbitrary inputs (called “props”) and return React elements describing what should appear on the screen.
```jsx
/* The simplest way to define a component 
is to write a JS function: */

function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}

/* This function is a valid React component 
because it accepts a single “props” (which stands for properties) object argument with data 
and returns a React element. */

// or use an ES6 class to define a component
class Welcome extends React.Component {
  render() {
    return <h1>Hello, {this.props.name}</h1>;
  }
}

/* Components can refer to other components in their output.
Useful to split components into smaller components. */
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}

function App() {
  return (
    <div>
      <Welcome name="Sara" />
      <Welcome name="Cahal" />
      <Welcome name="Edite" />
    </div>
  );
}
```

:warning: Always start component names with a capital letter. React treats components starting with lowercase letters as DOM tags. For example, `<div /> `represents an HTML div tag, but `<Welcome />` represents a component and requires Welcome to be in scope.

### Props
React elements not only represent DOM tags can also represent **user-defined components**. When React sees an element representing a user-defined component, it passes JSX attributes and children to this component as a single object. This object  is **“props”**.
```jsx
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}

const root = ReactDOM.createRoot(document.getElementById('root'));
const element = <Welcome name="Sara" />;
root.render(element);
```
:warning: Props are **read-only**. Whether you declare a component as a function or a class, it must never modify its own props. All React components must act like pure functions with respect to their props.

### State
State is similar to props, but it is **private** and fully controlled by the component.

Convert a function component to a class in :raised_hand_with_fingers_splayed: steps:
1. Create an `ES6 class`, with the same name, that extends `React.Component`.
2. Add a single empty method to it called `render()`.
3. Move the body of the function into the `render()` method.
4. Replace `props` with `this.props` in the `render()` body.
5. Delete the remaining empty function declaration.
```jsx
class Clock extends React.Component {
  render() {
    return (
      <div>
        <h1>Hello, world!</h1>
        <h2>It is {this.props.date.toLocaleTimeString()}.</h2>
      </div>
    );
  }
}
```
<br>

Adding local state to a class, by moving the date from props to state in :v:+:point_up: steps:
1. Replace `this.props.date` with `this.state.date` in `the render()` method.
2. Add a **class constructor** that assigns the initial `this.state`, and pass `props` to the base constructor. Class components should always call the base constructor with `props`.
3. Remove the date prop from the `<Clock />` element.
```jsx
class Clock extends React.Component {
  constructor(props) {
    super(props);
    this.state = {date: new Date()};
  }

  render() {
    return (
      <div>
        <h1>Hello, world!</h1>
        <h2>It is {this.state.date.toLocaleTimeString()}.</h2>
      </div>
    );
  }
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<Clock />);
```

:warning: Three things that need to know about `setState()`:
1. **Do Not Modify State Directly**, this will not re-render a component. Instead, use `setState()`, the only place can assign `this.state `is the constructor.
    ```jsx
    this.state.comment = 'Hello';       // Wrong
    this.setState({comment: 'Hello'});  // // Correct
    ```

2. **State Updates May Be Asynchronous**. React may batch multiple `setState()` calls into a single update for performance.
Because `this.props` and `this.state` may be updated **asynchronously**, should not rely on their values for calculating the next state. To fix it, use a second form of `setState()` that accepts a **function** rather than an object. That function will receive the previous state as the first argument, and the props at the time the update is applied as the second argument. 
    ```jsx

    this.setState({         // Wrong
    counter: this.state.counter + this.props.increment,
    });

    this.setState((state, props) => ({          // Correct
    counter: state.counter + props.increment
    }));

    this.setState(function(state, props) {          // Also Correct
    return {
        counter: state.counter + props.increment
    };
    });
    ```

3. **State Updates are Merged**. When call `setState()`, React merges the provided object into the current state. The merging is shallow, so `this.setState({comments}) `leaves `this.state.posts` intact, but completely replaces `this.state.comments`.
    ```jsx
    constructor(props) {
        super(props);
        this.state = {
        posts: [],        // variable 1
        comments: []      // variable 2
        };
    }

    componentDidMount() {
    fetchPosts().then(response => {
        this.setState({
        posts: response.posts       // update independently
        });
    });

    fetchComments().then(response => {
        this.setState({
        comments: response.comments     // update independently
        });
    });
    }
    ```
<br>

State is often called *local* or *encapsulated*. It is not accessible to any component other than the one that owns and sets it.
A component may choose to pass its state down as props to its child components. The `FormattedDate` component would receive the `date` in its props and wouldn’t know whether it came from the `Clock`’s state, from the `Clock`’s props, or was typed by hand. 
This is commonly called a **“top-down”** or **“unidirectional”** data flow. Any state is always owned by some specific component, and any data or UI derived from that state can only affect components **“below”** them in the tree.
```jsx
<FormattedDate date={this.state.date} />
function FormattedDate(props) {
  return <h2>It is {props.date.toLocaleTimeString()}.</h2>;
}
```

### Lifecycle
**“Mounting”**: Whenever the `Clock` is rendered to the DOM for the first time. 
**“Unmounting”**: Whenever the DOM produced by the `Clock` is removed.
**“Lifecycle methods”**:  Special methods can be declared on the component class to run some code when a component *mounts and unmounts*.
```jsx
class Clock extends React.Component {
  constructor(props) {
    super(props);
    this.state = {date: new Date()};
  }

  componentDidMount() {         // runs after the component output has been rendered to the DOM
    this.timerID = setInterval(
      () => this.tick(),
      1000
    );          // set up a timer
  }

  componentWillUnmount() {
    clearInterval(this.timerID);        // tear down the timer
  }

  tick() {             // Clock component will run every second
    this.setState({    // schedule updates to the component local state
      date: new Date()
    });
  }

  render() {
    return (
      <div>
        <h1>Hello, world!</h1>
        <h2>It is {this.state.date.toLocaleTimeString()}.</h2>
      </div>
    );
  }
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<Clock />);
```

## Handling Events
Handling events with React elements is very similar to handling events on DOM elements. There are some syntax differences:
- React events are named using **camelCase**, rather than lowercase.
- With JSX you pass a **function** as the event handler, rather than a string.

When using React, generally don’t need to call `addEventListener` to add listeners to a DOM element after it is created. Instead, just provide a listener when the element is **initially rendered**.
```jsx
class Toggle extends React.Component {
  constructor(props) {
    super(props);
    this.state = {isToggleOn: true};

    // This binding is necessary to make `this` work in the callback
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    this.setState(prevState => ({
      isToggleOn: !prevState.isToggleOn
    }));
  }

  render() {
    return (
      <button onClick={this.handleClick}>
        {this.state.isToggleOn ? 'ON' : 'OFF'}
      </button>
    );
  }
}
```

Passing Arguments to Event Handlers: Inside a loop, it is common to want to pass an extra parameter to an event handler. For example, if id is the row ID, either of the following would work.
```jsx
<button onClick={(e) => this.deleteRow(id, e)}>Delete Row</button>
<button onClick={this.deleteRow.bind(this, id)}>Delete Row</button>
```

## Conditional Rendering
In React, distinct components can encapsulate distinct behaviors. Depending on the state of the application, can render only some of them.
Conditional rendering in React works the same way conditions work in JavaScript. Use JavaScript operators like `if` or the `conditional operator` to create elements representing the current state, and let React update the UI to match them.
```jsx
function UserGreeting(props) {
  return <h1>Welcome back!</h1>;
}

function GuestGreeting(props) {
  return <h1>Please sign up.</h1>;
}

function Greeting(props) {
  const isLoggedIn = props.isLoggedIn;
  if (isLoggedIn) {
    return <UserGreeting />;
  }
  return <GuestGreeting />;
  
  // same as
  // return( <div> {isLoggedIn  ?<UserGreeting />  : <GuestGreeting /> } </div>)
  
}

const root = ReactDOM.createRoot(document.getElementById('root')); 
// Try changing to isLoggedIn={true}:
root.render(<Greeting isLoggedIn={false} />);
```

Inline If with Logical `&&` Operator: embed expressions in JSX by wrapping them in `curly braces { }`. This includes the JS logical `&&` operator. It can be handy for conditionally including an element. If the condition is `true`, the element right after `&&` will appear in the output. If it is `false`, React will **ignore and skip** it.
```jsx
function Mailbox(props) {
  const unreadMessages = props.unreadMessages;
  return (
    <div>
      <h1>Hello!</h1>
      {unreadMessages.length > 0 &&
        <h2>
          You have {unreadMessages.length} unread messages.
        </h2>
      }
    </div>
  );
}
```

## Thinking in React
How to decide components, for example, build a searchable product data table using React. See https://reactjs.org/docs/thinking-in-react.html.