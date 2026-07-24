# Security Review Checklist

## Authentication & Authorization
- Proper authentication is used
- Authorization checks are present on sensitive endpoints
- No hardcoded credentials or secrets

## Input Validation & Sanitization
- All user input is validated
- No SQL injection, XSS, or command injection risks
- Proper escaping is used where needed

## Data Protection
- Sensitive data is encrypted at rest and in transit
- Secrets are managed securely (no hardcoding)
- PII handling complies with privacy requirements

## Error Handling & Logging
- Errors do not leak sensitive information
- Logging does not include secrets or PII

## Dependencies & Configuration
- Dependencies are up to date with no known vulnerabilities
- Security headers are configured
- CORS and CSP are properly set

## Common Vulnerabilities
- OWASP Top 10 issues are addressed
- Rate limiting is in place where appropriate
- Secure defaults are used
