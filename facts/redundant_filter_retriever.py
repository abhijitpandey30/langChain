from typing import List
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import Chroma
from langchain.schema import BaseRetriever, Document


class RedundantFilterRetriever(BaseRetriever):
    embeddings: Embeddings
    chroma: Chroma

    def get_relevant_documents(self, query: str) -> List[Document]:
        # Embed the query
        emb = self.embeddings.embed_query(query)

        # Perform Max Marginal Relevance search
        return self.chroma.max_marginal_relevance_search_by_vector(
            embedding=emb,
            lambda_mult=0.8
        )

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        # Async version (not really async here, just stubbed for API compatibility)
        return self.get_relevant_documents(query)
