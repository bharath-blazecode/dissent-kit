# Deliberation protocol

Use this mode only for decisions with material downside, lock-in, competing values, or a costly reversal.

## Execution label

Start with one of these labels:

- `Isolated-pass deliberation`: Each lens receives the same neutral brief in a separate model or subagent pass before seeing the others.
- `Single-context deliberation`: One model runs every lens in the same context.

The second format can improve coverage, but it is not independent corroboration. Do not describe agreement between its lenses as independent consensus.

## Frame the decision

Write one neutral sentence that names the decision, options, objective, constraints, and important unknowns. Remove language that favors one option unless the preference itself is relevant evidence.

If the user is leaning toward one answer, assign one lens to steelman the rejected option.

## Run five chess-derived lenses

Each lens begins with a short pre-mortem. Assume the decision failed and explain the most plausible route to that failure.

1. **Rook, Direct**: State the clearest failure case without softening it.
2. **Bishop, Strategy**: Trace timing, dependencies, lock-in, and second-order effects.
3. **Knight, Blind spot**: Look for an angle outside the user's current framing.
4. **Queen, Synthesis**: Test how the arguments interact, where they contradict, and what changes when they are considered together.
5. **King, Stakes**: Name the outcome that must be protected and reject interesting points that do not affect it.

Evidence runs through every lens. Each one labels substantive claims as fact, inference, assumption, or unknown and flags unsupported numbers or causal claims.

In isolated-pass mode, do not show one lens another lens's work until every pre-mortem is complete. In single-context mode, draft each pre-mortem before starting synthesis and do not rewrite earlier views to create artificial agreement.

## Challenge the positions

After the pre-mortems, each lens states a position and confidence level. Relabel the positions A through E before the challenge round when the host supports isolated passes.

Challenge the weakest premise in each position. A lens may update only when the challenge exposes a specific error or missing fact. Record the reason for every confidence change. Do not reward movement for its own sake.

If nearly every lens agrees, test the strongest counterfactual before accepting consensus: assume the shared conclusion is wrong and state the best explanation for that failure.

## Deliver the result

Use this compact structure:

1. Execution label and limitation
2. Decision frame
3. Pre-mortems
4. Main challenges
5. Confidence before and after
6. What remains unresolved
7. Recommendation
8. Falsifier: the evidence that would overturn the recommendation
9. Review point: a date or observable event for checking the outcome
10. First action

Do not present a vote count as probability. Several passes can share the same blind spot, especially when they use one model or one source set.
