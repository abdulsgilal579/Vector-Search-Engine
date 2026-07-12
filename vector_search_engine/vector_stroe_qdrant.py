from qdrant_client import QdrantClient
from uuid import uuid4
from qdrant_client.models import Distance, VectorParams, PointStruct


class QdrantStore:
    def __init__(self, collection_name, url="http://localhost:6333", vector_size=384, distance=Distance.COSINE):
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.distance = distance
        self.ensureCollection()

    def ensureCollection(self):
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=self.distance),
            )

    def addDocument(self, texts, vectors, metadatas):
        points = []
        for text, vector, metadata in zip(texts, vectors, metadatas):
            point = PointStruct(
                id=uuid4().hex,
                vector=vector,
                payload={"text": text, **metadata},
            )
            points.append(point)
        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def search(self, query_vector, k=5):
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=k,
            with_payload=True,
        )
        clean = []
        for point in results.points:
            clean.append({
                "text": point.payload["text"],
                "score": point.score,
                "source": point.payload.get("source"),
                "page": point.payload.get("page"),
            })
        return clean
