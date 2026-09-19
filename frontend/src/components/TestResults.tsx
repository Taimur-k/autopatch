interface TestCase {
  name: string
  outcome: 'PASSED' | 'FAILED' | 'ERROR' | 'SKIPPED'
  duration_ms?: number
  message?: string
}

interface TestResultsSummary {
  passed: number
  failed: number
  errors: number
  skipped: number
  test_cases: TestCase[]
}

interface Props {
  results: TestResultsSummary
}

// Mock data shown when no real results are available yet.
export const MOCK_RESULTS: TestResultsSummary = {
  passed: 24,
  failed: 2,
  errors: 0,
  skipped: 1,
  test_cases: [
    { name: 'test_parse_simple',   outcome: 'PASSED', duration_ms: 12.3 },
    { name: 'test_parse_empty',    outcome: 'PASSED', duration_ms: 5.1 },
    { name: 'test_parse_nested',   outcome: 'PASSED', duration_ms: 18.7 },
    { name: 'test_parse_boundary', outcome: 'FAILED', duration_ms: 8.2,  message: 'IndexError: list index out of range' },
    { name: 'test_service_none',   outcome: 'FAILED', duration_ms: 3.4,  message: "AttributeError: 'NoneType' has no attribute 'data'" },
    { name: 'test_validate_empty', outcome: 'PASSED', duration_ms: 2.1 },
    { name: 'test_health',         outcome: 'PASSED', duration_ms: 45.0 },
  ],
}

export default function TestResults({ results }: Props) {
  return (
    <div className="space-y-4">
      {/* Summary row */}
      <div className="flex gap-6">
        <span className="text-green-400 font-mono text-sm">
          ✓ {results.passed} passed
        </span>
        {results.failed > 0 && (
          <span className="text-red-400 font-mono text-sm">
            ✗ {results.failed} failed
          </span>
        )}
        {results.errors > 0 && (
          <span className="text-orange-400 font-mono text-sm">
            ⚠ {results.errors} errors
          </span>
        )}
        {results.skipped > 0 && (
          <span className="text-gray-500 font-mono text-sm">
            ◌ {results.skipped} skipped
          </span>
        )}
      </div>

      {/* Per-test list */}
      <div className="space-y-1">
        {results.test_cases.map((tc, i) => (
          <div key={i} className="flex items-start gap-3">
            <span className={`text-xs mt-0.5 shrink-0 ${
              tc.outcome === 'PASSED'  ? 'text-green-500' :
              tc.outcome === 'FAILED'  ? 'text-red-500'   :
              tc.outcome === 'ERROR'   ? 'text-orange-500':
              'text-gray-600'
            }`}>
              {tc.outcome === 'PASSED' ? '✓' : tc.outcome === 'SKIPPED' ? '◌' : '✗'}
            </span>
            <div className="min-w-0">
              <span className="font-mono text-xs text-gray-300">{tc.name}</span>
              {tc.duration_ms !== undefined && (
                <span className="ml-2 text-xs text-gray-600">{tc.duration_ms.toFixed(1)}ms</span>
              )}
              {tc.message && (
                <p className="text-xs text-red-400 mt-0.5 font-mono">{tc.message}</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

