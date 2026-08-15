import { useState } from 'react'
import { API_BASE_URL } from '../config.js'

function UploadPanel({ onDocumentReady }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState(null)

  function handleFileChange(event) {
    const file = event.target.files[0] || null
    setSelectedFile(file)
    setUploadStatus(null)
    onDocumentReady(false)
  }

  async function handleUpload() {
    if (!selectedFile) {
      return
    }

    setIsUploading(true)
    setUploadStatus(null)

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Upload failed.')
      }

      setUploadStatus({
        type: 'success',
        message: `${data.filename} indexed successfully (${data.chunks_created} chunks).`,
      })
      onDocumentReady(true)
    } catch (error) {
      setUploadStatus({ type: 'error', message: error.message })
      onDocumentReady(false)
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <section className="card upload-card">
      <div className="section-heading">
        <span className="step-number">01</span>

        <div>
          <h2>Upload Study Material</h2>
          <p>Select a PDF to create a searchable knowledge base.</p>
        </div>
      </div>

      <div className="file-upload-area">
        <input
          id="pdf-upload"
          type="file"
          accept=".pdf,application/pdf"
          onChange={handleFileChange}
        />

        <label htmlFor="pdf-upload" className="file-upload-label">
          Choose PDF
        </label>

        <span className="file-name">
          {selectedFile ? selectedFile.name : 'No file selected'}
        </span>
      </div>

      <button
        className="primary-button"
        onClick={handleUpload}
        disabled={!selectedFile || isUploading}
      >
        {isUploading ? 'Indexing document...' : 'Upload & Index'}
      </button>

      {uploadStatus && (
        <div className={`status-message ${uploadStatus.type}`} role="status">
          <span className="status-dot"></span>
          <span>{uploadStatus.message}</span>
        </div>
      )}
    </section>
  )
}

export default UploadPanel
