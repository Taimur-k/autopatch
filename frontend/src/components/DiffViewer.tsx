interface Props {
  diff: string
}

function classifyLine(line: string): string {
  if (line.startsWith('+++') || line.startsWith('---')) return 'text-gray-500'
  if (line.startsWith('@@')) return 'text-blue-400 bg-blue-950/40'
  if (line.startsWith('+')) return 'text-green-400 bg-green-950/40'
  if (line.startsWith('-')) return 'text-red-400 bg-red-950/30'
  return 'text-gray-400'
}

export default function DiffViewer({ diff }: Props) {
  if (!diff) {
    return <p className="text-sm text-gray-500 p-4">No diff available.</p>
  }

  const lines = diff.split('\n')

  return (
    <div className="overflow-x-auto">
      <pre className="text-xs font-mono leading-5 p-4 bg-gray-950 min-w-0">
        {lines.map((line, i) => (
          <div key={i} className={`px-2 rounded-sm ${classifyLine(line)}`}>
            {line || ' '}
          </div>
        ))}
      </pre>
    </div>
  )
}

