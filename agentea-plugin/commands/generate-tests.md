---
allowed-tools: Read, Write, Edit, Bash(python:*), Bash(npm test:*)
description: Generuj test template dla funkcji lub modułu
argument-hint: [function-name] [file-path]
---

# Generate Test Template

Wygeneruj szablony testów dla: `$1` w pliku `$2`

## Parametry:

- **Function/Module Name**: `$1` (wymagane)
- **File Path**: `$2` (opcjonalne - default: $1.py)

## Proces:

### 1. **Analiza funkcji**
- Wczytaj plik: `$2`
- Znajdź funkcję: `$1`
- Wyekstrahuj:
  - Input parameters
  - Return type
  - Exceptions
  - Dependencies

### 2. **Identyfikuj test cases**

**Happy Path**:
```
- Standardowe inputs
- Oczekiwane outputs
- Normal flow
```

**Edge Cases**:
```
- Empty input
- None/null values
- Max/min values
- Boundary conditions
```

**Error Cases**:
```
- Invalid types
- Out of range
- Missing dependencies
- Exception handling
```

### 3. **Wygeneruj test template**

```python
# Format: pytest

import pytest
from $2 import $1

class Test$1:
    """Tests for $1 function"""

    def setup_method(self):
        """Setup test fixtures"""
        pass

    def test_$1_happy_path(self):
        """Test normal operation"""
        # Arrange
        input_data = ...
        expected = ...

        # Act
        result = $1(input_data)

        # Assert
        assert result == expected

    def test_$1_edge_case_empty(self):
        """Test with empty input"""
        result = $1([])
        assert result == expected

    def test_$1_edge_case_none(self):
        """Test with None input"""
        with pytest.raises(ValueError):
            $1(None)

    def test_$1_error_handling(self):
        """Test error handling"""
        with pytest.raises(TypeError):
            $1("invalid")

    @pytest.mark.parametrize("input,expected", [
        (value1, output1),
        (value2, output2),
    ])
    def test_$1_parametrized(self, input, expected):
        """Parametrized test"""
        assert $1(input) == expected
```

### 4. **Dodaj do test file**
- Jeśli plik testów istnieje: append
- Jeśli nie istnieje: create new `test_$2`

### 5. **Validate tests**
```bash
pytest test_$2.py::Test$1 -v
```

## Coverage Goals:

- ✅ Minimum 80% line coverage
- ✅ Wszystkie branches testowane
- ✅ All exceptions tested
- ✅ Parametrized tests dla variants

## Integracja z workflow:

1. **Napisz feature**: `new_feature.py`
2. **Szybki test**: `/generate-tests feature_func new_feature.py`
3. **Przegląd**: Agenci review
4. **Głębokie testy**: Agenci testy

## Output format:

```
## Test Template: $1

**File**: $2

**Test Cases Generated**:
- Happy Path: [1]
- Edge Cases: [N]
- Error Cases: [N]

**Coverage**: [%]
**Status**: Ready to implement

**Next Steps**:
1. Implement test body
2. Run: pytest
3. Achieve 80%+ coverage
```
