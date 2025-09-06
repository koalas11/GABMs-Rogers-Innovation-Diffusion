#import "unimib-template.typ": unimib
#import "packages.typ": codly, codly-languages

#show: unimib.with(
  title: "Simulating Rogers' Innovation Diffusion through GABMs",
  area: [Scuola di Scienze],
  department: [Dipartimento di Informatica, Sistemi e Comunicazione],
  course: [Corso di Scienze Informatiche],
  authors: (
    "Sanvito Marco 886493",
  ),
  bibliography: bibliography(style: "ieee", "citations.bib", full: true),
  abstract: include "abstract.typ",
  dark: false,
  lang: "en",
  // flipped: true
)


#show: codly.codly-init
#codly.codly(languages: codly-languages.codly-languages, breakable: true)

#set table(stroke: none, gutter: 0.2em, fill: (x, y) => {
  if y == 0 { luma(120) } else {
    if calc.odd(y) {
      luma(240)
    } else {
      luma(220)
    }
  }
})

#show table.cell: it => {
  if it.y == 0 {
    set text(white)
    strong(it)
  } else {
    it
  }
}

/*
#let MissingRef(body, small_text: 5pt) = {
      let body = if body == [] {
        [Missing Ref: XXX]
      } else {
        body
      }
      set text(fill: white, size: small_text, weight: "bold")
      text()[~~]
      box(
        fill: rgb("#e046d3"),
        outset: 4pt,
        radius: 3pt,
        stroke: luma(1),
        [#body #place()[    
          #set text(size: 0pt)    
          #figure(kind: "MissingRef", supplement: "", caption: body, []),
        ]])
      text()[~~]
}

#show ref: it => {
  if query(it.target).len() > 0 {
    it
  } else {
    MissingRef[Ref Missing #str(it.target)]

  }
}
*/

#set cite(form: "prose")

#set heading(numbering: none)

#set heading(numbering: "1.1.")

#include "chapters/01_ai_agents_introduction.typ"
#include "chapters/02_generative_agent_based_modeling.typ"
#include "chapters/03_rogers_innovation_theory.typ"
#include "chapters/04_simulation_implementation.typ"
#include "chapters/05_simulation_results.typ"
#include "chapters/06_conclusions_and_future_developments.typ"

#set heading(numbering: none)
