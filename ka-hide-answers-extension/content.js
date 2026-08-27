// Add style to always blur multiple choice answers
const style = document.createElement('style')
style.textContent = `
.perseus-widget-container legend + div {
  filter: blur(10px);
}
`
document.head.appendChild(style)

// Invoke callback on first mutation, then re-attach mutation observer after small delay
function observeSuccessive(target, callback) {
  const observer = new MutationObserver((list, obs) => {
    callback(target)
    obs.disconnect()

    setTimeout(() => observeSuccessive(target, callback), 1000)
  })
  observer.observe(target, {
    childList: true,
    subtree: true,
  })
}

// Add button to each 'Choose N answer(s)' legend which reveals answers when clicked
const enhanceLegends = (container) => {
  const legends = container.querySelectorAll('.perseus-widget-container legend')
  if (legends.length === 0) return

  legends.forEach(legend => {
    legend.style.padding = '0.2em'
    legend.style.border = '1px dashed #aaa'
    legend.style.cursor = 'pointer'
    legend.addEventListener('click', () => {
      // Assume the next sibling is the multiple choice container
      legend.nextElementSibling.style.filter = 'none'
    })
  })
}

const enhanceContentPanel = () => {
  const contentPanel = document.getElementById('content-library-content-panel')

  // Try again if contentPanel hasn't yet been loaded
  if (contentPanel === null) {
    setTimeout(enhanceContentPanel, 1000)
    return
  }

  console.log('Content panel:', contentPanel)

  enhanceLegends(contentPanel)
  // Enhance legend every time a new question is loaded
  observeSuccessive(contentPanel, enhanceLegends)
}

setTimeout(enhanceContentPanel, 1000)
