;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "treap_essencial"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("beamer" "aspectratio=169" "11pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("babel" "brazilian") ("inputenc" "utf8") ("fontenc" "T1") ("amsmath" "") ("amssymb" "") ("mathtools" "") ("tikz" "")))
   (add-to-list 'LaTeX-verbatim-environments-local "semiverbatim")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "href")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "C_macros"
    "beamer"
    "beamer11"
    "babel"
    "inputenc"
    "fontenc"
    "amsmath"
    "amssymb"
    "mathtools"
    "tikz")
   (TeX-add-symbols
    '("tri" 3)
    '("define" 1))
   (LaTeX-add-amsthm-newtheorems
    "proposicao"))
 :latex)

