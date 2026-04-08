# Sankofa — African Regulatory Intelligence (`/sankofa`)

> *"Go back. Fetch it. Prove it."*

Parse a folder of African regulatory documents (CBN circulars, CBK guidelines, BOG frameworks, SARB rules, etc.) and generate a structured compliance analysis report — with every claim cited back to the exact word on the exact page.

## Arguments

`$ARGUMENTS` should contain:
- **First argument (`$0`)**: Path to directory containing regulatory documents (PDFs, DOCX, PPTX)
- **Remaining arguments**: Your compliance question or product description

**Example invocations:**
```
/sankofa ./regs "What licences and capital requirements does a mobile money operator need in Ghana?"
/sankofa ./regs "Our app processes payments across Ghana, Nigeria and Kenya — what do we need?"
/sankofa ./regs "What AML rules apply to a crypto exchange in Ghana and South Africa?"
/sankofa ./regs "Compare agent banking requirements across East Africa"
/sankofa ./regs "What data localisation obligations exist for fintechs in Rwanda?"
```

If either argument is missing, ask the user to provide it.

## Step 1 — Parse Documents

Run the bundled script to extract text and bounding boxes from all supported files:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/generate_report.py" \
    --skill-dir "${CLAUDE_SKILL_DIR}" \
    --dir "$0" \
    --parse-only \
    --output /tmp/sankofa_parsed.json
```

Supported formats (no API key required — all local):
- **PDF** → PyMuPDF (word-level bounding boxes)
- **DOCX, PPTX, XLSX, images** → Docling (chunk-level bounding boxes)
- **Plaintext** → .txt, .md, .rst (read directly)

Output is a JSON file with text and bounding box coordinates per page.

If there are more than 50 files, ask the user which country or topic to focus on, then re-run with a narrower subdirectory.

## Step 2 — Read Parsed Content

Read `/tmp/sankofa_parsed.json` with the Read tool. For each file note:
- `name` — filename (often encodes the country/authority, e.g. `CBN_PSP_Guidelines_2023.pdf`)
- For PDF/DOCX/PPTX files: each page's `text` field
- For plaintext: the top-level `text` field
- `summary` — total counts

Before answering, build a mental map of:
1. Which **jurisdictions** are covered (infer from filename or doc content — see table below)
2. Which **regulatory bodies** issued each document (see table below)
3. What **type** of regulation each document is (licensing framework, capital requirements, AML rules, consumer protection, data rules, etc.)

### African regulatory body reference

| Country | Code | Primary Regulator | Common doc types |
|---------|------|-------------------|-----------------|
| Ghana | GH | BOG (Bank of Ghana) | Payment Systems Act, e-Money Guidelines, PSP Tiers |
| Nigeria | NG | CBN (Central Bank of Nigeria) | PSP Framework, AML/CFT Regs, IMTO Guidelines |
| Kenya | KE | CBK (Central Bank of Kenya) | Mobile Money Guidelines, NPS Regulations |
| South Africa | ZA | SARB / FSCA / PA | NPS Act, CASP Guidance, Exchange Control Regs |
| Rwanda | RW | BNR (National Bank of Rwanda) | Payment Services Regulation, E-Money Rules |
| Uganda | UG | BOU (Bank of Uganda) | Mobile Money Regulations, PSP Guidelines |
| Tanzania | TZ | BoT (Bank of Tanzania) | Payment Systems Regs, E-Money Licensing |
| Ethiopia | ET | NBE (National Bank of Ethiopia) | Digital Payments Directive, Forex Rules |
| Senegal / WAEMU | SN | BCEAO | e-Money Regulation, PSP Licensing |
| Egypt | EG | CBE (Central Bank of Egypt) | Fintech Licensing, Digital Payments Regs |
| Zambia | ZM | BOZ (Bank of Zambia) | NPS Regulations, E-Money Guidelines |
| Côte d'Ivoire | CI | BCEAO | (shared WAEMU framework with Senegal) |

**Where to find real regulatory documents:**
- Nigeria CBN: cbn.gov.ng → Regulations & Guidelines
- Kenya CBK: centralbank.go.ke → Bank Supervision → Licensing
- Ghana BOG: bog.gov.gh → Payment Systems → Regulations
- South Africa SARB: resbank.co.za → Prudential Authority
- Rwanda BNR: bnr.rw → Regulations → Payment Systems
- Uganda BOU: bou.or.ug → Financial Stability → Payment Systems
- African fintech regulation tracker: fintechregulation.africa

## Step 3 — Generate Compliance Analysis

Using the parsed text as context, answer the user's compliance question. Structure your answer as:

### Answer format

```
## Requirements Found
[Bullet list of concrete regulatory requirements discovered, each with [N] citation markers]

## Compliance Gaps
[What the user's product/question implies they may be missing or need to address. If no product description was given, note what common gaps apply.]

## Jurisdictional Summary
[One paragraph per jurisdiction covered, summarising the key rules relevant to the question]

## Action Items
[Numbered, concrete steps the developer/compliance officer should take next]
```

Write your answer to a JSON file:

```bash
cat > /tmp/sankofa_answer.json << 'ANSWER_EOF'
{
  "question": "<the user's question>",
  "answer": "<full markdown answer with [N] citation markers>",
  "jurisdictions_covered": ["NG", "KE"],
  "citations": [
    {
      "file": "<filename e.g. CBN_PSP_Guidelines_2023.pdf>",
      "page": <1-indexed page number>,
      "quote": "<exact verbatim substring from parsed text>",
      "relevance": "<what this rule means in context and why it matters for the question>",
      "jurisdiction": "<ISO 3166-1 alpha-2 code: NG, KE, GH, ZA, EG, TZ, RW, UG, SN, ET>",
      "regulatory_body": "<e.g. CBN, CBK, BOG, SARB, RBA, BNR, UCC>"
    }
  ]
}
ANSWER_EOF
```

**Critical rules for citation quotes:**
- `quote` MUST be **copied character-for-character** from the parsed text — used for bounding box lookup. No paraphrasing, no typo fixes.
- Prefer **short, precise quotes** under 60 characters: numbers, percentages, defined terms. Short quotes match bounding boxes more reliably.
- `page` is 1-indexed. For plaintext files set `page` to `0`.
- `file` is filename only, not full path.

**Critical rules for the answer:**
- Embed `[N]` citation markers inline, at the end of the sentence or claim they support.
- `[N]` corresponds to the **1-indexed** position in the `citations` array.
- Include **5–15 citations** covering key requirements, thresholds, and definitions.
- When the same requirement appears in multiple jurisdictions, cite each separately.

**Critical rules for relevance:**
- Don't just restate the label. Explain *so what*: "This sets the minimum paid-up capital for a PSP licence in Nigeria at ₦2 billion — your product must meet this before applying."

## Step 4 — Generate HTML Report

```bash
python "${CLAUDE_SKILL_DIR}/scripts/generate_report.py" \
    --skill-dir "${CLAUDE_SKILL_DIR}" \
    --dir "$0" \
    --answer-file /tmp/sankofa_answer.json \
    --output sankofa_output/
```

This will:
1. Parse and screenshot only the cited pages
2. Find bounding boxes for each cited quote
3. Generate a self-contained HTML report with visual highlights
4. Open the report in the default browser

## Step 5 — Present Results

Tell the user:
1. The file path of the generated report
2. Which jurisdictions were covered
3. How many citations were found
4. A 2–3 sentence summary of the key finding or most critical action item
