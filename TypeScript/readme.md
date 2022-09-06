# Read Me

## TypeScript vs JavaScript
TypeScript is a *strict typed superset* of JavaScript, more like an improved version of JS.
`TS = JS + type system`  add features like increased readability, static compilation, intuitive interface etc. therefor, JS syntax is **legal** TS. 
TS **never** changes the runtime behavior of JS code, means that wherever run code in JS or TS, it is guaranteed to run the same way, even if TypeScript thinks that the code has type errors.

### Advantages of TS over JS
1. Optional static typing
2. Improved readability
3. Intellisense
4. New features

||JavaScript|TypeScript|
|-|--|--|
||Dynamically typed language, software will not treat type difference as errors up until run time| Optional static typing, once declared a variable doesn't change its type and can only take certain values. Compiler alerts developers to type related mistakes -> early bug catching & structured code|
||Few readability add-ons, lots of errors need to be detected manually|Static reading along, increased code optimization, offers clear categories for variable declaration-> early bug detection, stable code, defined types, more informative version of a code base|
|||increases the development speed|
||Lacks several important features| Type annotation, value for each static type will be checked automatically. Generics, let developer write a generalized form of method. Improved API documentation, has tools like vscode navigation and let developers to see parameter types automatically, track variables etc.
|Ecosystem|More tools that support||
|NPM Package||can integrate ts with node.js|
|Compilation||eventually transpile into js|
Popularity|the most popular language currently|
|Use Cases|1. Extra transpilation tax isn't an option. 2. Flexibility is a priority -> offers dynamic typing allows to create new functionality without sticking to same rules  3. framework unsupported|1. Large codebase -> bring code to a single standard 2. Needed static typing  3. Speed is priority -> speeds up the development process by catching bugs in real time|

## Run the code
in terminal, `tsc greeter.ts` -> generate a `greeter.js` javascript file that have same functionality. Create a `html` file to run this js code and open it in browser.

## [TypeScript Playground](https://www.typescriptlang.org/play?#code/Q)
The TS online editor.
Another online editor for TS[playcode.io](https://playcode.io/typescript/)