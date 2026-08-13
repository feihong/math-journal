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

const enhanceLegend = (container) => {
  const legend = container.querySelector('.perseus-widget-container legend')
  if (legend === null) return

  legend.style.padding = '0.2em'
  legend.style.border = '1px dashed #aaa'
  legend.style.cursor = 'pointer'
  legend.addEventListener('click', () => {
    legend.nextElementSibling.style.filter = 'none'
  })

}

setTimeout(() => {
  const contentPanel = document.getElementById('content-library-content-panel')

  enhanceLegend(contentPanel)
  observeSuccessive(contentPanel, enhanceLegend)
}, 1000)
