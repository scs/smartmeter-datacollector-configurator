# Smart Meter Data Collector Configurator Frontend

## Introduction

The web interface is built with the [Vue 3](https://vuejs.org/) framework. Additionally, the following libraries and frameworks are used:
* [Buefy](https://buefy.org/): Lightweight UI components for Vue based on Bulma.
* [Fontawesome Free](https://fontawesome.com/): Icon package.

## Development

### Project Setup

Install latest LTS [nodejs (version 22.x.x)](https://nodejs.org/en/) using nvm (node version manager) which also installs the Node Package Manager `npm`.

Activate the required node version (in `.nvmrc`) in the shell
```
nvm use
```

Setup the project running
```
npm install --ignore-scripts --include=dev
```
inside the `frontend/smartmeter-datacollector-configurator` directory.

For development use
```
npm run dev
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
