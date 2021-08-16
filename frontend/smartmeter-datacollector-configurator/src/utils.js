const devMode = process.env.NODE_ENV === "development";
const devBaseUrl = "http://localhost:8000/api";

function getBaseHostUrl() {
  if (devMode) {
    return devBaseUrl;
  }
  return `http://${location.host}/api`;
}

export { getBaseHostUrl };
