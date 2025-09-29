import logging
from langchain_openai import OpenAIEmbeddings
from relic_app.db import db_manager
from relic_app.dto.EmuseumDTO import DataForVector

logger = logging.getLogger(__name__)
from dotenv import load_dotenv
load_dotenv()


class EmbeddingService:
    def __init__(self):
        self.embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
        
    def save_data_for_vector(self, data: DataForVector):
        """Saves relic data to be embedded later."""
        try:
            with db_manager.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO relic_data (relicId, "desc", materialName, purposeName, nationalityName)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (relicId) DO NOTHING;
                        """,
                        (data.relicId, data.desc, data.materialName, data.purposeName, data.nationalityName)
                    )
                    conn.commit()
                    logger.info(f"Successfully saved data for relicId: {data.relicId}")
        except Exception as e:
            logger.error(f"Database error while saving vector data: {e}")
            
    def embed_and_save(self):
        """Embeds new data and saves it to the vector store."""
        try:
            with db_manager.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT relicId, "desc", materialName, purposeName, nationalityName FROM relic_data WHERE embedded = FALSE;')
                    records = cur.fetchall()

                    if not records:
                        logger.info("No new data to embed.")
                        return

                    texts_to_embed = [f"Description: {r[1]} Material: {r[2]} Purpose: {r[3]} Nationality: {r[4]}" for r in records]
                    relic_ids = [r[0] for r in records]

                    embeddings = self.embedding_model.embed_documents(texts_to_embed)

                    for relicId, embedding in zip(relic_ids, embeddings):
                        cur.execute(
                            "INSERT INTO relic_vectors (relicId, embedding) VALUES (%s, %s) ON CONFLICT (relicId) DO UPDATE SET embedding = EXCLUDED.embedding;",
                            (relicId, embedding)
                        )
                        cur.execute("UPDATE relic_data SET embedded = TRUE WHERE relicId = %s;", (relicId,))

                    conn.commit()
                    logger.info(f"Successfully embedded {len(records)} records.")
        except Exception as e:
            logger.error(f"An unexpected error occurred during embedding: {e}")
            
embedding_service = EmbeddingService()
