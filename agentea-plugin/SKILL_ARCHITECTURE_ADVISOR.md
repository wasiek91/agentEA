# Architecture Advisor Skill - Documentation

**Claude's System Design Expert**

Specializes in architectural decisions, system design patterns, scalability, and technical trade-offs for the agentEA ecosystem.

---

## When Does This Skill Activate?

Claude automatically uses the Architecture Advisor skill when you ask:

- "Czy powinienem używać microservices czy monolith?"
- "Jak skalować Portfolio Manager Pro?"
- "Jak projektować API dla systemu handlu?"
- "Jakie są trade-offs między X a Y?"
- "Jak integować Janosik EA z Portfolio Manager?"

---

## What It Addresses

### 🏗️ Architecture Patterns
- Monolith vs Microservices vs Serverless
- Layered architecture
- Event-driven architecture
- Database per service
- API Gateway patterns

### 📈 Scalability
- Horizontal vs vertical scaling
- Load balancing strategies
- Database scaling (sharding, replication)
- Caching strategies (Redis, in-memory)
- Queue systems for async processing

### 🗄️ Database Design
- Schema optimization
- Indexing strategies
- Replication & failover
- Backup strategies
- NoSQL vs Relational trade-offs

### 🔌 API Design
- RESTful principles
- GraphQL vs REST
- Versioning strategies
- Rate limiting
- Authentication & authorization

### 🚀 Deployment
- Docker containerization
- Kubernetes orchestration
- CI/CD pipelines
- Blue-green deployments
- Rollback strategies

### 🏥 Reliability
- High availability setup
- Disaster recovery
- Circuit breakers
- Graceful degradation
- Monitoring & alerting

---

## Real-World Example: agentEA Architecture

### Question
```
"Jak architektować system handlu rozproszonego z Portfolio Manager Pro,
Janosik EA i Coding Agent? Monolith vs microservices?"
```

### Architecture Advisor Response
```
🏗️ ARCHITECTURE RECOMMENDATION FOR agentEA

Current Setup: 3 loosely coupled systems
├─ Portfolio Manager Pro (10-100+ strategies, high complexity)
├─ Janosik EA (1-2 specialized, low latency critical)
└─ Coding Agent (batch operations, not real-time)

═════════════════════════════════════════════════════════════

🎯 RECOMMENDATION: HYBRID ARCHITECTURE

Trading Core (Monolith) + Support Services (Microservices)

┌─────────────────────────────────────────┐
│  TRADING CORE (Single Process)          │ ← Critical Path
│  ├─ Portfolio Manager Pro               │   No network latency
│  ├─ Janosik EA                         │   Atomic operations
│  ├─ Shared Risk Manager                │   Easy state sharing
│  └─ MT5 Connector                      │
└──────────────┬──────────────────────────┘
               │ REST API (port 8000)
               ↓
┌──────────────────────────────┐
│  Support Services            │ ← Can Scale Independently
│  ├─ Dashboard (Dash)        │   Async processing
│  ├─ Analytics Service       │   External queries
│  ├─ Backtesting Service     │
│  └─ Coding Agent Wrapper    │
└──────────────────────────────┘
               │
        ┌──────┴──────┐
        ↓             ↓
   PostgreSQL    Message Queue
   (Primary)     (Redis/RabbitMQ)

═════════════════════════════════════════════════════════════

WHY THIS APPROACH:

✅ Advantages:
- Trading latency: <10ms (local calls, no network)
- Risk management: Centralized, atomic
- Scalability: Support services scale independently
- Reliability: Core isolated from dashboard crashes
- Simplicity: No distributed transactions needed

⚠️  Trade-offs Avoided:
- ❌ Full microservices would add 50-200ms latency (unacceptable for trading)
- ❌ Monolith would create scaling bottleneck for analytics
- ✅ Hybrid provides best of both

═════════════════════════════════════════════════════════════

IMPLEMENTATION PHASES:

Phase 1: Core Consolidation (Week 1)
├─ Move Portfolio Manager + Janosik to shared trading-core/
├─ Consolidate MT5 connector
└─ Use same PostgreSQL connection pool

Phase 2: REST API Wrapper (Week 2)
├─ FastAPI on top of trading-core
├─ Dashboard connects via REST
└─ Rate limiting: 100 req/sec

Phase 3: Support Microservices (Week 3-4)
├─ Backtesting Service (separate docker)
├─ Analytics Service (read replica)
├─ Coding Agent Wrapper (async queue)

═════════════════════════════════════════════════════════════

DATABASE STRATEGY:

Master-Replica Setup:
┌─ PostgreSQL Master (Write) ← Trading Core
│  ├─ Real-time trades, positions, signals
│  └─ Replication lag: <1ms
│
└─ PostgreSQL Replica (Read) ← Support Services
   ├─ Dashboard queries
   ├─ Analytics
   └─ Replication lag: 100-500ms (acceptable)

═════════════════════════════════════════════════════════════

DEPLOYMENT STRUCTURE:

docker-compose.yml:
services:
  trading-core:           # Monolith
    image: agentea:latest
    environment:
      PORTFOLIO_MGR=true
      JANOSIK_EA=true
    restart: always       # Critical!

  api-server:            # REST wrapper
    depends_on: trading-core
    ports: 8000:8000

  dashboard:             # Microservice
    ports: 8050:8050
    depends_on: postgresql

  backtesting:           # Microservice
    profiles: ['optional']

═════════════════════════════════════════════════════════════

MONITORING STRATEGY:

Critical Alerts:
- Trading core uptime < 99.9%
- API latency > 100ms
- Database replication lag > 5s

Dashboard Metrics:
- Requests per second
- Error rate
- Average response time
```

---

## Common Architecture Decisions

### Decision 1: REST vs gRPC

**For Portfolio Manager REST API:**
```
✅ REST (Better choice)
- Dashboard uses standard HTTP
- Mobile-friendly
- Easy debugging
- Latency: ~50ms acceptable for management API
```

**For Trading Core → Support Services:**
```
✅ Message Queue (Better choice)
- Async, no latency requirements
- Decoupled systems
- Scales well
```

---

### Decision 2: Caching Strategy

```python
# Cache trading metrics (ttl: 1 minute)
CACHE_CONFIG = {
    'strategy_performance': 60,
    'portfolio_metrics': 60,
    'risk_levels': 30,
}

# Don't cache:
# - Real-time positions
# - Current orders
# - Account balance
```

---

### Decision 3: Error Handling

```
API Error Codes:
200 - Order executed
400 - Invalid parameters
409 - Insufficient funds (recoverable)
500 - System error (retry after 5s)
503 - Trading core offline (critical)
```

---

## FAQ

**Q: Should each strategy be separate microservice?**
A: No. Keep all strategies in Portfolio Manager core. Microservices add too much latency for trading.

**Q: How to handle failover?**
A: Hot standby on separate VPS. Watchdog checks core every 5s, fails over if timeout.

**Q: How many database replicas?**
A: 1 for production (master + 1 replica). Use read pooling for load distribution.

**Q: Can we use Kubernetes?**
A: Only for support services. Trading core should run on single powerful machine for latency.

---

## Integration with Other Skills

Use with **Code Reviewer**:
```
"Design the trading core architecture, then review for security"
```

---

## Support

GitHub: github.com/wasiek91/agentEA/issues
