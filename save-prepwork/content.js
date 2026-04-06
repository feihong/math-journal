/*
Script to execute inside page
*/

const ELEMENT_TO_SCREENSHOT = '.aops-scrollbar-not-visible'

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

const getBlob = canvas => new Promise(resolve => canvas.toBlob(resolve))

const getBase64String = blob => new Promise(resolve => {
  const reader = new FileReader()
  reader.onloadend = () => resolve(reader.result)
  reader.readAsDataURL(blob)
})

async function main() {
  // Temporarily get rid of UI other than the prep work content
  let originalContent = document.body.innerHTML
  let title = document.querySelector('h3.title').textContent
  document.body.innerHTML = document.querySelector(ELEMENT_TO_SCREENSHOT).innerHTML
  const h1 = document.createElement('h1')
  h1.innerHTML = title
  document.body.prepend(h1)

  await sleep(100)

  // Get canvas from document body
  const canvas = await html2canvas(document.body)
  const blob = await getBlob(canvas)
  console.log(blob)

  const dataUrl = await getBase64String(blob)

  await chrome.runtime.sendMessage({ title, dataUrl })
  console.log('Sent image data back to service worker')

  // Restore page to original state
  // document.body.innerHTML = originalContent
}

main()
