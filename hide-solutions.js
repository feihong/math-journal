{
  const getSolutions = function*(classes) {
    for (const class_ of classes) {
      yield* [...document.querySelectorAll(class_)]
    }
  }

  const classes = ['.Solution', '.Trials', '.Evaluation', '.FreeResponse']

  for (const solution of getSolutions(classes)) {
    solution.remove()
  }
}
