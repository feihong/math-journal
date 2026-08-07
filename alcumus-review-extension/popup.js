const key = 'isActivated'

const btn = document.querySelector('button')
let isActivated = undefined

function update() {
  btn.innerHTML = isActivated ? "Disable" : "Enable"
}

async function main() {
  const result = await chrome.storage.local.get([key])
  isActivated = !!result.isActivated
  update()

  btn.addEventListener('click', async () => {
    isActivated = !isActivated
    await chrome.storage.local.set({ [key]: isActivated })
    update()

    setTimeout(() => window.close(), 500)
  })
}

main()
