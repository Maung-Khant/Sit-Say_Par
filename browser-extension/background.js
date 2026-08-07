// background.js
chrome.runtime.onInstalled.addListener(() => {
  console.log("Extension installed, creating context menu...");
  chrome.contextMenus.create({
    id: "scanWithSitSayPar",
    title: "Scan with Sit-Say Par",
    contexts: ["link", "selection"]
  }, () => console.log("Context menu created"));
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  console.log("Context menu clicked!", info);
  let url = info.linkUrl || info.selectionText;
  console.log("URL extracted:", url);
  if (url) {
    url = url.trim();
    fetchResult(url);
  }
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "analyzeUrl") {
    fetchResult(request.url).then(sendResponse);
    return true;
  }
});

async function fetchResult(url) {
  console.log("fetchResult called with:", url);
  const apiUrl = "https://sit-say-par.onrender.com/analyze";
  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url })
    });
    const data = await response.json();
    console.log("API response:", data);
    // Show notification
chrome.notifications.create({
  type: "basic",
  iconUrl: "icons/icon48.png",
  title: "Sit-Say Par Result",
  message: `Risk: ${data.risk_level} (${data.risk_score}/100)\n${data.explanation.split('\n').slice(0,2).join(' ')}...`,
  requireInteraction: true
}, (notificationId) => {
  console.log("Notification created:", notificationId);
});
    return data;
  } catch (error) {
    console.error("Error scanning URL:", error);
    return { error: "Scan failed" };
  }
}