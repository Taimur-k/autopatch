import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import NewRepair from './pages/NewRepair'
import RepairRun from './pages/RepairRun'

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-950">
        {/* Global navigation bar */}
        <nav className="border-b border-gray-800 bg-gray-900 px-6 py-3 flex items-center gap-3">
          <span className="text-lg font-bold text-white tracking-tight">
            🩹 AutoPatch
          </span>
          <span className="text-xs text-gray-500 font-mono bg-gray-800 px-2 py-0.5 rounded">
            v0.1.0
          </span>
          <span className="ml-2 text-xs text-gray-500">
            AI-powered automated program repair
          </span>
        </nav>

        {/* Page content */}
        <main className="mx-auto max-w-7xl px-6 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/new" element={<NewRepair />} />
            <Route path="/runs/:runId" element={<RepairRun />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

