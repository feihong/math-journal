/*
Script to execute inside page
*/
{
  const ELEMENT_TO_LIFT = '.aops-scrollbar-not-visible'

  async function main() {
    const pathname = window.location.pathname
    if (pathname.includes('/prepwork/')) {
      // Get rid of UI other than the prep work content
      let title = document.querySelector('h3.title').textContent
      document.body.innerHTML = document.querySelector(ELEMENT_TO_LIFT).innerHTML
      const h1 = document.createElement('h1')
      h1.innerHTML = title
      document.body.prepend(h1)
    }
  }

  main()
}
