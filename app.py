"""Public, read-only Flask website for SóFeijoada."""

import os

from flask import Flask, Response, abort, redirect, render_template, url_for

from locales import LANGUAGES, PAGE_LABELS


def create_app() -> Flask:
    application = Flask(__name__)
    environment = os.environ.get("SOFEIJOADA_ENV", "local")
    if environment not in {"local", "production"}:
        raise RuntimeError("SOFEIJOADA_ENV must be local or production")

    application.config.update(
        DEBUG=False,
        TESTING=False,
        TRUSTED_HOSTS=[
            "localhost",
            "127.0.0.1",
            "[::1]",
            "sofeijoada.ch",
            "www.sofeijoada.ch",
        ],
        MAX_CONTENT_LENGTH=16 * 1024,
        MAX_FORM_MEMORY_SIZE=16 * 1024,
        MAX_FORM_PARTS=10,
        SEND_FILE_MAX_AGE_DEFAULT=3600,
    )

    @application.after_request
    def security_headers(response: Response) -> Response:
        response.headers["Content-Security-Policy"] = (
            "default-src 'none'; "
            "img-src 'self'; style-src 'self'; script-src 'self'; "
            "font-src 'self'; connect-src 'none'; "
            "base-uri 'none'; object-src 'none'; frame-ancestors 'none'; "
            "form-action 'none'; require-trusted-types-for 'script'"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), payment=()"
        )
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        if environment == "local":
            response.headers["X-Robots-Tag"] = "noindex, nofollow"
        return response

    def render_page(language: str, *, menu_page: bool = False) -> str:
        if language not in LANGUAGES:
            abort(404)
        return render_template(
            "menu.html",
            language=language,
            copy=LANGUAGES[language],
            navigation=PAGE_LABELS[language],
            languages=LANGUAGES,
            menu_page=menu_page,
            page_endpoint="food_menu" if menu_page else "menu",
            poster_file="menu-poster" if menu_page else f"poster-{language}",
            poster_width=850 if menu_page else 1414,
            poster_height=1277 if menu_page else 2000,
            phone_display="076.210.70.87",
            phone_url="tel:+41762107087",
            # Direct WhatsApp destination resolved from the customer's QR code.
            whatsapp_url="https://api.whatsapp.com/qr/2QYGW7RO5DIOL1",
        )

    @application.get("/")
    def index() -> Response:
        return redirect(url_for("menu", language="fr"), code=302)

    @application.get("/<language>/")
    def menu(language: str) -> str:
        return render_page(language)

    @application.get("/<language>/menu/")
    def food_menu(language: str) -> str:
        return render_page(language, menu_page=True)

    @application.get("/menu/")
    def menu_index() -> Response:
        return redirect(url_for("food_menu", language="fr"), code=302)

    @application.get("/healthz")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @application.get("/robots.txt")
    def robots() -> Response:
        rule = "Allow: /" if environment == "production" else "Disallow: /"
        return Response(f"User-agent: *\n{rule}\n", mimetype="text/plain")

    @application.errorhandler(404)
    def not_found(_error: Exception) -> tuple[str, int]:
        return render_template("error.html", code=404, message="Page introuvable"), 404

    return application


# The existing shared host's Gunicorn service imports app:app.
app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=False, use_reloader=False)
