# LLM-Guided ABC Flow Search

This directory implements an LLM-guided search over ABC optimization command
sequences. The experiment compares the resulting AIG depth and gate count with
the two objectives provided by the original FlowTune source:

- `t=0`: minimize AIG gate count `and`
- `t=1`: minimize AIG logic depth `lev`

The full experiment design, comparisons, and caveats are documented in the
[repository README](../README.md).

## Files

- `controller.py`: candidate generation, prompt construction, ABC evaluation,
  ranking, and equivalence verification
- `depth_prompt.txt`: system prompt for the LLM
- `allowed_commands.json`: command pool available to the LLM
- `aggregate.py`: combines per-design summaries into one table
- `reverify_budget.py`: rechecks `fir` checkpoint candidates with a longer
  runtime limit
- `flowtune_t1_reference.json`: formal `t=1` reference values from the
  author's `6_10` FlowTune reproduction

## Required GitHub secret

Add this repository secret:

- `DEEPSEEK_API_KEY`

Optional repository secret:

- `DEEPSEEK_BASE_URL`

The default model is `deepseek-v4-flash`. The API endpoint must expose an
OpenAI-compatible `chat/completions` interface.

## Search loop

1. Read the original BLIF design and convert it to AIG with `strash`.
2. Ask the LLM for up to 8 distinct command sequences.
3. Validate that every command is in `allowed_commands.json` and that each
   sequence contains at most 10 commands.
4. Execute every candidate with the official FlowTune ABC build.
5. Apply the same evaluation tail to every candidate:

   ```text
   strash
   ifraig
   dch -f
   strash
   print_stats
   ```

6. Rank successful candidates by lower `lev`, then lower `and`, then shorter
   runtime.
7. Put the top 10 command sequences and metrics into the next LLM prompt.
8. Continue until the selected candidate budget is reached.
9. Verify the best candidate with `dsec`.

The LLM is not trained or fine-tuned. Each request is a fresh
`system + user` message. The "experience" visible to the model is only the
top-10 history constructed by the controller. Independent repeats do not share
history with each other.

## Experiment settings

- Designs: `bfly`, `dscg`, `fir`, `ode`, `or1200`, `syn2`
- Candidate budgets: 16, 32, 64, 128 per design per repeat
- Independent repeats: 3
- Candidates requested per LLM call: 8
- Maximum commands per candidate: 10
- Temperature: 0.2
- Ranking: lower `lev`, then lower `and`, then shorter runtime

The four budget points produce:

```text
(16 + 32 + 64 + 128) × 6 designs × 3 repeats
= 4,320 candidate flows
```

## Main result at 64 candidates

Each cell is `lev / and`:

| Design | LLM | FlowTune t=0 | FlowTune t=1 |
|---|---:|---:|---:|
| bfly | 66 / 24105 | 90 / 19292 | 85 / 19799 |
| dscg | 63 / 23475 | 94 / 18858 | 87 / 19715 |
| fir | 65 / 22915 | 92 / 17939 | 83 / 18877 |
| ode | 68 / 13657 | 94 / 11020 | 90 / 11100 |
| or1200 | 124 / 10733 | 131 / 9974 | 131 / 10020 |
| syn2 | 63 / 24815 | 89 / 19936 | 84 / 20353 |

The LLM produces the lowest depth in all six designs, while FlowTune `t=0`
produces the lowest gate count.

## Budget curve

From 64 to 128 candidates, most designs improve by only about 0.33 depth level,
`syn2` stays unchanged, and `or1200` remains noisy. Token consumption increases
from about 2.01 million to 6.35 million, roughly 3.15 times. The current primary
budget is therefore 64 candidates; 128 candidates is kept as a sensitivity
check.

## Equivalence

The selected 64-candidate and 128-candidate best flows are equivalent to their
original designs. Two difficult `fir` candidates at 64 candidates required
702.92 and 444.40 seconds. The 128-candidate `fir` best flow initially returned
`UNDECIDED` under ABC's internal 60-second per-frame limit. The local
verification build had already changed that hardcoded PDR limit from 60 to 1200
seconds, and the candidate proved equivalent after 649.43 seconds. This changes
only the prover resource limit, not the equivalence criterion.

The cloud batch recheck used `dsec -T 600`, which sets an outer runtime limit but
does not override the internal PDR limit in the unmodified ABC build. Those
checkpoint candidates therefore remained `UNDECIDED`.

Some `fir` candidates at 16 and 32 candidates remain `UNDECIDED`. This means the
prover did not finish; it does not mean the networks are non-equivalent.

## Run the workflow

Open GitHub Actions and run:

- `LLM Flow Cloud Search` for the main search
- `Recheck Budget Curve Equivalence` for checkpoint rechecks

Each search job uploads its complete result directory as an artifact. The
aggregate report is committed under `llm-flow-results/latest/`.

Full run IDs and result interpretation are listed in the
[repository README](../README.md#六后续研究llm-引导的-abc-流程搜索).
