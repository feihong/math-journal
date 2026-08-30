const enhanceDelay = 500

// Add style to blur submitted answers and solutions
const style = document.createElement('style')
style.textContent = `
.ebk-sb-user-sub-final {
  border: 1px dashed #aaa;
  cursor: pointer;
}

.ebk-sb-user-sub-final p, .ebk-sb-solution {
  filter: blur(10px);
}
`
document.head.appendChild(style)

function enhance(submission, blur) {
  const filter = blur ? 'blur(10px)' : 'none'

  // console.log('Your submission:', submission)
  const para = submission.querySelector('p')
  para.style.filter = filter
  const solution = submission.nextElementSibling
  solution.style.filter = filter

  submission.addEventListener('click', () => {
    para.style.filter = 'none'
    solution.style.filter = 'none'
  })
}

function enhanceAll() {
  console.log('enhanceAll')
  const submissions = document.querySelectorAll('.ebk-sb-user-sub-final');
  if (submissions.length === 0) {
    setTimeout(enhanceAll, enhanceDelay)
    return
  }

  document.querySelectorAll('.ebk-sb-user-sub-final').forEach(sub => enhance(sub, true))

  // Enhance Show Solution buttons
  document.querySelectorAll('.ebk-sb--show-sol').forEach(btn => {
    const main = btn.closest('.ebk-sb--main')
    btn.addEventListener('click', () => {
      setTimeout(() => {
        const submission = main.querySelector('.ebk-sb-user-sub-final')
        enhance(submission, false)
      }, 1000)
    }, { once: true })
  })
}

setTimeout(enhanceAll, enhanceDelay)
