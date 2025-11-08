# Test Generator Skill - Documentation

**Claude's QA & Testing Expert**

Automatically generates comprehensive test cases, identifies edge cases, and analyzes code coverage for trading systems.

---

## When Does This Skill Activate?

Claude automatically uses Test Generator when you ask:

- "Wygeneruj testy dla tej funkcji"
- "Jakie są edge cases dla calculate_position_size()?"
- "Jakie pokrycie testowe mamy dla mt5_connector.py?"
- "Napisz testy integracyjne dla API"
- "Czy są dziury w testach tego kodu?"

---

## What It Generates

### 🧪 Unit Tests
- Happy path tests (expected inputs)
- Edge case tests (boundary values)
- Error handling tests (invalid inputs)
- With pytest fixtures and parametrization

### 🔗 Integration Tests
- Function chain testing
- Database interactions
- API endpoint testing
- Multi-service workflows

### 📊 Performance Tests
- Load testing concepts
- Memory efficiency checks
- Execution time benchmarks

### 📋 Test Organization
- Test structure recommendations
- Fixture design patterns
- Mocking strategies
- Parametrized test generation

---

## Real-World Example

### Input Function
```python
def calculate_position_size(account_balance, risk_percent, entry_price, stop_price):
    """Calculate position size based on risk management rules"""
    risk_amount = account_balance * (risk_percent / 100)
    price_difference = abs(entry_price - stop_price)
    position_size = risk_amount / price_difference
    return position_size
```

### Test Generator Response
```
🧪 TEST GENERATION FOR: calculate_position_size()

═══════════════════════════════════════════════════════════

📝 FIXTURES (Setup):

@pytest.fixture
def trading_params():
    return {
        'account_balance': 100000,      # $100k account
        'risk_percent': 2,              # 2% risk per trade
        'entry_price': 1.2500,          # EUR/USD entry
        'stop_price': 1.2450,           # Stop 50 pips
    }

@pytest.fixture
def extreme_params():
    return {
        'account_balance': 1000,        # Small account
        'risk_percent': 0.1,            # Very tight risk
        'entry_price': 0.0001,          # Micro-forex
        'stop_price': 0.00005,          # Tight stop
    }

═══════════════════════════════════════════════════════════

✅ HAPPY PATH TEST:

def test_calculate_position_size_standard(trading_params):
    """Test with typical forex parameters"""
    result = calculate_position_size(**trading_params)

    # Expected: (100000 * 0.02) / (1.2500 - 1.2450) = 40000
    assert result == 40000
    assert isinstance(result, float)

═══════════════════════════════════════════════════════════

🔴 EDGE CASES & BOUNDARIES:

1. Very Small Account (Risk)
   def test_small_account(extreme_params):
       result = calculate_position_size(**extreme_params)
       # (1000 * 0.1) / (0.0001 - 0.00005) = 200000
       assert result == 200000

2. Very Large Risk Percent
   def test_high_risk_percent():
       result = calculate_position_size(10000, 50, 1.2500, 1.2400)
       # (10000 * 50) / (1.2500 - 1.2400) = 5000000
       assert result > 1000000  # Verify calculation

3. Very Tight Stop (Minimal Difference)
   def test_tight_stop():
       result = calculate_position_size(100000, 2, 1.2500, 1.24999)
       # (100000 * 0.02) / 0.00001 = 200000000
       assert result == 200000000  # Huge position

4. Stop Price > Entry (Reverse Trade)
   def test_reverse_stop():
       result = calculate_position_size(100000, 2, 1.2500, 1.2600)
       # (100000 * 0.02) / |1.2500 - 1.2600| = 20000
       assert result == 20000  # abs() handles it

═══════════════════════════════════════════════════════════

❌ ERROR HANDLING TESTS:

1. Zero Account Balance
   def test_zero_balance():
       with pytest.raises(ZeroDivisionError):
           calculate_position_size(0, 2, 1.2500, 1.2450)

2. Zero Price Difference (Entry = Stop)
   def test_zero_price_difference():
       with pytest.raises(ZeroDivisionError):
           calculate_position_size(100000, 2, 1.2500, 1.2500)

3. Negative Risk Percent
   def test_negative_risk():
       result = calculate_position_size(100000, -2, 1.2500, 1.2450)
       assert result < 0  # Negative position = short

4. Invalid Input Types
   def test_invalid_types():
       with pytest.raises(TypeError):
           calculate_position_size("100000", 2, 1.2500, 1.2450)

5. None Values
   def test_none_values():
       with pytest.raises((TypeError, AttributeError)):
           calculate_position_size(None, 2, 1.2500, 1.2450)

═══════════════════════════════════════════════════════════

🔄 PARAMETRIZED TESTS (Test Many Scenarios):

@pytest.mark.parametrize("balance,risk,entry,stop,expected", [
    (100000, 2, 1.2500, 1.2450, 40000),
    (50000,  1, 1.2500, 1.2450, 20000),
    (10000,  5, 1.2500, 1.2450, 200000),
    (1000,   0.1, 1.2500, 1.2450, 4000),
])
def test_calculate_position_size_parametrized(
    balance, risk, entry, stop, expected
):
    result = calculate_position_size(balance, risk, entry, stop)
    assert result == expected

═══════════════════════════════════════════════════════════

📊 TEST COVERAGE ANALYSIS:

Coverage by Line:
Line 1-2:  100% (docstring)
Line 3:    100% (risk_amount calculation)
Line 4:    100% (price_difference calculation)
Line 5:    100% (position_size calculation)
Line 6:    100% (return)

Current Coverage: 100%
Target Coverage: 80%+

═════════════════════════════════════════════════════════════

🎬 EXECUTION:

Run all tests:
$ pytest test_position_size.py -v

Run with coverage:
$ pytest test_position_size.py --cov=.

Run only edge cases:
$ pytest test_position_size.py -k "edge or boundary"

═════════════════════════════════════════════════════════════

📈 SUMMARY:

Total Tests Generated: 14
├─ Happy Path: 1
├─ Edge Cases: 4
├─ Error Handling: 5
└─ Parametrized Variants: 4

Expected Coverage: 100% (all lines executed)
Estimated Run Time: <100ms
```

