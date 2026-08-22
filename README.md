# omnixys-config

Unified, type-safe configuration for Omnixys services, built on
`pydantic-settings`. Every service setting lives in one settings tree with
section-scoped environment variables, matching the conventions used across the
Omnixys codebase.

## Installation

```bash
pip install omnixys-config
```

## Features

- **One settings tree** — `AppSettings` groups core, database, keycloak,
  security, kafka, cache, observability, and storage configuration into nested
  typed models.
- **Environment binding** — every section reads its own `env_prefix`
  (`database_`, `keycloak_`, `security_`, `kafka_`, `cache_`, `otel_`,
  `storage_`, ...); flat core settings read unprefixed variables
  (`SERVICE_NAME`, `PORT`, ...).
- **Nested environment support** — environment values are applied to nested
  settings models at every depth (e.g. `security.jwk.keys` from `JWK_KEYS`,
  `kafka.topics.outbox` from `TOPIC_OUTBOX`), something vanilla
  `pydantic-settings` does not do for nested models.
- **List values** — list fields parse JSON from the environment
  (`SECURITY_PERMIT_ALL_PATHS='["/health", "/metrics"]'`,
  `JWK_KEYS='["k1", "k2"]'`).
- **Env files** — a `.env` file is loaded automatically; a custom file can be
  passed to `load_settings(env_file=...)`. Precedence is
  **env var > env file > default**.
- **Computed helpers** — `core.is_local / is_development / is_production`,
  `keycloak.issuer / jwks_url`.
- **Factories** — `get_settings()` / `load_settings()` return a single cached
  `AppSettings` per call site.

## Quick start

```python
from config import get_settings

settings = get_settings()

settings.core.service_name          # "orders"
settings.database.url               # "postgresql+asyncpg://localhost/omnixys"
settings.security.jwk.keys          # [..]
settings.kafka.topics.outbox        # "omnixys.outbox.event"
```

Wire the settings object once per service, e.g. with dishka:

```python
from dishka import make_async_container
from config import AppSettings, get_settings

def settings_provider() -> AppSettings:
    return get_settings()

container = make_async_container(settings_provider)
settings = await container.get(AppSettings)
```

## Settings reference

### Core

| Field | Env variable | Default |
| --- | --- | --- |
| `service_name` | `SERVICE_NAME` | `"omnixys"` |
| `environment` | `ENVIRONMENT` | `"local"` |
| `log_level` | `LOG_LEVEL` | `"INFO"` |
| `host` | `HOST` | `"0.0.0.0"` |
| `port` | `PORT` | `8000` |
| `debug` | `DEBUG` | `false` |
| `internal_api_key` | `INTERNAL_API_KEY` | `""` |

Core helpers: `is_local` (`environment == "local"`),
`is_development` (`local`/`development`), `is_production` (`production`).

### Database (`database_`)

| Field | Env variable | Default |
| --- | --- | --- |
| `url` | `DATABASE_URL` | `"postgresql+asyncpg://omnixys:omnixys@localhost:5432/omnixys"` |
| `url_sync` | `DATABASE_URL_SYNC` | `"postgresql://omnixys:omnixys@localhost:5432/omnixys"` |
| `pool_size` | `DATABASE_POOL_SIZE` | `10` |
| `max_overflow` | `DATABASE_MAX_OVERFLOW` | `20` |
| `echo` | `DATABASE_ECHO` | `false` |

### Keycloak (`keycloak_`)

| Field | Env variable | Default |
| --- | --- | --- |
| `url` | `KEYCLOAK_URL` | `"http://localhost:8080"` |
| `realm` | `KEYCLOAK_REALM` | `"omnixysu"` |
| `audience` | `KEYCLOAK_AUDIENCE` | `"account"` |
| `client_id` | `KEYCLOAK_CLIENT_ID` | `"omnixys-backend"` |
| `client_secret` | `KEYCLOAK_CLIENT_SECRET` | `""` |

Helpers: `issuer` (`{url}/realms/{realm}`), `jwks_url`
(`{issuer}/protocol/openid-connect/certs`).

### Security (`security_`)

| Field | Env variable | Default |
| --- | --- | --- |
| `permit_all_post_paths` | `SECURITY_PERMIT_ALL_POST_PATHS` | `[]` (JSON) |
| `permit_all_get_paths` | `SECURITY_PERMIT_ALL_GET_PATHS` | `[]` (JSON) |
| `permit_all_paths` | `SECURITY_PERMIT_ALL_PATHS` | `[]` (JSON) |
| `stateless` | `SECURITY_STATELESS` | `true` |
| `form_login_disabled` | `SECURITY_FORM_LOGIN_DISABLED` | `true` |
| `csrf_disabled` | `SECURITY_CSRF_DISABLED` | `true` |
| `cookie_secure` | `SECURITY_COOKIE_SECURE` | `false` |
| `cookie_same_site` | `SECURITY_COOKIE_SAME_SITE` | `"lax"` |
| `cookie_domain` | `SECURITY_COOKIE_DOMAIN` | `""` |
| `cookie_path` | `SECURITY_COOKIE_PATH` | `"/"` |
| `access_token_name` | `SECURITY_ACCESS_TOKEN_NAME` | `"access_token"` |
| `refresh_token_name` | `SECURITY_REFRESH_TOKEN_NAME` | `"refresh_token"` |
| `access_token_max_age_ms` | `SECURITY_ACCESS_TOKEN_MAX_AGE_MS` | `900000` |
| `refresh_token_max_age_ms` | `SECURITY_REFRESH_TOKEN_MAX_AGE_MS` | `2592000000` |
| `cors_allowed_origins` | `SECURITY_CORS_ALLOWED_ORIGINS` | `[]` (JSON) |
| `cors_allowed_methods` | `SECURITY_CORS_ALLOWED_METHODS` | `["GET","POST","PUT","DELETE","PATCH","OPTIONS"]` (JSON) |
| `cors_allowed_headers` | `SECURITY_CORS_ALLOWED_HEADERS` | `[]` (JSON) |
| `cors_allow_credentials` | `SECURITY_CORS_ALLOW_CREDENTIALS` | `true` |
| `cors_max_age_seconds` | `SECURITY_CORS_MAX_AGE_SECONDS` | `3600` |

