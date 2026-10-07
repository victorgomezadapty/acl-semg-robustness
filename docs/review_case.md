# When a limb-symmetry number depends on how the signal is measured

For the reasoning behind each choice, read the [decision record](decision_log.md). To run the same analysis, follow the [reproduction guide](reproducibility.md).

## The problem

A comparison between legs can look straightforward: measure a signal on each side, divide one value by the other and interpret the result. But that number depends on what was recorded and how the recording was summarized. A short quiet segment or a large isolated spike can change the answer before any clinical interpretation begins.

I investigated this problem using a public [dataset from Gutierrez, Hart and Boukhechba (2022)](https://doi.org/10.5061/dryad.66t1g1k4j). It contains recordings from 12 people after ACL reconstruction and 10 healthy controls. The available files provide surface electromyography, or sEMG: an electrical signal recorded over the vastus lateralis, part of the quadriceps. They include both legs and two measurement conditions, giving 88 recordings. My question was: **how much does the interpretation of a bilateral sEMG ratio depend on the way we summarize the signal?**

## What I did

I first checked the source files against their published digital fingerprints, inspected their structure and retained the original recordings. I removed only empty padding at the ends. This made the analysis traceable to the downloaded data rather than a manually edited spreadsheet.

Next, I compared 21 explicit ways of summarizing amplitude. These included whole-record RMS, a measure that gives greater weight to larger values; average absolute amplitude; a version limiting unusually large values; and summaries of selected signal blocks. I also repeated the calculations after subtracting each recording's average value, and again after a standard 20–450 Hz band-pass filter. The authors do not state the sampling rate, but the clocks imply similar average rates (median 1,925.9 Hz), allowing a conditional filtering sensitivity analysis; uniform acquisition remains an assumption. Each participant remained a person in the analysis: thousands of samples and multiple processing choices were never treated as thousands of patients.

One pair needed a decision. In `healthy8`/`iso90`, the `uninv` recording lasts only 2 seconds; the next shortest of all 88 lasts 10.5 seconds, and its partner lasts about 25. Comparing a whole task with a short fragment does not compare like with like, so I left this pair out of the main results (43 pairs) and kept it in every sensitivity analysis.

Finally, I constructed synthetic signals whose starting ratio was known. I introduced pauses, spikes, noise and differences in sensor scaling, then repeated each scenario 100 times. This let me examine processing errors against a defined reference, something the patient recordings alone cannot provide.

## Four figures that explain the findings

### 1. One recording pair can support different directions

![Ratio sensitivity across processing choices](../reports/figures/robustness_matrix.png)

Each row represents one participant in one condition; each column represents a summary method. The colors show whether the exported `inv` signal is larger or smaller than `uninv`. Across all 21 methods, 13 of the 43 main pairs switch sides of a ratio of one. Restricting the comparison to the 11 RMS methods leaves 10 such pairs. The excluded `healthy8` pair does not switch, so including it changes neither count.

The practical point is to inspect how much a conclusion changes across reasonable summaries. A small crossing of one is counted here, so these switches are descriptive changes, not evidence that a clinical decision should change.

### 2. Removing the average does not solve every unusual ratio

![Ratios before and after removing the record mean](../reports/figures/centering_ratio_sensitivity.png)

The dashed line represents no change after centering. Most points stay close to it, and none of the 44 whole-RMS ratios reverses direction. The excluded `healthy8`/`iso90` pair remains extreme: its ratio increases from 25.21 to 46.51.

This happens because subtracting the average reduces the already small value in the bottom of the ratio: the average accounts for about 70.7% of that recording's mean-square value. Together with its 2-second length, this is why the pair was set aside. The files cannot tell us whether it reflects a truncated export, a failed trial or an acquisition problem.

### 3. Group medians can hide individual processing changes

![Band-pass sensitivity and RMS retention](../reports/figures/bandpass_sensitivity.png)

The left panel compares each pair's ratio before and after the 20–450 Hz filter. Only one of 43 pairs crosses one, from approximately 0.995 to 1.000, and group medians move by at most 0.05. Individual changes can nevertheless be substantial: healthy9/iso90 rises from 0.208 to 0.333, about 60%. Small changes in a group summary do not establish individual robustness or clinical equivalence.

The right panel shows filtered RMS divided by centered RMS. Four recordings fall below the retrospective review threshold of 0.8. This identifies records for inspection, not a diagnosis of movement artefacts. Squaring the ratio gives a mean-square comparison; neither quantity directly measures energy outside the selected frequency band.

### 4. A correction can help in one scenario and distort another

![Errors in controlled synthetic scenarios](../reports/figures/synthetic_scenario_matrix.png)

The matrix compares 11 scenarios and 21 methods, totaling 23,100 evaluations. Darker cells indicate smaller error against the constructed reference. In the isolated-spike scenario, whole-record RMS reverses the starting direction in all 100 repetitions. Limiting large values avoids that reversal.

However, when a sustained increase is deliberately defined as desired signal, limiting values also removes part of that signal. Selecting blocks helps with unequal pauses but does not recover the reference exactly. Unknown unequal sensor scaling persists across every method evaluated. The useful result is a map of trade-offs, rather than a claim that one processing choice always wins.

## What the work contributes

The project combines a verified data loader, an offline analysis pipeline, an individual signal viewer and reproducible scenario tests. It gives a reviewer the original amplitudes, the resulting ratios and the consequences of explicit processing choices. It also explains why an unusual number deserves investigation before interpretation.

Sensitivity to processing is already established in the literature, including [Benoit et al. (2003)](https://doi.org/10.1016/S0966-6362(02)00194-7) and [Devaprakash et al. (2016)](https://doi.org/10.1016/j.jelekin.2016.10.001). My contribution is this dataset-specific, inspectable implementation and its controlled failure cases, rather than discovering the general principle.

## Limits and next use

The files contain no force, movement-sensor or return-to-sport outcomes, and contraction boundaries and some acquisition details remain unresolved. The sampling rate is estimated from the clocks, and the device's own preprocessing is undocumented. The analysis is retrospective: centering, filtering, the quality flags and the `healthy8` exclusion were all decided after looking at the data, so each is shown next to the unmodified results. Synthetic perturbations are illustrative scenarios, not estimates of their frequency in real patients. Small samples limit statistical inference, and inspected external datasets did not support direct validation. Consequently, this work supports a methods and reproducibility portfolio case; it cannot determine readiness to return to sport. The complete [methods](review_methods.md), [results](review_results.md) and [limitations](review_limitations.md) provide the technical audit trail for review.
