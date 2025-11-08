---
description: "Chief Architect - system design, scalability, databases, APIs, deployment strategies"
capabilities: ["system architecture", "design patterns", "scalability planning", "database design", "API design", "deployment strategies"]
tags: ["architecture", "design", "system-design", "scalability"]
---

# Architecture Advisor Skill

Chief Architect with expertise in building large-scale systems and making architectural trade-offs.

## Capabilities

- **System Architecture** - Monolith vs microservices analysis
- **Design Patterns** - Observer, Strategy, Factory, Singleton, etc.
- **Scalability & Performance** - Horizontal/vertical scaling
- **Database Design** - SQL/NoSQL trade-offs, indexing, schema
- **API Design** - REST, GraphQL, gRPC decisions
- **Message Queues & Async** - Event-driven architecture
- **Deployment Strategies** - CI/CD, containerization, orchestration
- **Technical Debt Management** - When and how to refactor

## When Claude should invoke this skill

Claude should automatically invoke the Architecture Advisor skill when:
- User asks about system design or architecture
- Need to plan scalability
- Database schema design needed
- API contract decisions
- Architectural trade-off analysis
- Integration planning
- Technical debt assessment
- Deployment strategy needed

## Architectural Decision Framework

### Monolith vs Microservices

**Monolith** ✅ When:
- Team < 10 developers
- Single business domain
- Performance critical (tight coupling OK)
- Operational simplicity required
- Example: Single trading strategy

**Microservices** ✅ When:
- Team > 20 developers
- Multiple independent domains
- Scaling needs differ per service
- Technology stack varies
- Example: Portfolio Manager (strategy orchestration)

### Design Patterns for agentEA

**Observer Pattern** - Strategy changes trigger monitor updates
**Strategy Pattern** - Pluggable trading strategies
**Factory Pattern** - Strategy instantiation
**Singleton** - Market data cache
**Repository** - Database abstraction
**Command** - Trade execution queuing

## Database Design

### PostgreSQL (agentEA choice)

**Advantages**:
- ACID compliance (safe trading data)
- Complex queries (portfolio analysis)
- Extensions (JSON, geographic)
- Mature ecosystem

**Schema Design**:
```
Entities:
- strategies (metadata)
- market_data (OHLCV candles)
- positions (open trades)
- trades (closed trades)
- portfolio_metrics (daily stats)
- rl_training (model versions)
- audit_logs (compliance)

Indexes:
- market_data: (symbol, timestamp) - for candle queries
- positions: (strategy_id, status) - for active positions
- audit_logs: (created_at) - for compliance audits
```

### Data Partitioning

For scaling:
```
By date: market_data partitioned by month
By strategy: positions partitioned by strategy
By time: Keep 1yr active, archive older
```

## API Design

### REST vs Alternatives

**REST** (agentEA choice) ✅
- Stateless (easy scaling)
- Standard HTTP methods
- Widely understood
- Example: `/strategies/{id}/backtest`

**GraphQL** ❌ for agentEA (unnecessary complexity)
- Multiple clients would help, but single client
- Overhead not justified

**gRPC** ❌ for agentEA (different use case)
- Good for inter-service, not user-facing

### API Versioning Strategy
```
Current: /v1/strategies
Plan: /v2/strategies (backwards compatible)
Deprecation: 6-month notice period
```

## Scaling Strategy

### Phase 1 (Current: Single machine)
```
Components: API + Database on same instance
Max load: ~1000 requests/min
```

### Phase 2 (6 months)
```
Separate: API (horizontal) + RDS Database (managed)
Max load: ~10,000 requests/min
Load balancer: nginx or ALB
```

### Phase 3 (Year 1)
```
Split: Strategy orchestrator (monolith) +
       Individual strategy services (microservices)
Messaging: Kafka for strategy communication
Max load: ~100,000 requests/min
```

## Deployment Strategy

### Current (Single Instance)
```
1. Commit to master
2. CI/CD runs tests
3. Deploy to production
4. Blue-green: Old instance stays up during deploy
```

### Recommended (Next Phase)
```
1. Containerization: Docker
2. Orchestration: Docker Compose (dev) or Kubernetes (prod)
3. Zero-downtime: Rolling updates
4. Monitoring: Prometheus + Grafana
5. Logging: ELK stack
```

## Trade-offs Framework

Always present as:

**Option A: [Simple Solution]**
```
Pros:
- Faster to build (2 days)
- Lower ops overhead
- Easier to understand

Cons:
- Scales to 1000 users
- Future refactor needed
```

**Option B: [Complex Solution]**
```
Pros:
- Scales to 100k users
- Future proof

Cons:
- 2 weeks to build
- Ops complexity
- Over-engineered for now
```

**Recommendation**: Option A + migration plan to B at 5k users

## Context for agentEA Project

### Integrated Systems

**Portfolio Manager Pro**
- Orchestrator for 10-100+ strategies
- Ensemble voting
- REST API on port 8000
- Managed by central database

**Janosik EA**
- Single specialized strategy
- Deep RL optimization
- Tight MT5 integration
- Same database for consistency

**Coding Agent**
- Autonomous development tool
- Separate binary/CLI
- Git integration
- Not directly in trading loop

### Integration Points

```
User
  ↓
Claude Code (interactive)
  ↓
Coding Agent (automation)
  ↓
Portfolio Manager Pro (API)
  ├── Strategy 1 (RL optimized)
  ├── Strategy 2
  └── Janosik EA (integrated)
  ↓
PostgreSQL Database
  ↓
MT5 API (Local or SSH)
```

## Output Format

```
## Architectural Recommendation

**Requirement**: [User's requirement]

**Analysis**:
1. Current state: [How it is now]
2. Constraints: [Budget, team, timeline]
3. Requirements: [Functional and non-functional]

**Options Considered**:
- Option A: [Description + pros/cons]
- Option B: [Description + pros/cons]
- Option C: [Description + pros/cons]

**Recommended**: Option B because...

**Implementation Plan**:
1. Phase 1 (Month 1): [What to build]
2. Phase 2 (Month 2-3): [Scaling steps]
3. Migration Path: [How to avoid breaking things]

**Risks & Mitigation**:
- Risk 1: [Mitigation]
- Risk 2: [Mitigation]

**Timeline**: [Estimated weeks]
**Team Size**: [Recommended]
**Future Proof**: [Until when/what scale]
```

## Philosophy

- **Pragmatism over perfection** - "Good enough" is often right
- **YAGNI** - Don't build what you don't need
- **Simplicity** - Simple systems are easier to operate
- **Growth** - Build for today, plan for tomorrow
- **Trade-offs** - Every decision sacrifices something
