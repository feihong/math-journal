function getConfig(url) {
  if (url.includes('/prepwork/')) {
    return {
      windowWidth: 800,
      titleSelector: 'h3.title',
      contentSelector: '.aops-scrollbar-not-visible',
    }
  } else if (url.includes('/forum/')) {
    return {
      windowWidth: 700,
      titleSelector: '.cmty-topic-subject',
      contentSelector: '.cmty-post-middle',
      clearBackground: true,
      margin: '1em 1em 1em 3em',
    }
  } else if (url.includes('/homework/')) {
    return {
      windowWidth: 700
    }
  }
}

async function start(tab) {
  const current = await chrome.windows.getCurrent()

  const config = getConfig(tab.url)

  // Set the width of window to a specific value for consistency in PDFs
  await chrome.windows.update(current.id, {
    width: config.windowWidth,
    state: 'normal',
  })

  if (config.titleSelector && config.contentSelector) {
    // Get rid of all UI on the page other than the content
    await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      args: [config],
      func: ({ titleSelector, contentSelector, ...config }) => {
        const title = document.querySelector(titleSelector).textContent.trim()
        document.body.innerHTML = document.querySelector(contentSelector).innerHTML

        // Create h1 element and prepend to document body
        const h1 = document.createElement('h1')
        h1.innerHTML = title
        document.body.prepend(h1)

        if (config.clearBackground) {
          document.body.style.backgroundColor = 'white'
          document.body.style.backgroundImage = 'none'
        }

        if (config.margin) {
          document.body.style.margin = config.margin
        }
      },
    })
  }
}

chrome.action.onClicked.addListener(start)
