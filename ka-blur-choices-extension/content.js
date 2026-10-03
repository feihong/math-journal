const sleep = (ms) => new Promise((resolve, _reject) => setTimeout(resolve, ms))

const pollElement = async (cssSelector, options, callback) => {
  if (options.delay) {
    await sleep(options.delay)
  }

  const interval = options.interval || 1000
  let counter = options.timeout || 30_000
  while (true) {
    const nodes = document.querySelectorAll(cssSelector)
    if (nodes.length !== 0) {
      callback(nodes)
      return
    }
    await sleep(interval)
    counter -= interval
    if (counter <= 0) return
  }
}

const update = (url, delay) => {
  delay = delay ?? 1000
  if (url.match(/\/(?:e|quiz|test)\//) === null) return

  pollElement('.perseus-widget-container legend', { delay }, legends => {
    legends.forEach(legend => {
      legend.style.padding = '0.2em'
      legend.style.border = '1px dashed #aaa'
      legend.style.cursor = 'pointer'
      legend.addEventListener('click', () => {
        // Assume the next sibling is the multiple choice container
        legend.nextElementSibling.style.filter = 'none'
      })
    })
  })
}

const init = () => {
  // Add style to always blur multiple choice answers
  const style = document.createElement('style')
  style.textContent = `
  .perseus-widget-container legend + div {
    filter: blur(10px);
  }
  `
  document.head.appendChild(style)

  update(location.pathname)

  window.navigation.addEventListener('navigate', (event) => {
    update(event.destination.url)
  })

  // Proxy fetch function so we can update page whenever user presses 'Next question' button
  const fetchHandler = {
    apply: async function (target, thisArg, argumentsList) {
      const resource = argumentsList[0]
      if (typeof resource === 'object') {
        const url = new URL(resource.url)
        if (url.pathname === '/api/internal/_analytics/publish_event' && url.searchParams.get('type') === 'ContentLibraryNextQuestionButtonClicked') {
          update(location.pathname)
        }
      }
      return Reflect.apply(target, thisArg, argumentsList)
    }
  }

  const originalFetch = window.fetch
  window.fetch = new Proxy(originalFetch, fetchHandler)
  console.log('KA Blur Choices loaded')
}

init()