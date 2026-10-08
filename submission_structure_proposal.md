# Proposed STACS Track A submission structure

This is a proposal for the 15-page structure. The formal hardness statements and proofs are now grouped in one dedicated section; the only bound removed from the current summary is the no-longer-needed \(\sqrt{2}-\varepsilon\) GPD hardness bound.

## Submission constraints

The current STACS 2027 submission instructions require LIPIcs formatting and a maximum of 15 pages for the paper body. The title page, references, and a possible appendix are excluded. The title page must contain the title and abstract but no author information; the main text starts on the following page. Proofs omitted from the page-limited text may be placed in an appendix, and an anonymized full version as an appendix is encouraged. See the [STACS 2027 submission instructions](https://events.gwdg.de/event/1460/page/476-submissions) and the downloaded [LIPIcs author guidelines](./lipics-template/lipics-v2021-authors-guidelines.pdf).

The conference uses lightweight double-blind review. Keep identifying author and affiliation details out of the submitted PDF. The LIPIcs version uses its `anonymous` class option. The CFP also requires disclosure and a detailed description if AI tools were used to conduct research; include that disclosure in the final submission if applicable.

## Suggested 15-page body

| Part | Target | Content to prioritize |
|---|---:|---|
| 1. Introduction and result map | 1.5 pages | Motivate GPD/HCD and define the contribution hierarchy. State the headline general-graph, tree, and hardness results without repeating technical setup. |
| 2. Minimal preliminaries | 0.75 page | Keep only notation and definitions needed for generalized conductance, GPD, and HCD. Move routine identities and notation details to the appendix. |
| 3. Generalized conductance | 2.75 pages | Define GC; state the general-graph approximation and exact supply-tree result (`thm:generalized-conductance-approx`, `thm:tree-generalized-conductance`). Give the key reduction/algorithm idea and a short proof sketch. State the inapproximability consequence concisely. |
| 4. General-graph applications | 2.25 pages | Keep the GPD bicriteria guarantee and its parameter extension, then the HCD transfer result (`thm:gpd-bicriteria`, `thm:gpd-extension`, `cor:graph-partitioning-approximation`, `thm:hc-gpd-transfer`, `cor:hc-general-bounds`). Use one compact proof sketch to explain the dependence on GC. |
| 5. Supply-tree algorithms | 3.75 pages | Focus on the separator/maximum-coverage recursion and the full-quota \((4+\epsilon)\)-approximation, with their main corollaries (`thm:tree-centroid-max-coverage`, `thm:tree-centroid-full-quota`, `cor:tree-best-guarantee`, `cor:tree-hc-improved`). |
| 6. Hardness of approximation | 2 pages | Collect all lower-bound statements here: GC (`cor:generalized-conductance-hardness`), GPD (`thm:sse-gpd-bicriteria-hardness`, `cor:tree-gpd-hardness`), and HCD (`thm:sse-hcd-hardness`, `thm:hc-star-hardness`). Keep the table in the introduction to bound/reference entries only; use the appendix for long proofs if needed. |
| 7. Conclusion | 0.5 page | Summarize the main consequences and give only the most important open directions. |
| **Planned body total** | **13.5 pages** | Leaves approximately 1.5 pages of margin for figures, algorithms, and proof-sketch expansion. |

The title/abstract page, bibliography, and appendix are outside this 15-page body budget under the current CFP. Start the appendix on a new page after the references. Keep enough argument in the main text to make the stated results understandable and rigorously supported; the appendix should carry omitted proof details, not replace the exposition of the main contributions.

## Results and proof material to move out of the main text

These are recommendations for the later, shortened submission. The theorem statements and proofs for the hardness results are now together in the dedicated hardness section. Prefer putting omitted proof details and supporting results in the appendix so the full technical record remains available to the program committee.

1. **Move the alternative tree-algorithm chains to the appendix.** They are substantial parallel approaches alongside the two tree results prioritized above:
   - Anchored-LP chain: `lem:tree-anchored-relaxation`, `thm:tree-anchored-rounding`, and `cor:tree-general-demand-bicriteria`.
   - Weighted-budget chain: `lem:weighted-budget-rounding`, `thm:weighted-budget-dp`, `thm:tree-weighted-budget-direct`, `lem:weighted-budget-demand-degree`, and `thm:tree-weighted-budget-recursive`.
   
   In the main text, mention these approaches briefly only if they are needed to explain the scope of the contribution. If space is still tight, omit their theorem statements from the body and leave them in the appendix/full version.

2. **Move technical lemmas supporting the tree proofs to the appendix.** In particular, move the detailed statements/proofs for `lemma:tree_edge_weight_sum`, `lemma:tree-demand-pair-cover`, and `lem:tree-separator`. The main text can retain a brief structural claim or proof sketch where needed to support the two selected tree theorems.

3. **Keep the final SSEH hardness statements, but move their construction lemmas and proofs.** Move `lem:globalized-long-code-gap`, `lem:multiplicative-demands-encode-measure`, `lem:sse-gpd-completeness`, `lem:group-small-components`, and `lem:sse-gpd-soundness` to the appendix. Cite the background theorem `thm:rst-global-expansion` rather than reproducing its proof.

4. **Keep all hardness results together.** The statements `thm:tree-gpd-vertex-cover-hardness`, `cor:tree-gpd-hardness`, and `thm:hc-star-hardness` now sit in the same hardness section as the GC and SSEH-based GPD/HCD results. Keep the final bounds there; move the longer reduction proofs to the appendix if needed for the page limit.

5. **Shorten, but do not suppress, proofs of the headline results.** Keep concise derivations or proof sketches for the GC approximation, the principal GPD/HCD transfers, and the two selected tree algorithms. Put their full technical proofs—including supporting lemmas such as `lem:ABpartition`—in the appendix. This preserves a rigorous main-text argument while using the appendix for details expressly allowed by the CFP.

The proposed priority is therefore: **GC as the core contribution; its general-graph GPD/HCD applications; the strongest tree algorithms; and compact statements of the hardness results.** The LIPIcs conversion deliberately retains the current full section sequence so these proposed omissions remain decisions for a later revision.
