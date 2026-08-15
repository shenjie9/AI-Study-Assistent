function Header({ title, description }) {
  return (
    <header className="app-header">
      <div className="header-badge">
        LOCAL RAG SYSTEM
      </div>

      <h1>{title}</h1>
      <p>{description}</p>
    </header>
  )
}

export default Header