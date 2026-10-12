# Security baseline

This document defines minimum expectations for application and deployment changes in this repository.

## Secrets and repository content

- Do not commit passwords, API tokens, Flask `SECRET_KEY` values, private keys, certificates containing private material, `.env` files, customer data, or production logs.
- Keep production secrets outside the checkout and inject them at runtime through protected host configuration. Restrict access to the service account and administrators.
- Do not print secrets or place them in URLs, issue text, logs, screenshots, or build output.
- If a secret is pushed, revoke or rotate it first; removing the file or rewriting Git history does not revoke it.
- Review staged file names and diffs before every push. The ignore rules and GitHub secret scanning are defense in depth, not guarantees.

## Flask application

- Never expose Flask's development server or interactive debugger in production. Run the app with Gunicorn behind the production reverse proxy.
- Load `SECRET_KEY` from protected runtime configuration and fail closed if production secrets are missing.
- In HTTPS production, use secure, HttpOnly, SameSite session cookies. Add CSRF protection to cookie-authenticated state-changing routes.
- Keep Jinja auto-escaping enabled; do not mark untrusted content safe.
- Validate accepted hosts and configure forwarded-header trust only for the actual reverse-proxy hops.
- Validate inputs, authorize every protected operation, use parameterized database access, and avoid shell execution with request data.
- Keep CORS disabled unless a defined cross-origin use case requires a narrow allowlist.

## Hetzner deployment

- Use a dedicated unprivileged service account. Bind Gunicorn to loopback and expose the application through a maintained reverse proxy with TLS.
- Restrict inbound firewall access to required services. Keep SSH access controlled and the operating system and packages patched.
- Store deployment secrets outside the repository with access limited to the service and administrators. Do not put secrets in deployment scripts or GitHub workflow files.
- Keep debug mode disabled, use trusted-host validation, and avoid logging credentials or unnecessary personal data.

## Dependency and change review

- Keep runtime and development dependencies current. Review Dependabot updates and vulnerability alerts before deployment.
- Run Bandit and pip-audit as part of the implementation and release workflow once application code is added.
- Review changes before merging; use the pull request checklist for secret, security, and deployment impact.
