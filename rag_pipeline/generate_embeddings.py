import pandas as pd
from sentence_transformers import SentenceTransformer

input_path = r"E:\ai project\Datasets\chunked_bug_reports.csv"
output_path = r"E:\ai project\Datasets\bug_embeddings.csv"

# Load the chunked bug data
df = pd.read_csv(input_path)

# Load the embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
print("Generating embeddings...")
embeddings = model.encode(
    df["chunk_text"].fillna("").tolist(),
    show_progress_bar=True
)

# Convert embeddings to strings so they can be saved in CSV
df["embedding"] = [
    ",".join(map(str, embedding))
    for embedding in embeddings
]

# Save the embeddings
df.to_csv(output_path, index=False)

print("Embeddings generated successfully!")
print("Total embeddings:", len(embeddings))
print("Output:", output_path)