/*
Convert logs into markdown code and put that code on the clipboard.

Code can then be pasted directly into Notion.
*/

async function main() {
  const htmlToText = (htmlString) => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlString, 'text/html');
    return doc.body.textContent || "";
  }

  const getLogsMarkdown = (logs) => {
    const dateMap = {}

    for (const log of logs) {
      const [date, time] = log.happened_at.split(' ')
      const item = {
        trialId: log.data.trial_id,
        time: time.substring(0, 5),
        text: htmlToText(log.data.problem_text_short),
      }

      // TODO: ignore logs with undefined trialId
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

  const logs = AoPS.bootstrap_data.alc_init_data.user.logs
  const markdown = getLogsMarkdown(logs)
  await navigator.clipboard.writeText(markdown)
  console.log('Copied to clipboard:\n\n' + markdown)
}

main()
