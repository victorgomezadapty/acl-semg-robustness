# v0.2.0: Independent ENABL3S methods audit

The original Dryad analysis showed that bilateral sEMG ratios depend on amplitude-summary choices. This release checks that dependence in a separate healthy walking dataset using rules fixed after one exploratory pilot.

Of nine non-pilot participants, six meet the fixed annotation, transition-margin and segment-length rules; three are excluded with trial-level reasons. All six have eleven valid primary RMS ratios, and two cross ratio 1 across specifications. Temporal matching, shared selections and alternative transition margins are reported separately, including undefined results and matched comparison subsets.

Includes an executable derived-results review notebook, reproduction scripts, source hashes, a downloadable source-and-results ZIP, figures, and attribution for ENABL3S (CC BY 4.0). Original measurements are obtained from the source repository rather than bundled here. Original project code/prose are MIT.

Validation: 27 tests; Ruff checks; notebook executed locally against the packaged artifacts. See `verification.json` for actual execution status and runtime. This does not establish clinical usefulness or scientific priority. Existing Kaggle publication is documented separately; the new notebook has not been published there.