Nested sections use their own prefixes: `JWK_KEYS` (`jwk_`),
`SESSION_TTL_MS` (`session_`), `RATE_LIMIT_ENABLED` /
`RATE_LIMIT_DEFAULT_LIMIT` / `RATE_LIMIT_DEFAULT_WINDOW_MS` (`rate_limit_`).

### Kafka (`kafka_`)

| Field | Env variable | Default |
| --- | --- | --- |
| `enabled` | `KAFKA_ENABLED` | `true` |
| `bootstrap_servers` | `KAFKA_BOOTSTRAP_SERVERS` | `"localhost:9092"` |
| `client_id` | `KAFKA_CLIENT_ID` | `"omnixys"` |
| `group_id` | `KAFKA_GROUP_ID` | `"omnixys-group"` |
| `retries` | `KAFKA_RETRIES` | `3` |
| `acks` | `KAFKA_ACKS` | `"all"` |
| `concurrency` | `KAFKA_CONCURRENCY` | `1` |
| `auto_commit` | `KAFKA_AUTO_COMMIT` | `true` |
| `dlq_enabled` | `KAFKA_DLQ_ENABLED` | `true` |
| `dlq_suffix` | `KAFKA_DLQ_SUFFIX` | `".dlq"` |
| `dlq_max_retries` | `KAFKA_DLQ_MAX_RETRIES` | `3` |

Topic names use the `topic_` prefix (`TOPIC_DELIVERY_STATUS`,
`TOPIC_CONVERSATION_CREATED`, `TOPIC_CONVERSATION_MESSAGE`,
`TOPIC_EVENT_CREATED`, `TOPIC_EVENT_UPDATED`, `TOPIC_NOTIFICATION_SEND`,
`TOPIC_SEAT_CHANGED`, `TOPIC_TICKET_ISSUED`, `TOPIC_AUDIT_LOG`,
`TOPIC_OUTBOX`).

### Cache (`cache_`)

| Field | Env variable | Default |
| --- | --- | --- |
| `url` | `CACHE_URL` | `"redis://localhost:6379/0"` |
| `password` | `CACHE_PASSWORD` | `""` |
| `key_prefix` | `CACHE_KEY_PREFIX` | `"omnixys:"` |
| `invalidation_enabled` | `CACHE_INVALIDATION_ENABLED` | `true` |
| `invalidation_channel` | `CACHE_INVALIDATION_CHANNEL` | `"omnixys:cache:invalidate"` |
| `worker_enabled` | `CACHE_WORKER_ENABLED` | `false` |
| `worker_poll_interval_ms` | `CACHE_WORKER_POLL_INTERVAL_MS` | `5000` |

### Observability (`otel_`)

| Field | Env variable | Default |
| --- | --- | --- |
| `enabled` | `OTEL_ENABLED` | `true` |
| `service_name` | `OTEL_SERVICE_NAME` | `"omnixys"` |
| `tracing_enabled` | `OTEL_TRACING_ENABLED` | `true` |
| `sampling_probability` | `OTEL_SAMPLING_PROBABILITY` | `0.1` |
| `propagation` | `OTEL_PROPAGATION` | `"tracecontext"` |
| `metrics_enabled` | `OTEL_METRICS_ENABLED` | `true` |
| `prometheus_enabled` | `OTEL_PROMETHEUS_ENABLED` | `true` |
| `otlp_endpoint` | `OTEL_OTLP_ENDPOINT` | `"http://localhost:4318"` |
| `otlp_transport` | `OTEL_OTLP_TRANSPORT` | `"http"` |
| `tempo_health_url` | `OTEL_TEMPO_HEALTH_URL` | `""` |
| `prometheus_health_url` | `OTEL_PROMETHEUS_HEALTH_URL` | `""` |

### Storage (`storage_`)

| Field | Env variable | Default |
| --- | --- | --- |
| `region` | `STORAGE_REGION` | `"us-east-1"` |
| `endpoint` | `STORAGE_ENDPOINT` | `"http://localhost:9000"` |
| `access_key_id` | `STORAGE_ACCESS_KEY_ID` | `"minioadmin"` |
| `secret_access_key` | `STORAGE_SECRET_ACCESS_KEY` | `"minioadmin"` |
| `bucket` | `STORAGE_BUCKET` | `"omnixys"` |
| `link_ttl` | `STORAGE_LINK_TTL` | `3600` |
| `force_path_style` | `STORAGE_FORCE_PATH_STYLE` | `true` |
| `public_url` | `STORAGE_PUBLIC_URL` | `""` |

## Precedence

Values are resolved as **environment variable > env file > default**. Env files
are loaded with `override=False`, so an already-set variable always wins:

```python
from config import load_settings

# reads /path/to/app.env for values not already present in the environment
settings = load_settings(env_file="/path/to/app.env")
```

Without an argument, a `.env` file in the working directory is loaded if it
exists. All section-prefixed variables (`database_`, `keycloak_`, ...) are read
from the env file as well.

## Development

```bash
uv sync
uv run pytest -q
uv run ruff check .
uv run mypy src/
```

## License

GPL-3.0-or-later
