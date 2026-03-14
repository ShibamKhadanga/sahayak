// Sahayak Background Service Worker

chrome.runtime.onInstalled.addListener((details) => {
  console.log('Sahayak AI Co-Pilot installed', details);
  if (details.reason === 'install') {
    chrome.storage.local.set({ installDate: Date.now(), version: '3.0.0' });
  }
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'checkBackend') {
    fetch('http://localhost:5000/api/health')
      .then(r => r.json())
      .then(data => {
        sendResponse({ connected: true, data });
        chrome.storage.local.set({ backendConnected: true });
      })
      .catch(error => {
        sendResponse({ connected: false, error: error.message });
        chrome.storage.local.set({ backendConnected: false });
      });
    return true;
  }
  return false;
});