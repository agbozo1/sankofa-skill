# `/sankofa` — African Regulatory Compliance Skill

Parse regulatory documents from African central banks and financial regulators, then generate a structured compliance analysis report with word-level citations.

## Quick start

```
/sankofa ./path/to/regs "Your compliance question here"
```

## How it works

| Step | What happens |
|------|-------------|
| 1 | LiteParse extracts text + bounding boxes from every document |
| 2 | Claude reads the parsed content and maps jurisdictions |
| 3 | Claude generates a structured compliance analysis with inline `[N]` citation markers |
| 4 | The report generator screenshots only the cited pages and draws highlights |
| 5 | A self-contained HTML report opens in your browser |

## Answer structure

Every report is organised as:
- **Requirements Found** — specific rules with citation markers
- **Compliance Gaps** — what your product needs to address
- **Jurisdictional Summary** — per-country breakdown
- **Action Items** — concrete next steps

## Naming files

The skill infers jurisdiction from filenames. Use names like:
- `CBN_PSP_Framework_2023.pdf` → Nigeria
- `CBK_Mobile_Money_Guidelines.pdf` → Kenya
- `BOG_Payment_Systems_Act.pdf` → Ghana

## Dependencies

```
pip install docling pymupdf
```

No API key required — both run fully locally.
