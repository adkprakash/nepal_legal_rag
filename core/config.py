from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str | None = None

    log_level: str | None = None
    api_host: str | None = None
    api_port: int | None = None
    uvicorn_workers: int | None = None

    # Required by every service: without these MongoClient silently falls back to localhost
    mongo_uri: str
    mongo_db_name: str

    qdrant_url: str | None = None
    qdrant_api_key: str | None = None
    qdrant_collection: str | None = None
    qdrant_dense_vector_name: str | None = None
    qdrant_sparse_vector_name: str | None = None
    qdrant_auto_create_collection: bool | None = None

    redis_url: str | None = None
    celery_broker_url: str | None = None
    celery_result_backend: str | None = None
    celery_worker_concurrency: int | None = None
    celery_task_soft_time_limit: int | None = None
    celery_task_time_limit: int | None = None
    ingestion_lock_ttl_seconds: int | None = None

    embedding_model: str | None = None
    embedding_dim: int | None = None
    embedding_device: str | None = None
    embedding_use_fp16: bool | None = None
    embedding_batch_size: int | None = None
    hf_home: str | None = None

    cors_origins: str | None = None
    log_question_text: bool | None = None
    hybrid_top_k: int | None = None
    rerank_top_n: int | None = None
    rerank_min_score: float | None = None
    reranker_model: str | None = None
    reranker_device: str | None = None
    reranker_max_length: int | None = None

    # docker-compose passes OLLAMA_MODEL from infra.env to the user service as LLM_MODEL
    llm_model: str | None = None
    ollama_base_url: str | None = None
    llm_temperature: float | None = None
    llm_max_tokens: int | None = None
    llm_timeout_seconds: int | None = None

    admin_api_key: str | None = None
    max_upload_mb: int | None = None
    parser_backend: str | None = None
    chunk_max_tokens: int | None = None
    llama_cloud_api_key: str | None = None

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        if not self.cors_origins:
            return []
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
