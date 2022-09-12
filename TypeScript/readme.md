# Read Me
## Run the code
Go to terminal, run `$ tsc main.ts` first. This will generate the **latest edit version of** `main.js` javascript file that have same functionality. Double click `index.html` file to open it in browser.

# TypeScript
## TypeScript vs JavaScript
TypeScript is a *strict typed superset* of JavaScript, more like an improved version of JS.
`TS = JS + type system`  add features like increased readability, static compilation, intuitive interface etc. therefor, JS syntax is **legal** TS. 
TS **never** changes the runtime behavior of JS code, means that wherever run code in JS or TS, it is guaranteed to run the same way, even if TypeScript thinks that the code has type errors.

||JavaScript|TypeScript|
|-|--|--|
|Type-checking|Dynamically typed language, software will not treat type difference as errors up *until run time*| Optional static typing, once declared a variable doesn't change its type and can only take certain values. Compiler alerts developers to type related mistakes -> *early bug catching & structured code* |
|Readability|Few readability add-ons, lots of errors need to be *detected manually*|Static reading along, increased code optimization, offers clear categories for variable declaration-> early bug detection, stable code, defined types, more informative version of a code base|
|Features|Lacks several important features| Type annotation, value for each static type will be checked automatically. Generics, let developer write a generalized form of method. Improved API documentation, has tools like vscode navigation and let developers to see parameter types automatically, track variables etc.|
|Ecosystem|More tools that support|Not as much as JS|
|NPM Package|/|Can integrate ts with node.js|
|Compilation|The base of TS|Eventually transpile into JS|
|Popularity|The most popular language maybe|Increases the development speed, more and more developers use it|
|Use Cases|1. Extra transpilation tax isn't an option. 2. Flexibility is a priority -> offers dynamic typing allows to create new functionality without sticking to same rules  3. framework unsupported|1. Large codebase -> bring code to a single standard 2. Needed static typing  3. Speed is priority -> speeds up the development process by catching bugs in real time|

| |Pros|Cons|
|-|----|----|
|**TypeScript** vs **JavaScript**|- compiler catches errors <br>		- smaller feedback loop<br>		- makes factoring easier<br>- autocompletion/autoimports<br>- you can gradually adopt it<br>- more companies are adopting it|- takes more time upfront<br>- error messages<br>- library support<br>- takes time to learn|

## TypeScript Features
### Static type-checking
TypeScript has a static types systems that describe the shapes and behaviors of what our values will be when we run our programs. More easy to find bug in early stage, more quick to fix bugs.
It will catch typos, uncalled functions, basic logic errors or sometimes "valid" JS that won't immediately throw an error, and you can decide to leave it to go as it is.

### `tsc`, the TypeScript compiler

Install tsc by npm:  `npm install -g typescript`.

By run `tsc <filename>.ts` , `tsc` will compile or transform it to a plain **JS file**. Even if `tsc` reported problems, the JS file based on the ''error'' TS will still be transformed, so that TS will not actual "stop" you but only "warn" you. For example, scenario like you have a **worked** JS file and want to introducing type-checking errors and cleaning it afterwards. In this case, there is no reason TS to stop yun running the original JS code that was already working.

If you wan to be more defensive against mistakes and make TS act a bit more strictly, use `noEmitOnError` compiler option by run `tsc --noEmitOnError <filename>.ts`. So that if error occurs, JS file will never get updated.

### Explicit Types
For example,

   ```js
   function greet(person: string, date: Date) {
     console.log(`Hello ${person}, today is ${date.toDateString()}!`);
   }
   ```

add type annotations to describe that types of values `greet` can be called with. With this, TS can tell us about other cases where `greet` might have been called incorrectly.  However, type annotations **never** change the runtime behavior of program, when TS be complied to JS, all type annotations will be erased.

TS doesn’t use “types on the left”-style declarations like `int x = 0;` Type annotations will always go *after* the thing being typed. Wherever possible, TypeScript tries to automatically *infer* the types in your code. Even if you don’t have type annotations on your parameters, TypeScript will still check that you passed the right number of arguments. And usually don’t need a return type annotation because TypeScript will infer the function’s return type based on its `return` statements. 

For Optional properties, object types can also specify that some or all of their properties are *optional*. To do this, add a `?` after the property name: 

  ```js
  function printName(obj: { first: string; last?: string }) {
    // ...
  }
  // Both OK
  printName({ first: "Bob" });
  printName({ first: "Alice", last: "Alison" });
  ```

In JavaScript, if you access a property that doesn’t exist, you’ll get the value `undefined` rather than a runtime error. Because of this, when you *read* from an optional property, you’ll have to check for `undefined` before using it.

  ```js
  function printName(obj: { first: string; last?: string }) {
    // Error - might crash if 'obj.last' wasn't provided!
    console.log(obj.last.toUpperCase());
  Object is possibly 'undefined'.
  Object is possibly 'undefined'.
    if (obj.last !== undefined) {
      // OK
      console.log(obj.last.toUpperCase());
    }
  
    // A safe alternative using modern JavaScript syntax:
    console.log(obj.last?.toUpperCase());
  }
  ```

