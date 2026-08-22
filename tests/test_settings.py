"""Behaviour tests for the pydantic-settings based configuration package."""

from __future__ import annotations

from pathlib import Path

import pytest

from config import (
    AppSettings,
    CacheSettings,
    CoreSettings,
    DatabaseSettings,
    JwkConfig,
    KafkaSettings,
    KeycloakConfig,
    ObservabilitySettings,
    RateLimitConfig,
    SessionConfig,
    StorageSettings,
    TopicMapping,
    get_settings,
    load_settings,
)


def test_app_settings_defaults() -> None:
    settings = AppSettings()

    assert settings.core.service_name == "omnixys"
    assert settings.core.environment == "local"
    assert settings.core.log_level == "INFO"
    assert settings.core.host == "0.0.0.0"
    assert settings.core.port == 8000
    assert settings.core.debug is False
    assert settings.core.internal_api_key == ""

    assert settings.hot_reload is False
    assert settings.database.url == "postgresql+asyncpg://omnixys:omnixys@localhost:5432/omnixys"
    assert settings.database.url_sync == "postgresql://omnixys:omnixys@localhost:5432/omnixys"
    assert settings.database.pool_size == 10
    assert settings.database.max_overflow == 20
    assert settings.database.echo is False

    assert settings.keycloak.url == "http://localhost:8080"
    assert settings.keycloak.realm == "omnixysu"
    assert settings.security.jwk == JwkConfig()
    assert settings.security.session == SessionConfig()
    assert settings.security.rate_limit == RateLimitConfig()
    assert settings.security.cors_allowed_methods == [
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "PATCH",
        "OPTIONS",
    ]

    assert settings.kafka.bootstrap_servers == "localhost:9092"
    assert settings.kafka.topics == TopicMapping()
    assert settings.kafka.topics.outbox == "omnixys.outbox.event"

    assert settings.cache.url == "redis://localhost:6379/0"
    assert settings.observability.service_name == "omnixys"
    assert settings.storage.bucket == "omnixys"
    assert settings.storage.force_path_style is True


def test_subsection_defaults() -> None:
    assert CoreSettings().is_local is True
    assert DatabaseSettings().pool_size == 10
    assert KeycloakConfig().issuer == "http://localhost:8080/realms/omnixysu"
    assert KeycloakConfig().jwks_url == (
        "http://localhost:8080/realms/omnixysu/protocol/openid-connect/certs"
    )
    assert JwkConfig().keys == []
    assert SessionConfig().ttl_ms == 3600000
    assert RateLimitConfig().default_limit == 120
    assert KafkaSettings().dlq_suffix == ".dlq"
    assert KafkaSettings().dlq_max_retries == 3
    assert CacheSettings().invalidation_channel == "omnixys:cache:invalidate"
    assert ObservabilitySettings().sampling_probability == 0.1
    assert ObservabilitySettings().otlp_endpoint == "http://localhost:4318"
    assert StorageSettings().link_ttl == 3600


