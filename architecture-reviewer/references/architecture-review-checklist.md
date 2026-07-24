# Architecture Review Checklist

## Scalability & Performance
- Can the system handle expected load?
- Are there obvious bottlenecks or single points of failure?
- Is caching, sharding, or scaling strategy considered?

## Maintainability & Modularity
- Is the system properly modular and loosely coupled?
- Are responsibilities clearly separated?
- Is the architecture future-proof for likely changes?

## Security & Compliance
- Are security boundaries clearly defined?
- Is sensitive data handled appropriately?
- Are authentication, authorization, and audit requirements addressed?

## Reliability & Resilience
- What happens on failure of key components?
- Are retries, circuit breakers, or fallback strategies defined?
- Is observability (logging, metrics, tracing) sufficient?

## Technology Choices
- Are the chosen technologies appropriate and well understood by the team?
- Are there vendor lock-in or licensing concerns?
- Is the stack consistent with organizational standards?

## Trade-offs
- Are trade-offs explicitly documented?
- Are alternatives considered and reasons for rejection clear?
