# How DissentKit routes a request

```mermaid
flowchart LR
    A[User request] --> B{Review or decision?}
    B -->|No| C[Answer normally]
    B -->|Yes| D{Cheap to test or reverse?}
    D -->|Yes| E[Recommend the test or use Direct Review]
    D -->|No| F[Direct Review first]
    F --> G{Material downside, lock-in, or competing values?}
    G -->|No| H[Verdict and corrected version]
    G -->|Yes| I[Offer Deliberation]
    I --> J{Isolated passes available and requested?}
    J -->|Yes| K[Isolated-pass deliberation]
    J -->|No| L[Single-context deliberation]
    K --> M[Five chess-derived lenses and pre-mortems]
    L --> M
    M --> N[Challenge weak premises]
    N --> O[Record confidence movement]
    O --> P[Unresolved issue and recommendation]
    P --> Q[Falsifier, review point, first action]
```

The routing keeps routine criticism short. It also prevents a simulated panel from being described as independent evidence.

The five lenses use chess as a mnemonic: Rook for Direct, Bishop for Strategy, Knight for Blind spot, Queen for Synthesis, and King for Stakes. Evidence runs through every lens.

## What the pathway protects

- Direct Review avoids spending a large context budget on a small edit.
- Deliberation begins with failure cases so each lens has something concrete to challenge.
- The execution label tells the reader whether separate model passes actually ran.
- The falsifier and review point make the recommendation testable after the decision.
