const WINDOW_WIDTH = 800

async function start(tab) {
  const current = await chrome.windows.getCurrent()

  // Set the width of window to a specific value for consistency in PDFs
  await chrome.windows.update(current.id, {
    width: WINDOW_WIDTH,
    state: 'normal',
  })

  // Execute content.js in the context of the page
  await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: [ 'content.js' ],
  })
}

chrome.action.onClicked.addListener(start)
