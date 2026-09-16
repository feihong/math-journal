const makeButton = (label, parent, callback) => {
  const btn = document.createElement('button')
  btn.style.fontSize = '0.7em'
  btn.textContent = label
  btn.addEventListener('click', callback)
  parent.appendChild(btn)
  return btn
}

// Hide 'ready for next' ad banner, make log panel much taller.
const makeLogPanelMoreVisible = () => {
  console.log('Make log panel more visible')

  // Keep trying until you succeed
  const banner = document.querySelector('.ready-for-next')
  if (banner === null) {
    setTimeout(makeLogPanelMoreVisible, 200)
    return
  }

  // Hide tall ad banner
  banner.style.display = 'none'

  const logPanel = document.querySelector('.alc-log-panel')

  // Add buttons to log panel header
  const header = logPanel.querySelector('h1')
  header.style.display = 'flex'
  header.style.flexDirection = 'row'
  header.style.gap = '0.5em'

  makeButton('all', header, () => copyToClipboard(getAllLogsMarkdown()))
  makeButton('last', header, () => copyToClipboard(getLastLogMarkdown()))

  makeLogPanelTaller()
}

const makeLogPanelTaller = () => {
  console.log('Make log panel taller')

  const height = '400px'

  const logPanelBody = document.querySelector('.alc-log-panel .aops-scroll-outer')
  logPanelBody.style.height = height

  // There is some logic that keeps trying to make it shorter, so keep making it taller
  // Note that invoking this function inside update doesn't seem to help at all
  const observer = new MutationObserver(() => logPanelBody.style.height = height)
  observer.observe(logPanelBody, { attributes: true })
}

function hideAlcumusSolution() {
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

const domParser = new DOMParser();

const htmlToText = (htmlString) => {
  const doc = domParser.parseFromString(htmlString, 'text/html');
  return doc.body.textContent || "";
}

const getLogs = () => {
  return AoPS.bootstrap_data.alc_init_data.user.logs
    .filter(log => log.data.trial_id !== undefined)
    .map(log => {
      const [date, time] = log.happened_at.split(' ')
      return {
        trialId: log.data.trial_id,
        date,
        time: time.substring(0, 5),
        text: htmlToText(log.data.problem_text_short),
      }
    })
}

const getAllLogsMarkdown = () => {
  const logs = getLogs()

  const dateMap = {}

  for (const log of logs) {
    const date = log.date
    if (date in dateMap) {
      dateMap[date].unshift(log)
    } else {
      dateMap[date] = [log]
    }
  }

  const lines = []
  for (const [date, logs] of Object.entries(dateMap)) {
    lines.push(`# ${date}`)
    for (const log of logs) {
      lines.push('- [ ] ' + logToMarkdown(log))
    }
  }
  return lines.join('\n')
}

const logToMarkdown = ({ time, trialId, text }) => {
  return `[${time}](https://artofproblemsolving.com/alcumus/report/me/trial/${trialId}) - ${text}`
}

const getLastLogMarkdown = () => {
  const logs = getLogs()
  return logToMarkdown(logs[0])
}

async function copyToClipboard(text) {
  await navigator.clipboard.writeText(text)
  console.log('Copied to clipboard:\n\n' + text)
}

const update = (url) => {
  if (isPastProblemUrl(url)) {
    hideAlcumusSolution()
  }
}

async function main(url) {
  makeLogPanelMoreVisible()

  update(location.pathname)

  window.navigation.addEventListener('navigate', (event) => {
    update(event.destination.url)
  })
}

main()
