const devMode = process.env.NODE_ENV === "development";
const devApiPort = 8000;
const prodApiPort = 8000;
const apiPath = "/api";
const grafanaPort = 3000;

function getApiUrl() {
  if (devMode) {
    return `http://${location.hostname}:${devApiPort}${apiPath}`;
  }
  return `http://${location.hostname}:${prodApiPort}${apiPath}`;
}

function getGrafanaUrl() {
  return `http://${location.hostname}:${grafanaPort}`;
}

export { getApiUrl, getGrafanaUrl };
