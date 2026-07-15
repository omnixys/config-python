from __future__ import annotations

# ruff: noqa: D100, D101, D102, S104, S105
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="database_")
    url: str = "postgresql+asyncpg://omnixys:omnixys@localhost:5432/omnixys"
    url_sync: str = "postgresql://omnixys:omnixys@localhost:5432/omnixys"
    pool_size: int = 10
    max_overflow: int = 20
    echo: bool = False


class KeycloakConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="keycloak_")
    url: str = "http://localhost:8080"
    realm: str = "omnixys"
    audience: str = "account"
    client_id: str = "omnixys-backend"
    client_secret: str = ""

    @property
    def issuer(self) -> str:
        return f"{self.url}/realms/{self.realm}"

    @property
    def jwks_url(self) -> str:
        return f"{self.issuer}/protocol/openid-connect/certs"


class JwkConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="jwk_")
    keys: list[str] = Field(default_factory=list)


class SessionConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="session_")
    ttl_ms: int = 3600000


class RateLimitConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="rate_limit_")
    enabled: bool = True
    default_limit: int = 120
    default_window_ms: int = 60000


class SecuritySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="security_")
    permit_all_post_paths: list[str] = Field(default_factory=list)
    permit_all_get_paths: list[str] = Field(default_factory=list)
    permit_all_paths: list[str] = Field(default_factory=list)
    stateless: bool = True
    form_login_disabled: bool = True
    csrf_disabled: bool = True
    jwk: JwkConfig = JwkConfig()
    session: SessionConfig = SessionConfig()
    rate_limit: RateLimitConfig = RateLimitConfig()
    cookie_secure: bool = False
    cookie_same_site: str = "lax"
    cookie_domain: str = ""
    cookie_path: str = "/"
    access_token_name: str = "access_token"
    refresh_token_name: str = "refresh_token"
    access_token_max_age_ms: int = 900000
    refresh_token_max_age_ms: int = 2592000000
    cors_allowed_origins: list[str] = Field(default_factory=list)
    cors_allowed_methods: list[str] = Field(
        default_factory=lambda: ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    )
    cors_allowed_headers: list[str] = Field(default_factory=list)
    cors_allow_credentials: bool = True
    cors_max_age_seconds: int = 3600


class TopicMapping(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="topic_")
    delivery_status: str = "omnixys.delivery.status"
    conversation_created: str = "omnixys.conversation.created"
    conversation_message: str = "omnixys.conversation.message"
    event_created: str = "omnixys.event.created"
    event_updated: str = "omnixys.event.updated"
    notification_send: str = "omnixys.notification.send"
    seat_changed: str = "omnixys.seat.changed"
    ticket_issued: str = "omnixys.ticket.issued"
    audit_log: str = "omnixys.audit.log"
    outbox: str = "omnixys.outbox.event"


class KafkaSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="kafka_")
    enabled: bool = True
    bootstrap_servers: str = "localhost:9092"
    client_id: str = "omnixys"
    group_id: str = "omnixys-group"
    retries: int = 3
    acks: str = "all"
    concurrency: int = 1
    auto_commit: bool = True
    dlq_enabled: bool = True
    dlq_suffix: str = ".dlq"
    dlq_max_retries: int = 3
    topics: TopicMapping = TopicMapping()


class CacheSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="cache_")
    url: str = "redis://localhost:6379/0"
    key_prefix: str = "omnixys:"
    invalidation_enabled: bool = True
    invalidation_channel: str = "omnixys:cache:invalidate"
    worker_enabled: bool = False
    worker_poll_interval_ms: int = 5000


class ObservabilitySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="otel_")
    enabled: bool = True
    service_name: str = "omnixys"
    tracing_enabled: bool = True
    sampling_probability: float = 0.1
    propagation: str = "tracecontext"
    metrics_enabled: bool = True
    prometheus_enabled: bool = True
    otlp_endpoint: str = "http://localhost:4318"
    otlp_transport: str = "http"


class StorageSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="storage_")
    region: str = "us-east-1"
    endpoint: str = "http://localhost:9000"
    access_key_id: str = "minioadmin"
    secret_access_key: str = "minioadmin"
    bucket: str = "omnixys"
    link_ttl: int = 3600
    force_path_style: bool = True
    public_url: str = ""


class CoreSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    service_name: str = "omnixys"
    environment: str = "local"
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    internal_api_key: str = ""

    @property
    def is_local(self) -> bool:
        return self.environment == "local"

    @property
    def is_development(self) -> bool:
        return self.environment in ("local", "development")

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    core: CoreSettings = CoreSettings()
    database: DatabaseSettings = DatabaseSettings()
    keycloak: KeycloakConfig = KeycloakConfig()
    security: SecuritySettings = SecuritySettings()
    kafka: KafkaSettings = KafkaSettings()
    cache: CacheSettings = CacheSettings()
    observability: ObservabilitySettings = ObservabilitySettings()
    storage: StorageSettings = StorageSettings()
