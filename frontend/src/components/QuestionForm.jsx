import { useState } from 'react'
import { API_BASE_URL } from '../config.js'

function QuestionForm({ documentReady }) {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')
  const [provider, setProvider] = useState('ollama')

  function handleQuestionChange(event) {
    setQuestion(event.target.value)
  }

  function handleProviderChange(event) {
    setProvider(event.target.value)
  }

  async function handleSubmit(event) {
    event.preventDefault()

    if (!documentReady || !question.trim()) {
      return
    }

    setIsLoading(true)
    setAnswer('')
    setErrorMessage('')

    const formData = new FormData()
    formData.append('question', question.trim())
    formData.append('provider_name', provider)

    try {
      const response = await fetch(`${API_BASE_URL}/ask`, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Question request failed.')
      }

      setAnswer(data.answer)
    } catch (error) {
      setErrorMessage(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <section className="card question-card">
      <div className="section-heading">
        <span className="step-number">02</span>

        <div>
          <h2>Ask a Question</h2>
          <p>Generate answers grounded in your uploaded document.</p>
        </div>
      </div>

      <div className="provider-section">
        <label htmlFor="provider">Model Provider</label>

        <select
          id="provider"
          value={provider}
          onChange={handleProviderChange}
          disabled={isLoading}
        >
          <option value="ollama">Ollama · Llama 3.2 (Local)</option>
          <option value="openai" disabled>
            OpenAI · API credentials required
          </option>
        </select>

        <p className="provider-note">
          OpenAI integration is supported but requires API credentials to be configured.
        </p>
      </div>

      <form className="question-form" onSubmit={handleSubmit}>
        <input
          type="text"
          aria-label="Question"
          placeholder={
            documentReady
              ? 'Ask something about your document...'
              : 'Upload a PDF before asking questions.'
          }
          value={question}
          onChange={handleQuestionChange}
          disabled={!documentReady}
        />

        <button
          className="primary-button ask-button"
          type="submit"
          disabled={!documentReady || !question.trim() || isLoading}
        >
          {isLoading ? (
            <span className="loading-label">
              <span className="loading-dot"></span>
              Generating
            </span>
          ) : (
            'Ask'
          )}
        </button>
      </form>

      {answer && (
        <div className="answer-panel" aria-live="polite">
          <div className="answer-heading">
            <span className="response-dot"></span>
            <span>AI RESPONSE</span>
          </div>

          <p>{answer}</p>
        </div>
      )}

      {errorMessage && (
        <p className="error-message" role="alert">
          {errorMessage}
        </p>
      )}
    </section>
  )
}

export default QuestionForm
