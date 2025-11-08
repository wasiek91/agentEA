# RL Expert Skill - Documentation

**Claude's Reinforcement Learning Specialist**

Expert in optimizing trading strategies using advanced RL algorithms, hyperparameter tuning, and performance metrics.

---

## When Does This Skill Activate?

Claude automatically uses the RL Expert skill when you ask:

- "Jak zoptymalizować mój model RL?"
- "Mam problemy z konwergencją. Sharpe ratio 0.6 zamiast 1.0"
- "Jakie hiperparametry powinienem tunować?"
- "Jak zaprojektować reward function dla handlu?"
- "Model się nie uczy. Co robić?"

---

## What It Covers

### 🤖 RL Algorithms
- **PPO** (Proximal Policy Optimization) - stable, good for trading
- **DQN** (Deep Q-Network) - discrete actions
- **A3C** (Asynchronous Advantage Actor-Critic) - parallel training
- **DDPG** (Deep Deterministic Policy Gradient) - continuous control
- **SAC** (Soft Actor-Critic) - sample efficient, exploration

### 📊 Trading Metrics
- **Sharpe Ratio** - return/risk balance (target > 1.0)
- **Maximum Drawdown** - worst peak-to-trough decline
- **Win Rate** - % profitable trades
- **Profit Factor** - gross profit / gross loss
- **Sortino Ratio** - downside volatility adjusted

### 🎯 Hyperparameter Tuning
- Learning rates (`3e-4` to `3e-5`)
- Network architecture (layers, units)
- Batch size & steps (exploration/exploitation trade-off)
- Gamma, Lambda, entropy coefficient
- Update frequencies

### 🏆 Common Problems & Solutions
- Low Sharpe Ratio
- Convergence Issues
- Reward Shaping
- Exploration vs Exploitation
- Sample Efficiency

---

## Real-World Example

### Problem
```
"Model RL ma Sharpe ratio 0.6 ale potrzebuje 1.0. Co robić?"
```

### RL Expert Response
```
🎯 RL OPTIMIZATION STRATEGY - Sharpe Ratio 0.6 → 1.0+

Current Status: Below target (need +67% improvement)

🔴 ROOT CAUSES (likely):
1. Reward function not capturing risk-adjusted returns
2. Hyperparameters not optimized for forex trading
3. Network too small for complex patterns
4. Insufficient historical data / lookback window

✅ QUICK FIXES (try first - 30 min each):

1. Add Sharpe bonus to reward function
   reward = profit - 0.1 * loss - commission + bonus_if_sharpe_high

2. Increase network complexity
   From: Dense(64) → Dense(64)
   To:   Dense(128) → Dense(128) → Dense(64)

3. Adjust PPO hyperparameters (for forex):
   n_steps = 512        (↓ from 2048 - faster reactions)
   batch_size = 128     (↑ from 64 - stable updates)
   n_epochs = 20        (↑ from 10 - better convergence)

4. Add risk penalty to state:
   Include: volatility, drawdown, win_rate in state space

⏱️ EXPECTED TIMELINE:
- After 50k steps: Sharpe ~0.75
- After 100k steps: Sharpe ~1.0+
- After 200k steps: Sharpe 1.2-1.5 (stable)

🎬 IMPLEMENTATION STEPS:
1. Update reward function (portfolio-manager-pro/rl_engine.py:163)
2. Add features to state space (add ATR, drawdown, win_rate)
3. Modify hyperparameters in config
4. Retrain with: python rl_engine.py --total_timesteps 100000
5. Monitor: Track Sharpe ratio every 5k steps

ESTIMATED TIME: 4-6 hours implementation + 12+ hours training
```

---

## Common Optimization Problems

### Problem 1: Low Sharpe Ratio (< 0.5)

**Symptoms:** High returns but too volatile

**Solutions (in order):**
1. Add Sharpe bonus to reward function
2. Increase risk penalty weight
3. Add drawdown limit to reward
4. Increase network size
5. More training steps (100k → 200k)

