# Security Policy

## Supported Versions

EssenceMatch is currently in early development. Security fixes are provided
for the latest tagged release and for `main` until the next release is cut.

| Version | Supported          |
|---------|--------------------|
| `main`  | yes                |
| latest  | yes                |
| older   | no                 |

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

Report privately through GitHub Security Advisories by opening a draft
advisory from the repository's **Security** tab.

Include the following so we can triage quickly:

- A clear description of the issue and its impact.
- Reproduction steps, proof-of-concept code, or a minimal demo.
- The commit hash, tag, or release affected.
- Your contact details and preferred disclosure timeline.

We will acknowledge new reports within **3 business days** and aim to ship a
fix or mitigation within **30 days**, depending on severity and complexity.
Coordinated disclosure is appreciated.

## Disclosure Process

1. Maintainers confirm the issue and assign a severity.
2. A fix is developed on a private branch; release notes are drafted.
3. Once a fix is published, the advisory is made public with credit to the
  reporter (unless anonymity is requested).

## Secrets and Configuration

- Never commit `.env` files, real API keys, or production credentials.
- `.gitignore` excludes `.env`; only `.env.example` with safe placeholders
  belongs in the repository.
- Rotate `JWT_SECRET_KEY` and database credentials for every environment.

## Dependency Security

- Backend: `pip-audit` and Dependabot are recommended for continuous
  monitoring.
- Frontend: `npm audit` and Dependabot cover the npm dependency surface.

## Disclaimer

EssenceMatch provides informational wellness guidance only. It is **not** a
medical device and offers no diagnosis or treatment. Security issues that
affect the safety or accuracy of wellness recommendations should be reported
through the channels above.
