---
description: "QA Automation expert - comprehensive testing, edge cases, coverage analysis, test generation"
capabilities: ["unit testing", "integration testing", "edge case identification", "test coverage analysis", "mocking", "test automation"]
tags: ["testing", "qa", "test-generation", "quality-assurance"]
---

# Test Generator Skill

QA Automation expert specializing in comprehensive test generation and ensuring high code quality through rigorous testing.

## Capabilities

- **Unit Testing** - pytest, unittest frameworks
- **Integration Testing** - Component interaction verification
- **End-to-End Testing** - Full workflow validation
- **Edge Case Identification** - Boundary condition discovery
- **Mocking & Fixtures** - Dependency isolation
- **Performance Testing** - Benchmark and load testing
- **Test Coverage Analysis** - Line and branch coverage

## When Claude should invoke this skill

Claude should automatically invoke the Test Generator skill when:
- User requests test generation or implementation
- Code needs higher coverage
- Edge cases should be identified
- Test suite needs comprehensive coverage (target: 80%+)
- Performance tests needed
- Integration tests required
- Regression test suite needed

## Testing Framework Selection

### Python (agentEA primary language)
```
Unit Testing:       pytest (preferred) or unittest
Coverage:           pytest-cov
Mocking:           unittest.mock or pytest-mock
Fixtures:          pytest fixtures
Parametrization:   pytest.mark.parametrize
```

### JavaScript (if needed)
```
Unit Testing:      Jest or Mocha
Coverage:          Istanbul/nyc
Mocking:          Jest automocking
Fixtures:         Jest setup files
```

## Test Hierarchy

```
Unit Tests         80% (test individual functions)
Integration Tests  15% (test component interaction)
End-to-End Tests   5% (test full workflows)
```

## Test Structure (AAA Pattern)

```python
# Arrange: Setup test data
# Act: Call the function
# Assert: Verify the result

def test_calculate_sharpe_ratio():
    # Arrange
    returns = [0.01, 0.02, -0.01, 0.03]
    expected = 1.25

    # Act
    result = calculate_sharpe_ratio(returns)

    # Assert
    assert abs(result - expected) < 0.01
```

## Test Cases Checklist

### Happy Path (Normal Operation)
- Valid inputs
- Expected outputs
- Normal flow execution
- Example: `test_strategy_valid_parameters()`

### Edge Cases (Boundary Conditions)
- Empty input
- Single element
- Maximum/minimum values
- Special characters
- Examples:
  - `test_empty_market_data()`
  - `test_max_position_size()`
  - `test_zero_capital()`

### Error Cases (Exception Handling)
- Invalid types
- Out of range values
- Missing dependencies
- Network failures
- Examples:
  - `test_invalid_symbol_type()`
  - `test_negative_capital_raises_error()`
  - `test_database_connection_failure()`

### Performance Cases (Non-functional)
- Large datasets
- Timeout scenarios
- Memory usage
- Concurrency issues
- Examples:
  - `test_backtest_1000_trades_performance()`
  - `test_portfolio_update_latency()`

## Test Organization

```
project/
├── src/
│   ├── trading/
│   │   ├── strategy.py
│   │   └── risk_manager.py
│   └── rl/
│       └── agent.py
└── tests/
    ├── unit/
    │   ├── test_strategy.py
    │   ├── test_risk_manager.py
    │   └── test_agent.py
    ├── integration/
    │   ├── test_strategy_api.py
    │   └── test_rl_training.py
    └── conftest.py (shared fixtures)
```

## Fixture and Mock Usage

### Fixtures (Test Data)
```python
@pytest.fixture
def market_data():
    return pd.DataFrame({
        'time': [...],
        'open': [...],
        'close': [...]
    })

def test_strategy_with_data(market_data):
    # Use fixture here
    pass
```

### Mocks (External Dependencies)
```python
from unittest.mock import patch, MagicMock

@patch('mt5_api.get_balance')
def test_balance_check(mock_balance):
    mock_balance.return_value = 100000
    result = check_trading_capital()
    assert result == 100000
```

## Coverage Targets

```
Overall:           80%+ (minimum)
Critical paths:    100% (trading logic)
Error handling:    90%+ (risk management)
Utils:             70%+ (nice to have)

Commands to measure:
pytest --cov=src tests/
pytest --cov=src --cov-report=html tests/
```

## Test Naming Convention

**Good Names** (Descriptive):
- `test_calculate_sharpe_ratio_with_positive_returns()`
- `test_position_sizing_respects_max_risk()`
- `test_mt5_connection_failure_handled_gracefully()`

**Bad Names** (Unclear):
- `test1()`
- `test_strategy()`
- `test_error()`

## Test Execution

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/unit/test_strategy.py

# Run with coverage
pytest --cov=src tests/

# Run with verbosity
pytest -v tests/

# Run failing tests first
pytest --lf tests/

# Parallel execution
pytest -n auto tests/
```

## Context for agentEA Project

### Trading-Specific Test Cases

**Strategy Testing**:
```
- Valid entry/exit signals
- Position sizing within limits
- Risk management enforcement
- Stop-loss triggers
- Portfolio ensemble voting
```

**RL Model Testing**:
```
- Convergence detection
- Reward calculation accuracy
- Action space validation
- Environment reset correctness
- Deterministic mode (for testing)
```

**Risk Management Testing**:
```
- Daily loss limit enforcement
- Maximum position size validation
- Drawdown threshold triggers
- Correlation risk calculation
- Exposure limits per asset
```

**API Integration Testing**:
```
- Strategy CRUD operations
- Backtest execution
- Model training workflow
- Data persistence
- Concurrent requests
```

### Mock Data Fixtures

```python
@pytest.fixture
def trading_account():
    return {
        'balance': 100000,
        'equity': 100000,
        'margin': 0,
        'free_margin': 100000
    }

@pytest.fixture
def market_snapshot():
    return {
        'EURUSD': {'bid': 1.0850, 'ask': 1.0851},
        'GBPUSD': {'bid': 1.2650, 'ask': 1.2651},
        'XAUUSD': {'bid': 1850.5, 'ask': 1851.0}
    }
```

## Output Format

```
## Test Generation Results

**Target**: [function/module name]

**Test Cases Generated**:
- Happy Path: [N tests]
- Edge Cases: [N tests]
- Error Cases: [N tests]
- Performance: [N tests]

**Total**: [N tests]

**Coverage**:
- Line Coverage: [%]
- Branch Coverage: [%]

**Test Files**:
- tests/unit/test_[module].py
- tests/integration/test_[feature].py

**Fixtures Created**:
- [fixture_1]
- [fixture_2]

**Next Steps**:
1. Implement test bodies
2. Add specific assertions
3. Run: `pytest --cov`
4. Achieve 80%+ coverage
5. Review edge cases

**Estimated Implementation Time**: [hours]
```

## Best Practices

✅ **DO**:
- Write tests before or with code (TDD)
- Use descriptive test names
- Keep tests independent (no shared state)
- Mock external dependencies
- Test both success and failure paths
- Maintain > 80% coverage

❌ **DON'T**:
- Test implementation details (test behavior)
- Share state between tests
- Use sleep() for timing
- Hardcode test data
- Test library code
- Create brittle tests
