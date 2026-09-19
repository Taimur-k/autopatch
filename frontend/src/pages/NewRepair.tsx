import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import IssueInput from '../components/IssueInput'
import { createIssue, createRepairRun } from '../services/api'

export default function NewRepair() {
  const navigate = useNavigate()

  const [repositoryUrl, setRepositoryUrl] = useState('')
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    if (!repositoryUrl.trim() || !title.trim() || !description.trim()) {
      setError('All fields are required.')
      return
    }

    setLoading(true)
    try {
      const issue = await createIssue({
        title: title.trim(),
        description: description.trim(),
        repository_url: repositoryUrl.trim(),
      })
      const run = await createRepairRun(issue.id)
      navigate(`/runs/${run.id}`)
    } catch (err: unknown) {
      setError('Failed to start repair. Is the backend running?')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">New Repair</h1>
        <p className="text-sm text-gray-500 mt-1">
          Describe the bug and AutoPatch will attempt to generate a fix automatically.
        </p>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="bg-gray-900 border border-gray-800 rounded-xl p-6 space-y-6">
        <IssueInput
          repositoryUrl={repositoryUrl}
          setRepositoryUrl={setRepositoryUrl}
          title={title}
          setTitle={setTitle}
          description={description}
          setDescription={setDescription}
        />

        {error && (
          <div className="rounded-lg bg-red-950 border border-red-800 px-4 py-3 text-sm text-red-300">
            {error}
          </div>
        )}

        <div className="flex justify-end gap-3">
          <button
            type="button"
            onClick={() => navigate('/')}
            className="px-4 py-2 text-sm text-gray-400 hover:text-gray-200 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className="px-5 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:text-gray-500 text-white text-sm font-semibold rounded-lg transition-colors"
          >
            {loading ? 'Starting…' : 'Start Repair →'}
          </button>
        </div>
      </form>
    </div>
  )
}

