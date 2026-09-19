interface Props {
  repositoryUrl: string
  setRepositoryUrl: (v: string) => void
  title: string
  setTitle: (v: string) => void
  description: string
  setDescription: (v: string) => void
}

export default function IssueInput({
  repositoryUrl, setRepositoryUrl,
  title, setTitle,
  description, setDescription,
}: Props) {
  return (
    <div className="space-y-5">
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-1.5">
          Repository URL
        </label>
        <input
          type="url"
          value={repositoryUrl}
          onChange={e => setRepositoryUrl(e.target.value)}
          placeholder="https://github.com/owner/repo"
          className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2.5 text-sm text-gray-100 placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-1.5">
          Issue Title
        </label>
        <input
          type="text"
          value={title}
          onChange={e => setTitle(e.target.value)}
          placeholder="e.g. IndexError when parsing empty input"
          className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2.5 text-sm text-gray-100 placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-1.5">
          Issue Description
        </label>
        <textarea
          rows={6}
          value={description}
          onChange={e => setDescription(e.target.value)}
          placeholder="Describe the bug in detail. Include steps to reproduce, expected behaviour, and the actual behaviour observed."
          className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2.5 text-sm text-gray-100 placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-y"
        />
      </div>
    </div>
  )
}

