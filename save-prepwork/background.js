// https://developer.chrome.com/docs/extensions/reference/api/windows

const WINDOW_WIDTH = 1000

const getImageName = title => {
  // Extract week number
  let numStr = title.match(/Week (\d)+/)[1]
  numStr = numStr.padStart(2, '0')
  return `prepwork ${numStr}.png`
}

async function start(tab) {
  const current = await chrome.windows.getCurrent()

  // Set the width of window to a specific value for consistency in captured images
  await chrome.windows.update(current.id, {
    width: WINDOW_WIDTH,
    state: 'normal',
  })

  // Execute content.js in the context of the page
  await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: [ 'libs/html2canvas.min.js', 'content.js' ],
  })
}

// Handle image data sent from content script
async function handleMessage(message, sender, sendResponse) {
  if (message.title && message.dataUrl) {
    // Download the image
    const downloadId = await chrome.downloads.download({
      url: message.dataUrl,
      filename: getImageName(message.title),
      conflictAction: 'overwrite',
      saveAs: false // Set to true to show the "Save As" dialog
    })
    console.log('Download ID:', downloadId)
  }

  return true
}

chrome.action.onClicked.addListener(start)
chrome.runtime.onMessage.addListener(handleMessage)