---

### Problem 2: Convergence Issues

**Symptoms:** Loss oscillating, not improving

**Solutions:**
1. Reduce learning rate (1e-3 → 1e-4)
2. Increase batch size (32 → 128)
3. Stabilize reward signal
4. Add entropy bonus for exploration
5. Reduce epsilon-greedy decay rate

---

### Problem 3: Overfit/Overly Optimistic

**Symptoms:** Great backtest, bad live trading

**Solutions:**
1. Reduce training data percentage in validation
2. Add noise to training data
3. Early stopping when validation diverges
4. Regularize network weights
5. Train on shorter lookback windows

---

## Trading-Specific Recommendations

### For Forex (like Janosik EA)
```python
# Recommended PPO settings for forex
PPO_CONFIG = {
    'learning_rate': 3e-4,
    'n_steps': 512,              # Responsive to market changes
    'batch_size': 128,
    'n_epochs': 20,
    'gamma': 0.97,               # Prioritize recent rewards
    'gae_lambda': 0.95,
    'ent_coef': 0.01,            # Explore more
    'max_grad_norm': 0.5,        # Stable gradients
}

# Reward engineering for forex
def compute_reward(profit, loss, sharpe, drawdown):
    base_reward = profit - 2 * loss
    sharpe_bonus = max(0, sharpe - 1.0) * 10  # Bonus if Sharpe > 1.0
    drawdown_penalty = drawdown * 5
    return base_reward + sharpe_bonus - drawdown_penalty
```

### For Portfolio Trading (like Portfolio Manager Pro)
```python
# Recommended PPO settings for portfolio
PPO_CONFIG = {
    'learning_rate': 1e-4,
    'n_steps': 2048,            # Longer steps for stable portfolio
    'batch_size': 64,
    'n_epochs': 10,
    'gamma': 0.99,              # Long-term rewards matter more
    'gae_lambda': 0.95,
    'ent_coef': 0.005,          # Less exploration (stability)
    'max_grad_norm': 0.5,
}
```

---

## Hyperparameter Tuning Guide

### Network Architecture
```
Small (simple trading):
  Dense(64) → Dense(64) → Output

Medium (portfolio):
  Dense(128) → Dense(128) → Dense(64) → Output

Large (complex patterns):
  Dense(256) → Dense(256) → Dense(128) → Dense(64) → Output
```

### Learning Rates (by problem)
- **Convergence too slow**: 3e-4 (higher)
- **Convergence too fast**: 1e-5 (lower)
- **Unstable updates**: 1e-4 (sweet spot)

### Exploration (Entropy)
- **Too exploitative**: ent_coef = 0.02
- **Too explorative**: ent_coef = 0.001
- **Sweet spot**: ent_coef = 0.01

---

## Monitoring During Training

### Track These Metrics:
```python
# Every 5000 steps
- Mean Reward
- Sharpe Ratio
- Win Rate
- Max Drawdown
- Policy Loss
- Value Function Loss
```

### Early Stopping:
```python
# Stop if Sharpe >= 1.0 for 10 consecutive evals
if sharpe_ratio >= 1.0 and epochs_at_target >= 10:
    break
```

---

## FAQ

**Q: How many training steps do I need?**
A: 50k-100k for simple strategies, 200k-500k for complex ones.

**Q: Should I use PPO or DQN?**
A: Use PPO for continuous actions (forex), DQN for discrete (buy/sell/hold).

**Q: Can I train on live data?**
A: Not recommended. Use historical data for initial training, then fine-tune on recent data.

**Q: How often should I retrain?**
A: Monthly for changing market conditions. More frequently if performance drops.

---

## Integration

Use with **Code Reviewer** to ensure safe implementation:
```
"Zoptymalizuj reward function dla Sharpe 1.0, a potem przejrzyj kod"
```

---

## Support

- GitHub: github.com/wasiek91/agentEA/issues
- CLAUDE.md: Full project documentation
