# AutoPatch – Benchmark

This directory contains the benchmark configuration for evaluating AutoPatch
against real-world bug datasets.

## Directory Structure

```
benchmark/
├── repositories/   Cloned repositories (git-ignored; populated at runtime)
├── issues/         JSON issue descriptors
└── README.md       This file
```

## Issue Descriptor Format

Each file in `issues/` is a JSON object describing a single bug:

```json
{
  "id": "acme-billing-001",
  "repository": "https://github.com/acme-corp/billing-service",
  "commit": "abc1234",
  "title": "IndexError when parsing empty input",
  "description": "Calling parse_expression() with an empty token list raises IndexError.",
  "failing_tests": [
    "tests/test_parser.py::test_parse_boundary"
  ],
  "expected_patch_files": [
    "src/parser.py"
  ]
}
```

## Supported Benchmarks

| Benchmark | Language | Issues | Link |
|---|---|---|---|
| SWE-bench | Python | 2,294 | https://swe-bench.github.io |
| BugsInPy  | Python | 493   | https://github.com/soarsmu/BugsInPy |
| Defects4J | Java   | 835   | https://defects4j.org |

## Running Evaluation

```bash
# (Future) Evaluate AutoPatch on SWE-bench Lite
python -m autopatch.eval --benchmark swe-bench-lite --output results/
```

