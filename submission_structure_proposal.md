# Proposed STACS Track A submission structure

This is a proposal for a 15-page STACS Track A submission. Assume the title/abstract page, introduction, and preliminaries together occupy just under five pages, as in the current draft, and will not shrink substantially. Put all hardness results, including their statements, in the appendix; the main-text result map should focus on the algorithmic contributions.

## Submission constraints

The current STACS 2027 submission instructions require LIPIcs formatting and a maximum of 15 pages for the paper body. The title page, references, and a possible appendix are excluded. The title page must contain the title and abstract but no author information; the main text starts on the following page. Proofs omitted from the page-limited text may be placed in an appendix, and an anonymized full version as an appendix is encouraged. See the [STACS 2027 submission instructions](https://events.gwdg.de/event/1460/page/476-submissions) and the downloaded [LIPIcs author guidelines](./lipics-template/lipics-v2021-authors-guidelines.pdf).

The conference uses lightweight double-blind review. Keep identifying author and affiliation details out of the submitted PDF. The LIPIcs version uses its `anonymous` class option. The CFP also requires disclosure and a detailed description if AI tools were used to conduct research; include that disclosure in the final submission if applicable.

## Suggested 15-page body

| Part | Target | Content to prioritize |
|---|---:|---|
| 1. Introduction and algorithmic result map | 4 pages | Motivate GPD/HCD, explain generalized conductance as the organizing tool, and state the algorithmic contributions. Keep the result table to upper bounds; do not state hardness results in the main text. |
| 2. Preliminaries | 0.75 page | Retain only notation and definitions needed for generalized conductance, GPD, and HCD. Together with the title/abstract page and introduction, target just under five pages total, with little expected reduction. |
| 3. Generalized conductance | 1.75 pages | Define GC; state the general-graph approximation and exact supply-tree result (`thm:generalized-conductance-approx`, `thm:tree-generalized-conductance`). Explain the key reduction and give a concise proof sketch. |
| 4. General-graph applications | 4 pages | Present the GPD bicriteria guarantee and parameter extension, then the HCD transfer (`thm:gpd-bicriteria`, `thm:gpd-extension`, `cor:graph-partitioning-approximation`, `thm:hc-gpd-transfer`, `cor:hc-general-bounds`). Use compact proof sketches to explain the dependence on GC. |
| 5. Supply-tree algorithms | 4.5 pages | Focus on the separator/maximum-coverage recursion and the full-quota \((4+\epsilon)\)-approximation, with their main corollaries (`thm:tree-centroid-max-coverage`, `thm:tree-centroid-full-quota`, `cor:tree-best-guarantee`, `cor:tree-hc-improved`). |
| **Planned body total** | **15 pages** |

The title/abstract page, bibliography, and appendix are outside this 15-page body budget under the current CFP. Start the appendix on a new page after the references. Keep enough argument in the main text to make the algorithmic results understandable and rigorously supported; the appendix should contain all hardness results as well as omitted proof details.

## Results and proof material to move out of the main text

These are recommendations for the shortened submission. Move the following material out of the 15-page body while keeping the full technical record available to the program committee.

1. **Move the alternative tree-algorithm chains to the appendix.** They are substantial parallel approaches alongside the two tree results prioritized above:
   - Anchored-LP chain: `lem:tree-anchored-relaxation`, `thm:tree-anchored-rounding`, and `cor:tree-general-demand-bicriteria`.
   - Weighted-budget chain: `lem:weighted-budget-rounding`, `thm:weighted-budget-dp`, `thm:tree-weighted-budget-direct`, `lem:weighted-budget-demand-degree`, and `thm:tree-weighted-budget-recursive`.
   
   In the main text, mention these approaches briefly only if they are needed to explain the scope of the contribution. If space is still tight, omit their theorem statements from the body and leave them in the appendix/full version.

2. **Move technical lemmas supporting the tree proofs to the appendix.** In particular, move the detailed statements/proofs for `lemma:tree_edge_weight_sum`, `lemma:tree-demand-pair-cover`, and `lem:tree-separator`. The main text can retain a brief structural claim or proof sketch where needed to support the two selected tree theorems.

3. **Move every hardness result to the appendix.** This includes the statements and proofs for GC (`cor:generalized-conductance-hardness`), GPD (`thm:sse-gpd-bicriteria-hardness`, `cor:tree-gpd-hardness`, `thm:tree-gpd-vertex-cover-hardness`), and HCD (`thm:sse-hcd-hardness`, `thm:hc-star-hardness`), as well as all reduction details. Move `lem:globalized-long-code-gap`, `lem:multiplicative-demands-encode-measure`, `lem:sse-gpd-completeness`, `lem:group-small-components`, and `lem:sse-gpd-soundness` with them. Keep the main-text results table limited to algorithmic upper bounds, and avoid stating hardness bounds in the introduction. Cite `thm:rst-global-expansion` rather than reproducing its proof.

4. **Shorten proofs of the headline algorithmic results.** Keep concise derivations or proof sketches for the GC approximation, the principal GPD/HCD transfers, and the two selected tree algorithms. Put full technical proofs—including supporting lemmas such as `lem:ABpartition`—in the appendix. This preserves a rigorous main-text argument while using the appendix for details expressly allowed by the CFP.

The proposed priority is therefore: **GC as the core contribution; its general-graph GPD/HCD applications; and the strongest tree algorithms.** Move the current main-text hardness section to the appendix in full, and revise the introduction's result table to omit lower bounds.
