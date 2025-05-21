
mathjax = """
<script>
MathJax = {
  svg: {
    fontCache: 'global'
  }
};
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
</script>
"""

pyscript = """
<link rel="stylesheet" href="https://pyscript.net/releases/2025.3.1/core.css" />
<script type="module" src="https://pyscript.net/releases/2025.3.1/core.js"></script>
"""

# It's not recommended to use KaTeX because its support for TeX commands is a bit too limited. For example, it can't
# handle mbox.
# https://katex.org/docs/autorender.html
# https://github.com/KaTeX/KaTeX/blob/main/contrib/auto-render/auto-render.js
katex = """
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.css" integrity="sha384-5TcZemv2l/9On385z///+d7MSYlvIEw9FuZTIdZ14vJLqWphw7e7ZPuOiCHJcFCP" crossorigin="anonymous">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.js" integrity="sha384-cMkvdD8LoxVzGF/RPUKAcvmm49FQ0oxwDF3BGKtDXcEc+T1b2N+teh/OJfpU0jr6" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/contrib/auto-render.min.js" integrity="sha384-hCXGrW6PitJEwbkoStFjeJxv+fSOOQKOPbJxSfM6G5sWZjAyWhXiTIIAmQqnlLlh" crossorigin="anonymous"
    onload="renderMathInElement(document.body);"></script>
"""
