// Hide 'ready for next' ad banner, make log panel much taller.
// Since small flicker is acceptable, so no need to use mutation observer.
setTimeout(() => {
  // Hide tall ad banner
  const banner = document.querySelector('.ready-for-next')
  banner.style.display = 'none'

  const logPanel = document.querySelector('.alc-log-panel')

  // Make log panel title clickable
  const title = logPanel.querySelector('h1')
  title.style.cursor = 'pointer'
  title.addEventListener('click', () => {
    copyLogsDataToClipboard()
    title.textContent = 'Log (copied)'
    setTimeout(() => title.textContent = 'Log', 2000)
  })

  const body = logPanel.querySelector('.aops-scroll-outer')

  // Make log panel body taller
  body.style.height = '400px'

  // Keep body taller
  const observer = new MutationObserver(() => {
    // console.log('Adjust height')
    body.style.height = '400px'
  })
  observer.observe(body, { attributes: true })
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

const htmlToText = (htmlString) => {
  const parser = new DOMParser();
  const doc = parser.parseFromString(htmlString, 'text/html');
  return doc.body.textContent || "";
}

const getLogsMarkdown = (logs) => {
  const dateMap = {}

  for (const log of logs) {
    // If trial_id is undefined, then it's an achievement
    if (log.data.trial_id === undefined) continue

    const [date, time] = log.happened_at.split(' ')
    const item = {
      trialId: log.data.trial_id,
      time: time.substring(0, 5),
      text: htmlToText(log.data.problem_text_short),
    }

    if (date in dateMap) {
      dateMap[date].unshift(item)
    } else {
      dateMap[date] = [item]
    }
  }

  const lines = []
  for (const [date, items] of Object.entries(dateMap)) {
    lines.push(`# ${date}`)
    for (const { trialId, time, text } of items) {
      lines.push(`- [${time}](https://artofproblemsolving.com/alcumus/report/me/trial/${trialId}) - ${text}`)
    }
  }
  return lines.join('\n')
}

async function copyLogsDataToClipboard() {
  const logs = AoPS.bootstrap_data.alc_init_data.user.logs
  const markdown = getLogsMarkdown(logs)
  await navigator.clipboard.writeText(markdown)
  console.log('Copied to clipboard:\n\n' + markdown)
}

async function main() {
  if (isPastProblemUrl(location.pathname)) {
    hideSolution()

    // Hide solution even if navigating to new page
    window.navigation.addEventListener('navigate', (event) => {
      if (isPastProblemUrl(event.destination.url)) {
        hideSolution()
      }
    })
  }
}

main()