---

## Common Test Patterns

### Pattern 1: Fixtures for Setup
```python
@pytest.fixture
def mt5_mock():
    """Mock MT5 connection"""
    with patch('core_mt5.MTClientMT5') as mock:
        mock.login.return_value = True
        yield mock
```

### Pattern 2: Parametrization
```python
@pytest.mark.parametrize("input,expected", [
    (100000, 2000),
    (50000, 1000),
])
def test_various_inputs(input, expected):
    assert calculate(input) == expected
```

### Pattern 3: Error Testing
```python
def test_invalid_input():
    with pytest.raises(ValueError):
        function_that_validates()
```

### Pattern 4: Mocking External Services
```python
@patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.status_code = 200
    result = fetch_data()
    assert result is not None
```

---

## Trading-Specific Test Cases

### For MT5 Connector
```python
# Test successful connection
# Test failed authentication
# Test order placement
# Test position retrieval
# Test network timeout handling
# Test reconnection logic
```

### For Risk Manager
```python
# Test position sizing calculations
# Test maximum loss limits
# Test daily loss limits
# Test margin requirements
# Test risk/reward ratios
```

### For Strategy Framework
```python
# Test signal generation
# Test entry conditions
# Test exit conditions
# Test position management
# Test performance metrics
```

---

## Coverage Goals

```
Target Coverage: 80%+

For Trading Core: 90%+ (critical)
For Utilities: 75%+ (acceptable)
For UI/Dashboard: 60%+ (acceptable)
```

---

## FAQ

**Q: How many tests do I need?**
A: Minimum: 1 happy path + 1 error case. Ideal: 5-10 per function.

**Q: Should I test external APIs?**
A: Mock them. Use `@patch` or `responses` library.

**Q: How to test database operations?**
A: Use pytest fixtures with in-memory SQLite for tests.

**Q: Can I test async code?**
A: Yes, use `pytest-asyncio` plugin.

---

## Integration with Other Skills

Use with **Code Reviewer**:
```
"Generate tests for this function, then review them for quality"
```

---

## Support

GitHub: github.com/wasiek91/agentEA/issues
