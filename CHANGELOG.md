# 🧾 Changelog

All notable changes in this project will be documented in this file.


## [3.0.2](https://github.com/omnixys/config-python/compare/v3.0.1...v3.0.2) (2026-09-02)

### Ci

* **Ci:** add setup-uv to release job for uv lock in prepare cmd ([](https://github.com/omnixys/config-python/commit/33d8ee781c909c2caeddfe5aad9565604be1245c))
* **Ci:** bundle semantic-release tool install to fix conventional-changelog-writer ([](https://github.com/omnixys/config-python/commit/e791aea65d1c993cd5c8275ee1b8403fd19ef9bc))
* **Ci:** pin conventional-changelog-conventionalcommits to v9 for release-notes-generator compat ([](https://github.com/omnixys/config-python/commit/ff47504d81c0fdde5f87bb624244165a7cbbc26b))
* **Ci:** publish tagged release to PyPI ([](https://github.com/omnixys/config-python/commit/86cc1aa628822c6e7763dc4a1e254d99a38c9f0a))
* **Ci:** remove stray comma from releaseBodyTemplate ([](https://github.com/omnixys/config-python/commit/9a48a07645d7f2d5e869c2fcb4426f0d155822fa))

### Deps

* **Deps:** update omnixys deps ([](https://github.com/omnixys/config-python/commit/23e87b8f5ec3b60339af81dd21112c5ea223fbc7))

### Other

* **Other:** ga ([](https://github.com/omnixys/config-python/commit/d11cd950a1e9b623e87c5e87b4f65694ae5448ad))
* **Other:** Merge pull request #1 from omnixys/migration/uuid-v7 ([](https://github.com/omnixys/config-python/commit/dd1c26642d749dee3e172aef3cce0e714f5f9d1f)), closes [#1](https://github.com/omnixys/config-python/issues/1)

### Packaging

* **Packaging:** fix ruff lint and version metadata tests ([](https://github.com/omnixys/config-python/commit/30e8efecfcc15aa64494db30c2f6ab05e8d2dd90))
* **Packaging:** move package version to pyproject.toml and align release workflow ([](https://github.com/omnixys/config-python/commit/02e57091eff9cd74b09af5e0ddfb5a1baf801169))

## [3.0.1](https://github.com/omnixys/config-python/compare/v3.0.0...v3.0.1) (2026-08-22)


### Bug Fixes

* **dir:** remove target dir ([8832be9](https://github.com/omnixys/config-python/commit/8832be9387eeda7a45d15ff5a7502988054f286a))

# [3.0.0](https://github.com/omnixys/config-python/compare/v2.0.4...v3.0.0) (2026-07-23)


### Bug Fixes

* **config:** add CacheSettings.password field and update default keycloak realm ([b0b4638](https://github.com/omnixys/config-python/commit/b0b4638bd2bc0b17c2fd29290781b0d0495a2670))
* **config:** propagate .env values to nested BaseSettings subclasses ([710d430](https://github.com/omnixys/config-python/commit/710d430e3a0f940b12b3b2130af0e29235161894))
* **config:** propagate .env values to os.environ for nested BaseSettings ([181d905](https://github.com/omnixys/config-python/commit/181d9050d9dd01df8320503e4d6ff2363ea39bc2))


### Features

* **config:** accept optional env_file in load_settings ([4589095](https://github.com/omnixys/config-python/commit/458909534b8f6a2c349d71dae80a13ea25759f8a))
* **config:** add tempo_health_url and prometheus_health_url to ObservabilitySettings ([985014e](https://github.com/omnixys/config-python/commit/985014eed66a20eae104681f04a5be20c3f18dfd))

## [2.0.4](https://github.com/omnixys/config-python/compare/v2.0.3...v2.0.4) (2026-07-22)


### Bug Fixes

* **publish:** add uv build before uv publish ([d431275](https://github.com/omnixys/config-python/commit/d4312758e8f20a2a6fca4494dc035650b5ffd6d0))

## [2.0.3](https://github.com/omnixys/config-python/compare/v2.0.2...v2.0.3) (2026-07-22)


### Bug Fixes

* **publish:** replace gh release upload with uv publish to PyPI ([d014c76](https://github.com/omnixys/config-python/commit/d014c7640fe65a4dc43958488a042cffde285f7d))

## [2.0.2](https://github.com/omnixys/config-python/compare/v2.0.1...v2.0.2) (2026-07-22)


### Bug Fixes

* **release:** add @semantic-release/exec to update __version__ in __init__.py ([22ac2c4](https://github.com/omnixys/config-python/commit/22ac2c4bc6e3876a6e53232e7b087e4a8ee84352))

## [2.0.1](https://github.com/omnixys/config-python/compare/v2.0.0...v2.0.1) (2026-07-22)


### Bug Fixes

* **cicd:** use version comparison for release detection ([01ddf72](https://github.com/omnixys/config-python/commit/01ddf727b648e886e16f75a92fe7d5626ebf9a58))

# [2.0.0](https://github.com/omnixys/config-python/compare/v1.1.1...v2.0.0) (2026-07-22)

# Changelog

All notable changes in this project will be documented in this file.


## [1.1.1](https://github.com/omnixys/config-python/compare/v1.1.0...v1.1.1) (2026-07-22)

## [1.0.2](https://github.com/omnixys/config-python/compare/v1.0.1...v1.0.2) (2026-07-22)

## [1.0.1](https://github.com/omnixys/config-python/compare/v1.0.0...v1.0.1) (2026-07-15)

## 1.0.0 (2026-07-15)
