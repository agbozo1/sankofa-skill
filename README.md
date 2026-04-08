# Sankofa 🦅

> *"Go back. Fetch it. Prove it."*

A Claude Code skill that parses African regulatory documents and generates deep compliance reports — with every claim cited back to the exact word on the exact source page.

## The problem

African fintechs expanding across borders must navigate 54+ different regulatory regimes. Central bank circulars, licensing frameworks, and AML guidelines live in dense PDFs. Missing one rule can mean a revoked licence. Compliance work demands an audit trail.

## What it does

1. **Parses** your folder of regulatory PDFs (CBN, CBK, BOG, SARB, RBA, BNR…) in seconds using [LiteParse](https://github.com/run-llama/liteparse)
2. **Analyses** your compliance question with Claude — finding requirements, gaps, and action items
3. **Generates** a self-contained HTML report with word-level citations and bounding boxes highlighted directly on each source page image

## Install

```bash
npx skills add your-username/sankofa --skill research_regs
```

Or clone and add the skill path manually.

## Usage

```
/sankofa ./regs "What licences does a mobile money operator need in Nigeria?"
/sankofa ./regs "Our app lets users send money across borders in Nigeria and Kenya — what do we need?"
/sankofa ./cbk-docs "What are the capital adequacy requirements for Kenyan banks?"
```

**Arguments:**
- First: path to a directory of regulatory documents (PDF, DOCX, PPTX, XLSX, images, .txt)
- Rest: your compliance question or product description

## Output

A timestamped HTML report (`sankofa_output/sankofa-report-YYYY-MM-DD-HHmmss.html`) containing:
- **Requirements Found** — what the regulations actually say, with citations
- **Compliance Gaps** — what your product may be missing
- **Jurisdictional Summary** — per-country breakdown
- **Action Items** — numbered next steps
- **Visual citations** — each claim linked back to the highlighted word on the source PDF page

## Supported jurisdictions

Nigeria (CBN) · Kenya (CBK) · Ghana (BOG) · South Africa (SARB) · Rwanda (BNR) · Uganda (BOU) · Tanzania (BoT) · Egypt (CBE) · Senegal (BCEAO) · + any African regulatory doc

## Sample data

Drop some central bank PDFs into `data/sample_regs/` and try:

```
/sankofa ./data/sample_regs "What is required to operate a payment service in this jurisdiction?"
```

## Requirements

```
pip install docling pymupdf
```

No API key required. Both libraries run fully locally.

- **PyMuPDF** — PDF parsing with word-level bounding boxes and page screenshots
- **Docling** (IBM, open source) — DOCX, PPTX, images, and other formats

## Inspired by

[liteparse_samples](https://github.com/jerryjliu/liteparse_samples) by Jerry Liu — built the original research-docs skill this is adapted from.

---

*Sankofa is an Akan word from Ghana meaning "go back and fetch it" — the wisdom to look back at the source before moving forward.*
