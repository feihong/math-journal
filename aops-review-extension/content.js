const makeButton = (label, parent, callback) => {
  const btn = document.createElement('button')
  btn.style.fontSize = '0.7em'
  btn.textContent = label
  btn.addEventListener('click', callback)
  if (parent) {
    parent.appendChild(btn)
  }
  return btn
}

const sleep = (ms) => new Promise((resolve, _reject) => setTimeout(resolve, ms))

const pollElement = async (cssSelector, options, callback) => {
  if (options.delay) {
    await sleep(options.delay)
  }

  const interval = options.interval || 200
  let counter = options.timeout || 10_000
  while (true) {
    const node = document.querySelector(cssSelector)
    if (node !== null) {
      callback(node)
      return
    }
    await sleep(interval)
    counter -= interval
    if (counter <= 0) return
  }
}

const showShowSolutionButton = () => {
  pollElement('.alc-solution-box', { delay: 500 }, target => {
    // Don't add button if it's already been added
    if (target.previousElementSibling && target.previousElementSibling.tagName !== 'BUTTON') {
      console.log('show "show solution" button')
      const btn = makeButton('Show solution', null, () => target.style.filter = 'none')
      target.before(btn)
    }
  })
}

function isPastProblemUrl(url) {
  return url.match(/\/alcumus\/report\/me\/trial\/.*/) !== null
}

const domParser = new DOMParser();

const htmlToText = (htmlString) => {
  const doc = domParser.parseFromString(htmlString, 'text/html');
  return doc.body.textContent || "";
}

const getTrialsGroupedByDate = () => {
  const infos = trials.values()
    .map(trial => {
      const [date, time] = trial.trial_date.split(' ')
      return {
        trialId: trial.trial_id,
        date,
        time: time.substring(0, 5),
        topicIds: trial.topic_id_list,
        text: htmlToText(trial.problem_text_short),
      }
    })

  const groups = Object.groupBy(infos, ({ date }) => date)
  const entries = Object.entries(groups)
  // Most recent first
  entries.sort((a, b) => b[0].localeCompare(a[0]))
  return entries.map(entry => {
    const trials = entry[1]
    trials.sort((a, b) => b.time.localeCompare(a.time))
    return entry
  })
}

const getTrialsMarkdown = (days) => {
  const entries = getTrialsGroupedByDate().slice(0, days)

  const lines = []
  for (const [date, trials] of entries) {
    lines.push(`# ${date}`)
    for (const trial of trials) {
      lines.push('- [ ] ' + trialToMarkdown(trial))
    }
  }
  return lines.join('\n')
}

const trialToMarkdown = ({ time, trialId, text, topicIds }) => {
  const topicsStr = topicIds.map(id => topics.get(id)).join('/')
  return `[${time} ${topicsStr}](https://artofproblemsolving.com/alcumus/report/me/trial/${trialId}) - ${text}`
}

async function copyToClipboard(text) {
  await navigator.clipboard.writeText(text)
  console.log('Copied to clipboard:\n\n' + text)
}

const addTrialExportUi = (pathname) => {
  if (pathname !== '/alcumus/report/me') return

  pollElement('.alc-report-problem-table h1', { delay: 500 }, target => {
    if (target.nextElementSibling && target.nextElementSibling.className === 'custom-log-export')
      return

    const template = document.createElement('template')
    template.innerHTML = `
      <div class="custom-log-export" style="display: flex; flex-direction: row; gap: 0.5em;">
        <button>copy</button>
        <input size="2" value="1">
        <span>days</span>
      </div>
    `
    const div = template.content.firstElementChild
    target.after(div)
    const copyBtn = div.querySelector('button')
    copyBtn.addEventListener('click', () => {
      const days = parseInt(div.querySelector('input').value)
      copyToClipboard(getTrialsMarkdown(days))
    })
  })
}

const topics = new Map()
const trials = new Map()

async function init() {
  // Redefine XMLHttpRequest.open to intercept response
  const originalOpen = XMLHttpRequest.prototype.open

  XMLHttpRequest.prototype.open = function (_method, url, ..._args) {
    // Listen for the request completion
    this.addEventListener('readystatechange', (event) => {
      const xhr = event.target

      if (xhr.readyState === 4) { // 4 means DONE
        if (url === '/m/alcumus/ajax.php' && xhr.getResponseHeader('content-type') === 'application/json') {
          const data = JSON.parse(xhr.responseText)
          if (data.response.trials) {
            for (const trial of data.response.trials) {
              // console.log(trial)
              trials.set(trial.trial_id, trial)
            }
          }
        }
      }
    })
    return originalOpen.apply(this, arguments)
  }

  for (const topic of AoPS.bootstrap_data.alc_init_data.user.topics) {
    topics.set(topic.topic_id, topic.name)
  }
  console.log(`Found ${topics.size} topics`)

  // Add style to blur solutions
  const style = document.createElement('style')
  style.textContent = `
      .alc-solution-box {
        filter: blur(10px);
      }

      /* Don't blur solutions on problem pages */
      .alc-problem-page-main .alc-solution-box {
        filter: none;
      }
    `
  document.head.appendChild(style)

  showShowSolutionButton()
  addTrialExportUi(location.pathname)

  window.navigation.addEventListener('navigate', (event) => {
    const pathname = new URL(event.destination.url).pathname
    console.log(`navigating to ${pathname}`)
    showShowSolutionButton()
    addTrialExportUi(pathname)
  })
}

init()
