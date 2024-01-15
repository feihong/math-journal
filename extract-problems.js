/*
Extract problem text
*/
{
  const getTitle = function(header) {
    const textChunks = [...header.childNodes].map(node => node.wholeText?.trim())

    for (const text of textChunks) {
      if (text !== undefined && text !== "") {
        return text
      }
    }
    return undefined
  }

  const getTextChunks = function*(node) {
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

  const problems =
    [...document.querySelectorAll('.problem-cronus-wrapper-outer')]
    .map(node => {
      const title = getTitle(node.querySelector('.problem-header'))
      const body =
        [...getTextChunks(node.querySelector('.body'))].join('').trim()

      return {
        title: title,
        body: body,
      }
    })
  // console.log(problems)

  const problemText =
    problems.map(({title, body}) => `${title}\n${body}`).join('\n\n')

  console.log(problemText)
}
