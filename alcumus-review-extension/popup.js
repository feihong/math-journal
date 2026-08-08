const key = 'isActivated'

const btn = document.querySelector('button')
let isActivated = undefined

async function main() {
  const result = await chrome.storage.local.get([key])
  isActivated = !!result.isActivated
  btn.innerHTML = isActivated ? "Disable" : "Enable"

  btn.addEventListener('click', async () => {
    isActivated = !isActivated
    await chrome.storage.local.set({ [key]: isActivated })
    window.close()
  })
}

main()