def test_core_env_binding(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SERVICE_NAME", "orders")
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("HOST", "127.0.0.1")
    monkeypatch.setenv("PORT", "9000")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("INTERNAL_API_KEY", "super-secret")

    core = AppSettings().core

    assert core.service_name == "orders"
    assert core.environment == "production"
    assert core.log_level == "DEBUG"
    assert core.host == "127.0.0.1"
    assert core.port == 9000
    assert core.debug is True
    assert core.internal_api_key == "super-secret"


@pytest.mark.parametrize(
    ("environment", "local", "development", "production"),
    [
        ("local", True, True, False),
        ("development", False, True, False),
        ("production", False, False, True),
        ("staging", False, False, False),
    ],
)
def test_core_environment_helpers(
    monkeypatch: pytest.MonkeyPatch,
    environment: str,
    local: bool,
    development: bool,
    production: bool,
) -> None:
    monkeypatch.setenv("ENVIRONMENT", environment)

    core = AppSettings().core

    assert core.is_local is local
    assert core.is_development is development
    assert core.is_production is production


def test_database_env_binding(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://user:pass@db:5432/orders")
    monkeypatch.setenv("DATABASE_URL_SYNC", "postgresql://user:pass@db:5432/orders")
    monkeypatch.setenv("DATABASE_POOL_SIZE", "5")
    monkeypatch.setenv("DATABASE_MAX_OVERFLOW", "7")
    monkeypatch.setenv("DATABASE_ECHO", "true")

    database = AppSettings().database

    assert database.url == "postgresql+asyncpg://user:pass@db:5432/orders"
    assert database.url_sync == "postgresql://user:pass@db:5432/orders"
    assert database.pool_size == 5
    assert database.max_overflow == 7
    assert database.echo is True


def test_keycloak_env_binding_and_derived_urls(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("KEYCLOAK_URL", "http://kc:8080")
    monkeypatch.setenv("KEYCLOAK_REALM", "main")
    monkeypatch.setenv("KEYCLOAK_AUDIENCE", "orders-api")
    monkeypatch.setenv("KEYCLOAK_CLIENT_ID", "orders-backend")

    keycloak = AppSettings().keycloak

    assert keycloak.url == "http://kc:8080"
    assert keycloak.realm == "main"
    assert keycloak.audience == "orders-api"
    assert keycloak.client_id == "orders-backend"
    assert keycloak.issuer == "http://kc:8080/realms/main"
    assert keycloak.jwks_url == "http://kc:8080/realms/main/protocol/openid-connect/certs"


def test_security_env_binding(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SECURITY_STATELESS", "false")
    monkeypatch.setenv("SECURITY_PERMIT_ALL_PATHS", '["/health", "/metrics"]')
    monkeypatch.setenv("SECURITY_PERMIT_ALL_POST_PATHS", '["/webhooks"]')
    monkeypatch.setenv("SECURITY_COOKIE_SECURE", "true")
    monkeypatch.setenv("SECURITY_COOKIE_SAME_SITE", "strict")
    monkeypatch.setenv("SECURITY_CORS_ALLOWED_ORIGINS", '["https://app.example.com"]')

    security = AppSettings().security

    assert security.stateless is False
    assert security.permit_all_paths == ["/health", "/metrics"]
    assert security.permit_all_post_paths == ["/webhooks"]
    assert security.cookie_secure is True
    assert security.cookie_same_site == "strict"
    assert security.cors_allowed_origins == ["https://app.example.com"]


def test_security_nested_sections_bind(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("JWK_KEYS", '["k1", "k2"]')
    monkeypatch.setenv("SESSION_TTL_MS", "7200000")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")
    monkeypatch.setenv("RATE_LIMIT_DEFAULT_LIMIT", "60")

    security = AppSettings().security

    assert security.jwk.keys == ["k1", "k2"]
    assert security.session.ttl_ms == 7200000
    assert security.rate_limit.enabled is False
    assert security.rate_limit.default_limit == 60


def test_kafka_env_binding(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("KAFKA_ENABLED", "false")
    monkeypatch.setenv("KAFKA_BOOTSTRAP_SERVERS", "broker:9092")
    monkeypatch.setenv("KAFKA_CLIENT_ID", "orders")
    monkeypatch.setenv("KAFKA_RETRIES", "5")
    monkeypatch.setenv("KAFKA_DLQ_SUFFIX", ".dead")

    kafka = AppSettings().kafka

    assert kafka.enabled is False
    assert kafka.bootstrap_servers == "broker:9092"
    assert kafka.client_id == "orders"
    assert kafka.retries == 5
    assert kafka.dlq_suffix == ".dead"
    assert kafka.topics.delivery_status == "omnixys.delivery.status"


def test_topic_mapping_env_binding(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TOPIC_DELIVERY_STATUS", "custom.status")
    monkeypatch.setenv("TOPIC_OUTBOX", "custom.outbox")

    topics = AppSettings().kafka.topics

    assert topics.delivery_status == "custom.status"
    assert topics.outbox == "custom.outbox"


def test_cache_env_binding(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CACHE_URL", "redis://cache:6379/1")
    monkeypatch.setenv("CACHE_KEY_PREFIX", "acme:")
    monkeypatch.setenv("CACHE_INVALIDATION_CHANNEL", "acme:cache:invalidate")
    monkeypatch.setenv("CACHE_WORKER_ENABLED", "true")

    cache = AppSettings().cache

    assert cache.url == "redis://cache:6379/1"
    assert cache.key_prefix == "acme:"
    assert cache.invalidation_channel == "acme:cache:invalidate"
    assert cache.worker_enabled is True


def test_observability_env_binding(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OTEL_ENABLED", "false")
    monkeypatch.setenv("OTEL_SERVICE_NAME", "orders")
    monkeypatch.setenv("OTEL_SAMPLING_PROBABILITY", "0.5")
    monkeypatch.setenv("OTEL_OTLP_ENDPOINT", "http://otel:4318")

    observability = AppSettings().observability

    assert observability.enabled is False
    assert observability.service_name == "orders"
    assert observability.sampling_probability == 0.5
    assert observability.otlp_endpoint == "http://otel:4318"


def test_storage_env_binding(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STORAGE_REGION", "eu-central-1")
    monkeypatch.setenv("STORAGE_ENDPOINT", "http://minio:9000")
    monkeypatch.setenv("STORAGE_ACCESS_KEY_ID", "access")
    monkeypatch.setenv("STORAGE_SECRET_ACCESS_KEY", "secret")
    monkeypatch.setenv("STORAGE_BUCKET", "files")
    monkeypatch.setenv("STORAGE_LINK_TTL", "600")
    monkeypatch.setenv("STORAGE_FORCE_PATH_STYLE", "false")
    monkeypatch.setenv("STORAGE_PUBLIC_URL", "https://cdn.example.com")

    storage = AppSettings().storage

    assert storage.region == "eu-central-1"
    assert storage.endpoint == "http://minio:9000"
    assert storage.access_key_id == "access"
    assert storage.secret_access_key == "secret"
    assert storage.bucket == "files"
    assert storage.link_ttl == 600
    assert storage.force_path_style is False
    assert storage.public_url == "https://cdn.example.com"


def test_app_settings_hot_reload_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOT_RELOAD", "true")

    assert AppSettings().hot_reload is True


def test_load_settings_reads_env_file(tmp_path: Path) -> None:
    env_file = tmp_path / "app.env"
    env_file.write_text(
        "DATABASE_URL=postgresql+asyncpg://filehost/db\n"
        "SERVICE_NAME=fileapp\n"
        "CACHE_URL=redis://filecache:6379/9\n"
        "TOPIC_OUTBOX=custom.outbox\n"
        "HOT_RELOAD=true\n",
    )

    settings = load_settings(env_file=env_file)

    assert settings.database.url == "postgresql+asyncpg://filehost/db"
    assert settings.core.service_name == "fileapp"
    assert settings.cache.url == "redis://filecache:6379/9"
    assert settings.kafka.topics.outbox == "custom.outbox"
    assert settings.hot_reload is True


def test_load_settings_defaults_without_env_file() -> None:
    settings = load_settings()

    assert isinstance(settings, AppSettings)
    assert settings.core.service_name == "omnixys"
    assert settings.database.pool_size == 10


def test_load_settings_ignores_missing_env_file() -> None:
    settings = load_settings(env_file="/nonexistent/app.env")

    assert settings.core.service_name == "omnixys"
    assert settings.database.url == "postgresql+asyncpg://omnixys:omnixys@localhost:5432/omnixys"


def test_env_var_precedes_env_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    env_file = tmp_path / "app.env"
    env_file.write_text("DATABASE_URL=postgresql+asyncpg://filehost/db\n")
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://envhost/db")

    settings = load_settings(env_file=env_file)

    assert settings.database.url == "postgresql+asyncpg://envhost/db"


def test_get_settings_delegates_to_load_settings() -> None:
    assert get_settings() == load_settings()
