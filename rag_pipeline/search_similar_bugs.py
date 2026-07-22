import chromadb
from sentence_transformers import SentenceTransformer

# Vector database location
db_path = r"E:\ai project\vector_db"

# Load the embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path=db_path)

# Get the bug collection
collection = client.get_collection(
    name="historical_bug_reports"
)

# Get a new bug report
query = input("\nEnter your bug report: ")

# Generate embedding for the new bug
query_embedding = model.encode(query).tolist()

# Search for the 5 most similar historical bugs
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

print("\n" + "=" * 60)
print("       SIMILAR HISTORICAL BUG ANALYSIS")
print("=" * 60)

for i in range(len(results["documents"][0])):

    distance = results["distances"][0][i]

    # Convert distance to an approximate similarity score
    similarity = max(0, (1 - distance / 2) * 100)

    metadata = results["metadatas"][0][i]
    document = results["documents"][0][i]

    print(f"\n{'=' * 60}")
    print(f"MATCH {i + 1}")
    print(f"{'=' * 60}")

    print(f"Similarity Score : {similarity:.2f}%")
    print(f"Product          : {metadata.get('product', 'Unknown')}")
    print(f"Component        : {metadata.get('component', 'Unknown')}")
    print(f"Severity         : {metadata.get('severity', 'Unknown')}")
    print(f"Status           : {metadata.get('status', 'Unknown')}")
    print(f"Resolution       : {metadata.get('resolution', 'Unknown')}")

    print("\nHistorical Bug:")
    print("-" * 60)
    print(document)

print("\n" + "=" * 60)
print("           SEARCH COMPLETED")
print("=" * 60)