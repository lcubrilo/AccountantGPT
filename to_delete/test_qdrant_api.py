from qdrant_client import QdrantClient
client = QdrantClient(url="https://72bad419-5a52-45ec-b858-43e3828b861f.us-east4-0.gcp.cloud.qdrant.io:6333", api_key="qETHUQtyNbpasjuKuAFl-Yhjm25C7lIxag7MBnxoONVVgZy4ETmCUg")
print(client.get_collections())
