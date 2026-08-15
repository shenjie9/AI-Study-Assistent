import { useState } from 'react'
import Header from './components/Header.jsx'
import UploadPanel from './components/UploadPanel.jsx'
import QuestionForm from './components/QuestionForm.jsx'
import './App.css'

function App() {
  const [documentReady, setDocumentReady] = useState(false)

  return (
    <main className="app">
      <div className="app-container">
        <Header
          title="AI Study Assistant"
          description="Upload your study material and ask questions about it."
        />

        <div className="workspace">
          <UploadPanel onDocumentReady={setDocumentReady} />
          <QuestionForm documentReady={documentReady} />
        </div>
      </div>
    </main>
  )
}

export default App
