# Smart Meter Data Collector Configurator Frontend

## Introduction

The web interface is built with the [Vue.js 2.x](https://vuejs.org/) framework. Additionally, the following libraries and frameworks are used:
* [Buefy](https://buefy.org/): Lightweight UI components for Vue.js based on Bulma.
* [Axios](https://github.com/axios/axios): Promise based HTTP client for API to backend.
* [Fontawesome Free](https://fontawesome.com/): Icon package.

## Development

### Project Setup

Install latest LTS [nodejs (version 16.x.x)](https://nodejs.org/en/) which also installs the Node Package Manager `npm`.

Setup the project running
```
npm install --dev
```
inside the `frontend/smartmeter-datacollector-configurator` directory.

For development use
```
npm run serve
```
that compiles and hot-reloads the application.

### Prepare for production

Run the linter and formatter with 
```
npm run lint
```
before committing your changes.

If you require the minified build output of the fronted run
```
npm run build
```
which generates a `dist` directory with the static files.

## Customize Vue CLI configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
