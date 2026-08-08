const key = 'isActivated'

// This justs improves UI, so no need to use mutation observer. Small flicker is acceptable.
setTimeout(() => {
  const logPanel = document.querySelector('.alc-log-panel .aops-scroll-outer')

  // Make Log panel taller
  logPanel.style.height = '500px'

  // Hide tall ad banner
  const banner = document.querySelector('.ready-for-next')
  banner.style.display = 'none'

  const observer = new MutationObserver(() => {
    // console.log('Adjust height')
    logPanel.style.height = '500px'
  })
  observer.observe(logPanel, { attributes: true })
}, 500)

function hideSolution() {

  const observer = new MutationObserver((_mutations, obs) => {
    const target = document.querySelector('.alc-solution-box')
    if (target) {
      if (target.style.visibility === 'hidden') return

      target.style.visibility = 'hidden'

      // Add button to show the solution
      const btn = document.createElement('button')
      btn.innerHTML = 'Show solution'
      btn.addEventListener('click', () => target.style.visibility = 'visible')
      target.before(btn)

      obs.disconnect()
    }
  })
  observer.observe(document.body, { childList: true, subtree: true })
}

function isPastProblemUrl(url) {
  return url.match(/\/alcumus\/report\/me\/trial\/.*/) !== null
}

async function main() {
  if (isPastProblemUrl(location.pathname)) {
    console.log(location.href)

    const result = await chrome.storage.local.get([key])
    if (!result.isActivated) return

    hideSolution()

    window.navigation.addEventListener("navigate", (event) => {
      hideSolution()
      const url = event.destination.url
      if (isPastProblemUrl(url)) {
        console.log(url)
      }
    })
  }
}

main()
