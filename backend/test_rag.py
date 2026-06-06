from rag import (
    extract_text_from_pdf,
    chunk_text,
    create_vector_store,
    retrieve_relevant_chunks,
    generate_answer
)

pdf_path = "backend/csc311_study_notes.pdf"

text = extract_text_from_pdf(pdf_path)

print("Text extracted.")

chunks = chunk_text(text)

print(f"Created {len(chunks)} chunks.")

index, chunks = create_vector_store(chunks)

question = input("Ask a question: ")

results = retrieve_relevant_chunks(question, index, chunks)

print("\nTop Retrieved Chunks:\n")

for i, chunk in enumerate(results):
    print(f"\n----- Chunk {i + 1} -----\n")
    print(chunk[:500])

answer = generate_answer(question, results)

print("\nAI Answer:\n")
print(answer)