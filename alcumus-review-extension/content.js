const key = 'isActivated'

const observer = new MutationObserver((_mutations, obs) => {
  const target = document.querySelector('.alc-solution-box')

  if (target) {
    target.style.visibility = 'hidden'

    // Add button to show the solution
    const btn = document.createElement('button')
    btn.innerHTML = 'Show solution'
    btn.addEventListener('click', () => target.style.visibility = 'visible')
    target.before(btn)

    // Hide tall ad banner
    const banner = document.querySelector('.ready-for-next')
    console.log(banner)
    banner.style.display = 'none'

    // Make Log panel taller
    const logPanel = document.querySelector('.alc-log-panel .aops-scroll-outer')
    logPanel.style.height = '500px'

    obs.disconnect()
  }
})

async function main() {
  const result = await chrome.storage.local.get([key])
  isActivated = !!result.isActivated
  if (isActivated) {
    observer.observe(document.body, { childList: true, subtree: true })
  }
}

main()
