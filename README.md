# sofeijoada.ch

Python and Flask website for <https://sofeijoada.ch>, deployed using Hetzner + GoDaddy.

## Project status

The website is live at <https://sofeijoada.ch> and includes all 11 customer-supplied language posters. The language button opens a menu of native language names; selecting one performs a full page reload to its own URL, such as `/uk/` for Ukrainian. French is the default.

The header has two page tabs: Home and Menu, with translated labels. The Home page retains the existing language posters. The Menu page (`/fr/menu/`, `/uk/menu/`, and equivalent language routes) displays the supplied dessert and meal bundle artwork. Switching tabs keeps the current language; switching languages keeps the current tab. The one supplied menu poster remains in French, while its controls and readable bundle labels follow the selected language.

The supplied poster artwork is displayed unchanged, with lossless WebP delivery and original PNG fallback. Phone links, WhatsApp ordering, the original ordering QR code, and an expandable readable menu are included. The page scales to the available screen width. No account, online payment processing, database, analytics, or session cookies are used.

## Local environment

Use Python 3.12 or newer. The initial host target remains Python 3.12; the current local environment uses Python 3.14. Create an isolated environment and install the dependencies with:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5050/>. The server binds only to loopback, with debugging and automatic reload disabled. Stop it with Ctrl+C before starting another instance on the same port. Local pages request that search engines do not index them.

For development tools, install `requirements-dev.txt` into the same virtual environment.

The repository includes Flask and Gunicorn as runtime dependencies. Ruff, Bandit, and pip-audit are development tools. Security guidance is in [SECURITY.md](SECURITY.md) and [docs/security-baseline.md](docs/security-baseline.md).

## Files

- `app.py`: read-only routes, host validation, security headers, and the Gunicorn `app:app` entry point.
- `locales.py`: customer poster text and translated website controls.
- `templates/menu.html` and `static/site.css`: exact poster display, language selection, and responsive contact controls.
- `static/images/`: supplied artwork and lossless web versions; see [asset provenance](docs/assets.md).

## Production deployment

Deployed using Hetzner + GoDaddy with HTTPS. See [deployment notes](docs/deployment.md).

## Secrets

Never commit credentials, API tokens, passwords, session keys, private keys, or production configuration. Keep local secrets outside Git and provide production secrets through the host's protected runtime configuration. `.gitignore` excludes common local environment and key files; this is an extra safeguard, not a substitute for reviewing staged changes.

## Repository rights

The repository is public, but no open-source license has been granted. All rights remain with the copyright holder unless a license is added later.