### Strictness
TypeScript has several type-checking strictness flags that can be turned on or off, and all of our examples will be written with all of them enabled unless otherwise stated. The [`strict`](https://www.typescriptlang.org/tsconfig#strict) flag in the CLI, or `"strict": true` in a [`tsconfig.json`](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html)toggles them all on simultaneously, but we can opt out of them individually. The two biggest ones you should know about are [`noImplicitAny`](https://www.typescriptlang.org/tsconfig#noImplicitAny) and [`strictNullChecks`](https://www.typescriptlang.org/tsconfig#strictNullChecks).



### Asnyc/ Await
**Synchronous code**: Start at the top of the file and execute all the way down to bottom of file, each line in order until it gets to the bottom and it will stop.

**Asynchronous code**: Start at the top of the file and execute until it gets to the bottom, during execution if run into certain asynchronous functions or code or it will split off and execute that asynchronous code separately from the rest of the code. Usually because it needs to wait reduce some operation that takes a long period of time. So it will execute from top, if occurs asynchronous code, run this part of code and the rest of the code at the same time, and it will do that for every asynchronous code it hits. Results to have multiple different threads running different code in different sections and may execute in a different order. Some asynchronous functions for example:

- `setTimeout(somefunction(), timelog)` will run `somefunction()` after `timelog` that you specified. 

- `.then(somefunction())` will first run what happened before `.then` then run `somefunction()`.



**`Promise()`** is like actual promise in real life, you promised something, which will lead to two consequences. One 'resolve' means you sticked to your promise, one 'reject' means you failed on your promise.

```JS
let p = new Promise( (resolve, reject) => {
 let a = 1+1           // make some promise
 if(a == 2){ resolve('Success stick to your promise')} 
 else { reject('Failed on your promise.') }
})

p.then((message) =>{			// message come from promise, in this case is sentence message
  console.log('This means promise resolve' + message)
}).catch((message) =>{
  console.log('This means promise reject ' + message)
})

// write in function
function makePromise(number){
  return new Promise((resolve, reject) => {
     let a = 1+number           // make some promise
     if(a == 2){ resolve('Success stick to your promise')} 
     else { reject('Failed on your promise.') }
  })
}

var number = 1
makePromise(number).then((message) =>{
  // message come from promise, in this case is sentence message
  console.log('This means promise resolve' + message)
}).catch((message) =>{
  console.log('This means promise reject ' + message)
})
```



**`Async/ Await`** basically is syntactical sugar wrapped around `Promise` to make it easier to work with.

```JS
// Rewrite the previous Promise function into async/await
function makePromise(number){
  return new Promise((resolve, reject) => {
     let a = 1+number           // make some promise
     if(a == 2){ resolve('Success stick to your promise')} 
     else { reject('Failed on your promise.') }
  })
}

var number = 1

async function promiseButAsync(){
  try{
    const message = await makePromise(number)
    console.log('This means promise resolve' + message)
  } catch (message){
    console.log('This means promise reject ' + message)
  } 
}

promiseButAsync()
```

-  `async` tells JS that this function is asynchronous, so that it will know how to handle the `await` sequences that put inside if it.
- `await` tells JS the code should wait until this await function (in this case `makePromise`) is finished, then afterward execute the next thing. Once JS hits the `await` statement, it'll leave the function, do other work inside of the program and as soon as the await function finishes executing it'll come back to where  await function is and return the result to variable `message`.
- `try...catch...`  along side the `await` will run code like `.then.catch` but easier to reason with and looks more like synchronous code even though it's actually asynchronous code.

### Type Casting
JS doesn’t have a concept of type casting because variables have dynamic types. However, TS variables have type, can use the `as` keyword or `<>` operator for type castings to convert a variable from one type to another.
- Casting use `as`:
```JS
const input = document.querySelector('input[type="text"]') as HTMLInputElement;
console.log(input.value);
```
- Casting use `<>`:
```JS
const input = <HTMLInputElement> document.querySelector('input[type="text"]');
console.log(input.value);
```

### TypeScript online editor
The TS online editor：[TypeScript Playground](https://www.typescriptlang.org/play?#code/Q)
Another online editor for TS： [playcode.io](https://playcode.io/typescript/)


### `LocalStorage`
- Save some data to 'key'
`localStorage.setItem('key', 'data');`
- Get the data from the 'key'
`const data = localStorage.getItem('key');`
- Remove specific key
`localStorage.removeItem('key');`
- Clear all data in the storage
`localStorage.clear();`


### others
1. download and use TS `$ npm init -y` to get all default options.
2. step 1 will create `package.json` file, where to put everything for dependencies and scripts inside of.
3. `$ npm install --save-dev typescript` install and save develop dependencies in package file.
4. `$ npx tsc --init` gives a boilerplate TS config file
5. `src` put TS file, `dest` put JS file that been transformed