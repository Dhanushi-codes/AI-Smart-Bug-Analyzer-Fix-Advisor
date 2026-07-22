import pandas as pd
import chromadb

# Paths
input_path = r"E:\ai project\Datasets\bug_embeddings.csv"
db_path = r"E:\ai project\vector_db"

# Load embeddings file
print("Loading embeddings...")
df = pd.read_csv(input_path)

# Create a persistent ChromaDB client
client = chromadb.PersistentClient(path=db_path)

# Create or get our collection
collection = client.get_or_create_collection(
    name="historical_bug_reports"
)

print("Adding embeddings to ChromaDB...")

# Add data to ChromaDB
collection.add(
    ids=[f"{bug_id}_chunk_{i}" for i, bug_id in enumerate(df["bug_id"].astype(str))],
    embeddings=[
        [float(value) for value in embedding.split(",")]
        for embedding in df["embedding"]
    ],
    documents=df["chunk_text"].fillna("").tolist(),
    metadatas=[
        {
            "source": str(row["source"]),
            "product": str(row["product"]),
            "component": str(row["component"]),
            "severity": str(row["severity"]),
            "status": str(row["status"]),
            "resolution": str(row["resolution"])
        }
        for _, row in df.iterrows()
    ]
)

print("Vector database created successfully!")
print("Total vectors stored:", collection.count())
print("Database location:", db_path)