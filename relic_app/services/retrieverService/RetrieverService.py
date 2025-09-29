import logging
from langchain_openai import OpenAIEmbeddings
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from typing import List
from relic_app.db import db_manager

logger = logging.getLogger(__name__)


class RelicRetriever(BaseRetriever):
    def __init__(self, top_k=5):
        self.embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
        self.top_k = top_k
        
    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        try:
            with db_manager.get_connection() as conn:
                with conn.cursor() as cur:
                    query_embedding = self.embedding_model.embed_query(query)

                    cur.execute(
                        f"""
                        SELECT relicId FROM relic_vectors
                        ORDER BY embedding <=> %s
                        LIMIT {self.top_k};
                        """,
                        (str(query_embedding),)
                    )
                    relic_ids = [row[0] for row in cur.fetchall()]

                    if not relic_ids:
                        return []

                    cur.execute(
                        'SELECT relicId, "desc", materialName, purposeName, nationalityName FROM relic_data WHERE relicId IN %s;',
                        (tuple(relic_ids),)
                    )
                    records = cur.fetchall()

                    documents = []
                    for rec in records:
                        page_content = f"Description: {rec[1]}\nMaterial: {rec[2]}\nPurpose: {rec[3]}\nNationality: {rec[4]}"
                        metadata = {
                            "relicId": rec[0],
                            "materialName": rec[2],
                            "purposeName": rec[3],
                            "nationalityName": rec[4],
                        }
                        documents.append(Document(page_content=page_content, metadata=metadata))
                    
                    return documents

        except Exception as e:
            logger.error(f"An unexpected error occurred during retrieval: {e}")
            return []