/*
Extract problem text
*/
{
  const getTitle = (header) => {
    const textChunks = [...header.childNodes].map(node => node.wholeText?.trim())

    for (const text of textChunks) {
      if (text !== undefined && text !== "") {
        return text
      }
    }
    return undefined
  }

  const getTextChunks = function* (node) {
    if (node instanceof Text) {
      yield node.wholeText
    } else if (node instanceof HTMLImageElement) {
      yield node.getAttribute('alt')
    } else {
      for (const child of node.childNodes) {
        yield* getTextChunks(child)
      }
    }
  }

  const indent = (s) => {
    const lines = s.split('\n').map(l => {
      if (l[0] == " " && l[1] == " ")
        return l
      else if (l[0] == " ")
        return " " + l
      else
        return "  " + l
    })
    return lines.join('\n')
  }

  const problems =
    [...document.querySelectorAll('.grid-tab-assignments-problem')]
      .map(node => {
        const title = getTitle(node.querySelector('.problem-header'))
        const anchorName = node.querySelector('a[name]').name
        const url = `https://${location.host}${location.pathname}#${anchorName}`
        const body =
          indent(Array.from(getTextChunks(node.querySelector('.body'))).join('').trim())

        return {
          title,
          url,
          body,
        }
      })
  // console.log(problems)

  const problemText =
    problems
      .map(({ title, body, url }) => `- [ ] [${title}](${url})\n${body}`)
      .join('\n\n')

  console.log(problemText)
}
