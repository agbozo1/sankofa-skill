# Sankofa 🦅

> *"Go back. Fetch it. Prove it."*

A Claude Code skill — born in Ghana — that finds African regulatory documents online, parses every page, and generates deep compliance reports with every claim cited back to the exact word on the exact source page.

![Sankofa Report](assets/screenshot.png)

## The problem

African fintechs expanding across borders must navigate 54+ different regulatory regimes. Central bank circulars, licensing frameworks, and AML guidelines live in dense PDFs scattered across government websites. Missing one rule can mean a rejected application or a revoked licence. Compliance work demands an audit trail.

## What it does

1. **Finds** the right regulatory documents online for your target jurisdictions — no manual downloading
2. **Parses** every PDF locally with word-level precision — no API key, no cloud upload
3. **Analyses** your compliance question with Claude — requirements, gaps, and action items
4. **Generates** a self-contained HTML report with every claim highlighted back to the exact word on the exact source page

## Install

```bash
npx skills add agbozo1/sankofa-skill --skill sankofa
```

## Usage

### Auto-fetch mode
Just ask your question. Sankofa detects the jurisdictions, searches for the relevant regulatory PDFs, downloads them, and runs the analysis.

```
/sankofa "What licences does a mobile money operator need in Ghana?"
/sankofa "Our app processes payments across Ghana, Nigeria and Kenya — what do we need?"
/sankofa "What AML rules apply to a crypto exchange in Ghana and South Africa?"
/sankofa "Compare agent banking requirements across East Africa"
```

### Local mode
Point it at your own folder of documents — useful for custom circulars, draft regulations, or internal compliance policies.

```
/sankofa ./my-regs "What licences does a mobile money operator need in Ghana?"
```

### Hybrid mode
Combine your local documents with an online search. Sankofa merges both into a single corpus before analysing. Your local files take priority — online docs fill the gaps.

```
/sankofa ./my-regs --hybrid "What licences does a mobile money operator need in Ghana?"
```

## Output

A timestamped HTML report (`sankofa_output/sankofa-report-YYYY-MM-DD-HHmmss.html`) containing:
- **Requirements Found** — what the regulations actually say, with citations
- **Compliance Gaps** — what your product may be missing
- **Jurisdictional Summary** — per-country breakdown
- **Action Items** — numbered next steps
- **Visual citations** — each claim linked back to the highlighted word on the source PDF page

## Supported jurisdictions

Ghana (BOG) · Nigeria (CBN) · Kenya (CBK) · South Africa (SARB) · Rwanda (BNR) · Uganda (BOU) · Tanzania (BoT) · Zambia (BOZ) · Ethiopia (NBE) · Egypt (CBE) · Senegal (BCEAO) · + any African regulatory doc

## Requirements

```bash
pip install pymupdf python-docx python-pptx requests
```

No API key required. All libraries run fully locally.

| Library | Purpose |
|---------|---------|
| PyMuPDF | PDF parsing — word-level bounding boxes and page screenshots |
| python-docx | DOCX text extraction |
| python-pptx | PPTX slide text extraction |
| requests | PDF download from regulatory body websites |

## Inspired by

[liteparse_samples](https://github.com/jerryjliu/liteparse_samples) by Jerry Liu — built the original research-docs skill this is adapted from.

---

*Sankofa is an Akan word from Ghana meaning "go back and fetch it" — the wisdom to look back at the source before moving forward. The name, the symbol, and the purpose are all Ghanaian.*
