// Sahayak Popup Script

document.addEventListener('DOMContentLoaded', () => {
  checkBackendStatus();
  
  // Activate assistant button
  document.getElementById('activate-btn').addEventListener('click', () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.tabs.sendMessage(tabs[0].id, { action: 'showAssistant' });
      window.close();
    });
  });
  
  // Check backend button
  document.getElementById('backend-btn').addEventListener('click', () => {
    checkBackendStatus();
  });
});

async function checkBackendStatus() {
  const statusEl = document.getElementById('backend-status');
  const indicatorEl = document.getElementById('backend-indicator');
  const alertEl = document.getElementById('backend-alert');
  
  statusEl.textContent = 'Checking...';
  indicatorEl.className = 'status-indicator';
  
  try {
    const response = await fetch('http://localhost:5000/api/health');
    const data = await response.json();
    
    if (data.status === 'healthy') {
      statusEl.textContent = 'Connected ✓';
      indicatorEl.className = 'status-indicator connected';
      alertEl.classList.remove('show');
    } else {
      throw new Error('Backend unhealthy');
    }
  } catch (error) {
    statusEl.textContent = 'Not Connected ✗';
    indicatorEl.className = 'status-indicator disconnected';
    alertEl.classList.add('show');
  }
}