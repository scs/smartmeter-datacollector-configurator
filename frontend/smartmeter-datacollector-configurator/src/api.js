import { getApiUrl } from "./utils";

class ApiError extends Error {
  constructor(message, { status = null, data = null, isResponse = false } = {}) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
    this.isResponse = isResponse;
  }
}

function buildAuthHeader(auth) {
  if (!auth) {
    return {};
  }
  const encoded = btoa(`${auth.username}:${auth.password}`);
  return { Authorization: `Basic ${encoded}` };
}

async function request(
  path,
  { method = "GET", body = null, auth = null, timeout = 3000, responseType = null, contentType = null } = {},
) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);

  const headers = { ...buildAuthHeader(auth) };
  if (contentType) {
    headers["Content-Type"] = contentType;
  }

  let response;
  try {
    response = await fetch(`${getApiUrl()}${path}`, {
      method,
      headers,
      body,
      signal: controller.signal,
    });
  } catch {
    throw new ApiError("Request failed.", { isResponse: false });
  } finally {
    clearTimeout(timer);
  }

  const text = await response.text();
  let data = text;
  if (responseType === "json" && text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = text;
    }
  }

  if (!response.ok) {
    throw new ApiError(response.statusText, {
      status: response.status,
      data,
      isResponse: true,
    });
  }

  return data;
}

function getTtyDevices() {
  return request("/ttydevices", { responseType: "json", timeout: 3000 });
}

function getConfig(auth) {
  return request("/config", { responseType: "json", timeout: 3000, auth });
}

function postConfig(configJson, auth) {
  return request("/config", {
    method: "POST",
    body: configJson,
    contentType: "application/json",
    timeout: 4000,
    auth,
  });
}

function restartDatacollector(auth) {
  return request("/restart", { method: "POST", timeout: 6000, auth });
}

function restartDemo(auth) {
  return request("/restart-demo", { method: "POST", timeout: 8000, auth });
}

function changePassword(newPassword, auth) {
  return request("/credentials", {
    method: "POST",
    body: newPassword,
    contentType: "text/plain",
    timeout: 4000,
    auth,
  });
}

export { ApiError, getTtyDevices, getConfig, postConfig, restartDatacollector, restartDemo, changePassword };
