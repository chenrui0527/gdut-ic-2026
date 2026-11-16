# LLM-Guided ABC Flow Search

| Design | Baseline lev | LLM best lev | FlowTune t=1 lev | LLM and | FlowTune and | Equivalent | Best commands |
|---|---:|---:|---:|---:|---:|---|---|
| bfly | 74 | 66 | 87 | 24265 | 19954 | True | `balance; rewrite -z; refactor -z; rewrite -z; balance; refactor -z; rewrite -z; balance` |
| dscg | 73 | 64 | 85 | 23563 | 19539 | True | `balance; refactor -z; rewrite -z; refactor -z; balance; rewrite -z; balance` |
| fir | 75 | 66 | 85 | 23040 | 18710 | False | `balance; refactor -z; rewrite -z; resub -K 8; balance; refactor -z; rewrite -z; balance` |
| ode | 80 | 70 | 90 | 13650 | 11320 | True | `balance; rewrite -z; refactor -z; balance; rewrite -z; refactor -z; balance; rewrite -z; refactor -z; balance` |
| or1200 | 138 | 128 | 131 | 10931 | 10064 | True | `balance; refactor; refactor; balance; refactor; balance` |
| syn2 | 70 | 64 | 84 | 25041 | 20376 | True | `balance; resub -K 8; rewrite -z; refactor -z; rewrite -z; balance` |
