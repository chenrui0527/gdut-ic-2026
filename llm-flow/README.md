# LLM-Guided ABC Flow Search

This workflow asks a DeepSeek-compatible LLM to propose ABC optimization flows
and evaluates the candidates with the author's FlowTune ABC build.

## Required GitHub secret

Add this repository secret:

- `DEEPSEEK_API_KEY`

Optional repository secret:

- `DEEPSEEK_BASE_URL`

The model defaults to `deepseek-v4-flash`. The API must expose an
OpenAI-compatible `chat/completions` endpoint.

## Experiment defaults

- Designs: `bfly`, `dscg`, `fir`, `ode`, `or1200`, `syn2`
- Candidates per design per repeat: 64
- Repeats: 3
- LLM candidates requested per API call: 8
- Maximum commands per candidate: 10
- Temperature: 0.2
- Ranking: lower `lev`, then lower `and`, then lower runtime
- Equivalence: the best result of every repeat is checked with `dsec`

## Run

Open GitHub Actions, choose `LLM Flow Cloud Search`, and run the workflow.
Six design jobs run in parallel. Results are uploaded as artifacts and committed
under `llm-flow-results/latest/`.
