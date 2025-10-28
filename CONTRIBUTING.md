# 🤝 Contributing to PolyWhale

Thank you for your interest in contributing to PolyWhale! This document provides guidelines for contributing.

---

## 🎯 Ways to Contribute

### 1. Report Bugs
- Use GitHub Issues
- Include detailed description
- Provide steps to reproduce
- Include error messages/logs

### 2. Suggest Features
- Open a GitHub Issue
- Describe the feature
- Explain the use case
- Discuss implementation ideas

### 3. Submit Code
- Fork the repository
- Create a feature branch
- Write clean, documented code
- Submit a pull request

### 4. Improve Documentation
- Fix typos
- Add examples
- Clarify instructions
- Translate to other languages

---

## 🔧 Development Setup

### 1. Fork and Clone

```bash
# Fork on GitHub, then clone
git clone https://github.com/yourusername/polywhale.git
cd polywhale
```

### 2. Set Up Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest pytest-asyncio black flake8 mypy
```

### 3. Configure

```bash
# Copy environment file
cp .env.example .env

# Edit .env with your test credentials
```

### 4. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=bot

# Run specific test
pytest tests/test_models.py
```

---

## 📝 Code Style

### Python Style Guide

We follow PEP 8 with some modifications:

```python
# Good
def fetch_whale_trades(address: str, limit: int = 10) -> List[Trade]:
    """
    Fetch trades for a specific whale
    
    Args:
        address: Ethereum address
        limit: Maximum number of trades
        
    Returns:
        List of Trade objects
    """
    pass

# Bad
def fetch_whale_trades(address,limit=10):
    pass
```

### Formatting

Use Black for formatting:

```bash
# Format all files
black .

# Check formatting
black --check .
```

### Linting

Use Flake8 for linting:

```bash
# Lint all files
flake8 .

# Ignore specific errors
flake8 --ignore=E501,W503 .
```

### Type Hints

Use type hints for all functions:

```python
from typing import List, Optional

def get_whale(address: str) -> Optional[Whale]:
    pass

async def fetch_trades(limit: int) -> List[Trade]:
    pass
```

---

## 🌿 Git Workflow

### Branch Naming

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Test additions

Examples:
- `feature/whale-consensus`
- `fix/database-connection`
- `docs/api-documentation`

### Commit Messages

Follow conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting
- `refactor` - Code restructuring
- `test` - Tests
- `chore` - Maintenance

Examples:
```
feat(whale): add whale consensus calculation

fix(database): handle connection timeout

docs(readme): update installation instructions
```

---

## 🔄 Pull Request Process

### 1. Create Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write clean code
- Add tests
- Update documentation
- Follow style guide

### 3. Test

```bash
# Run tests
pytest

# Format code
black .

# Lint code
flake8 .
```

### 4. Commit

```bash
git add .
git commit -m "feat(scope): description"
```

### 5. Push

```bash
git push origin feature/your-feature-name
```

### 6. Create Pull Request

- Go to GitHub
- Click "New Pull Request"
- Fill in template
- Request review

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Refactoring

## Testing
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Manual testing done

## Checklist
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Commits are clean
```

---

## 🧪 Testing Guidelines

### Unit Tests

```python
# tests/test_models.py
import pytest
from bot.models import Trade

def test_trade_is_whale():
    trade = Trade(
        id="test",
        trader_address="0x123",
        market_id="market1",
        side="BUY",
        size=15000,
        price=0.5,
        timestamp=datetime.now()
    )
    assert trade.is_whale_trade == True
```

### Integration Tests

```python
# tests/test_api.py
import pytest
from bot.services.polymarket_api import PolymarketAPI

@pytest.mark.asyncio
async def test_fetch_trades():
    api = PolymarketAPI()
    trades = await api.fetch_recent_trades(limit=5)
    assert len(trades) > 0
    await api.close()
```

### Test Coverage

Aim for >80% coverage:

```bash
pytest --cov=bot --cov-report=html
```

---

## 📚 Documentation

### Code Documentation

```python
def calculate_win_rate(wins: int, losses: int) -> float:
    """
    Calculate win rate percentage
    
    Args:
        wins: Number of winning trades
        losses: Number of losing trades
        
    Returns:
        Win rate as percentage (0-100)
        
    Examples:
        >>> calculate_win_rate(80, 20)
        80.0
    """
    total = wins + losses
    if total == 0:
        return 0.0
    return (wins / total) * 100
```

### README Updates

When adding features, update:
- Feature list
- Command list
- Examples
- Screenshots

---

## 🐛 Bug Reports

### Good Bug Report

```markdown
**Description**
Bot crashes when fetching whale trades

**Steps to Reproduce**
1. Run `python main.py`
2. Send `/whales` command
3. Bot crashes

**Expected Behavior**
Should show recent whale trades

**Actual Behavior**
Bot crashes with error:
```
KeyError: 'market_name'
```

**Environment**
- OS: Windows 11
- Python: 3.11.5
- Bot version: 1.0.0

**Logs**
[Attach relevant logs]
```

---

## 💡 Feature Requests

### Good Feature Request

```markdown
**Feature Name**
Whale Portfolio Tracking

**Problem**
Users want to see all positions held by a whale

**Proposed Solution**
Add `/portfolio <address>` command that shows:
- All active positions
- Total value
- Profit/loss

**Alternatives Considered**
- Show in whale profile
- Separate command (preferred)

**Additional Context**
Similar to Polymarket's portfolio view
```

---

## 🎨 Design Principles

1. **Keep it simple** - Don't over-engineer
2. **User first** - Focus on user experience
3. **Performance** - Optimize for speed
4. **Reliability** - Handle errors gracefully
5. **Maintainability** - Write clean, documented code

---

## 📞 Communication

- **GitHub Issues** - Bug reports, features
- **Pull Requests** - Code contributions
- **Discussions** - General questions
- **Twitter** - [@Zun2025](https://x.com/Zun2025)

---

## 🏆 Recognition

Contributors will be:
- Listed in README
- Mentioned in release notes
- Credited in documentation

---

## ❓ Questions?

Feel free to:
- Open a GitHub Discussion
- Comment on issues
- Reach out on Twitter

---

**Thank you for contributing to PolyWhale! 🐋**

