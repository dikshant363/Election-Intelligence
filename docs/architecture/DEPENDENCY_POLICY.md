# DEPENDENCY_POLICY.md

## Dependency Management

### Python
- Use `uv` for dependency management
- Pin all dependencies to exact versions
- Run `uv pip install -r requirements.txt` to install

### Node.js
- Use `pnpm` as the package manager
- Lockfile must be committed (`pnpm-lock.yaml`)
- Run `pnpm install` to install dependencies

### Flutter
- Use `pubspec.yaml` for dependencies
- Run `flutter pub get` to install
- Run `flutter pub outdated --mode=analysis` to check for updates

## Version Policy

| Dependency Type | Update Policy |
|-----------------|---------------|
| Production deps | Only for security patches |
| Dev dependencies | Periodic review, quarterly |
| Tooling | Latest stable versions |

## Dependency Review

Run `./scripts/verify` to check for:
- Security vulnerabilities
- Outdated dependencies
- Duplicate packages
- License compliance