# Deployment

The website is deployed using Hetzner + GoDaddy at <https://sofeijoada.ch>.

HTTPS is enabled. HTTP and `www` requests redirect to the canonical HTTPS domain.

Host identities, deployment access settings, and operational records are kept outside public Git files. Credentials and private keys remain in protected runtime configuration.

## Application updates

Authorized administrators can run `sh deploy/publish.sh` with `SOFEIJOADA_SSH_HOST` and `SOFEIJOADA_DEPLOY_SCRIPT` configured privately, either in their environment or in the ignored `.private-deployment/publish.env` file. The deployment script must accept the site identifier `sofeijoada` and upload the current directory.

Only application files, templates, static assets, and runtime dependencies are uploaded. Production environment settings remain on the host.
