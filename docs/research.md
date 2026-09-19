# AutoPatch – Research Notes

This document lists key papers and resources relevant to the techniques
used (or planned) in AutoPatch.

## Spectrum-Based Fault Localisation (SBFL)

| Paper | Year | Notes |
|---|---|---|
| Abreu et al., "An Evaluation of Similarity Coefficients for Software Fault Localization" | 2006 | Introduces and benchmarks Ochiai coefficient |
| Jones & Harrold, "Empirical Evaluation of the Tarantula Automatic Fault-Localization Technique" | 2005 | Tarantula, an alternative SBFL formula |
| Wong et al., "A Survey on Software Fault Localization" | 2016 | Comprehensive SBFL survey |

## Automated Program Repair (APR)

| Paper / System | Year | Notes |
|---|---|---|
| Le Goues et al., GenProg | 2012 | Genetic programming for APR; the foundational APR work |
| Kim et al., PAR | 2013 | Template-based repair using human-written fix patterns |
| Liu et al., TBar | 2019 | Template-based APR, uses fix patterns from existing commits |
| Jiang et al., CURE | 2021 | NMT-based repair with code-aware embeddings |
| Xia et al., AlphaRepair | 2022 | Cloze-style repair using CodeBERT / UnixCoder |
| Wei et al., ChatRepair | 2023 | Conversational LLM repair (GPT-4) with test feedback |
| Cao et al., SoFix | 2023 | SWE-bench top performer using Agentless + LLMs |
| SWE-bench (Jimenez et al.) | 2023 | Standard APR benchmark using real GitHub issues |

## LLM Code Generation

| Resource | Notes |
|---|---|
| OpenAI Codex | Code generation backbone (deprecated in favour of GPT-4o) |
| DeepSeek-Coder | Open-weight alternative for code generation |
| CodeLlama | Meta's open-weight code LLM |
| Gemini 1.5 Pro | Strong at long-context code tasks |

## Benchmark Datasets

| Dataset | URL | Notes |
|---|---|---|
| SWE-bench | https://swe-bench.github.io | 2,294 real GitHub issues + test suites |
| Defects4J | https://defects4j.org | Classic Java APR benchmark |
| BugsInPy | https://github.com/soarsmu/BugsInPy | Python bugs with test suites |
| ManyBugs | https://repairbenchmarks.cs.umass.edu | C program bugs |

## Useful Tools

| Tool | Purpose |
|---|---|
| `pytest-cov` | Coverage collection for SBFL |
| `coverage.py` | Statement-level coverage data |
| `tree-sitter` | Fast AST parsing for code retrieval |
| `unidiff` | Python unified diff parsing |
| `gitpython` | Python Git automation |

