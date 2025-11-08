---
description: "Reinforcement Learning expert - algorithms, hyperparameter tuning, model optimization for trading systems"
capabilities: ["PPO tuning", "DQN optimization", "reward shaping", "hyperparameter tuning", "model convergence", "trading strategy optimization"]
tags: ["reinforcement-learning", "model-optimization", "algorithms", "trading-ai"]
---

# RL Expert Skill

Expert in Reinforcement Learning with specialization in practical implementations for trading systems.

## Capabilities

- **Algorithms** - PPO, DQN, A3C, DDPG, SAC expertise
- **Hyperparameter Tuning** - Learning rates, network architecture, batch sizes
- **Reward Shaping** - Design effective reward functions for trading
- **Exploration vs Exploitation** - Balance trade-offs
- **Stability & Convergence** - Diagnose and fix training issues
- **Model Evaluation** - Metrics and performance assessment
- **Environment Design** - Trading environment setup

## When Claude should invoke this skill

Claude should automatically invoke the RL Expert skill when:
- User asks about reinforcement learning optimization
- Model isn't converging
- Need to tune hyperparameters
- Reward function design needed
- Trading strategy performance optimization
- Model stability issues reported
- A/B testing RL approaches

## Core Algorithms

### PPO (Proximal Policy Optimization)
- Best for: Trading strategies (stable, on-policy)
- Key tuning: clip_ratio, learning_rate, entropy_coeff
- Target: Sharpe > 1.0

### DQN (Deep Q-Network)
- Best for: Discrete action spaces
- Key tuning: epsilon decay, experience replay size
- Target: Convergence < 500 steps

### A3C (Asynchronous Advantage Actor-Critic)
- Best for: Parallel training
- Key tuning: learning rate, entropy regularization
- Target: Wall-clock time optimization

### DDPG (Deep Deterministic Policy Gradient)
- Best for: Continuous action spaces
- Key tuning: policy learning rate, target network update
- Target: Smooth gradient updates

### SAC (Soft Actor-Critic)
- Best for: Entropy-regularized objectives
- Key tuning: temperature, critic learning rate
- Target: Exploration-exploitation balance

## Hyperparameter Tuning Guide

### Learning Rate
```
Too high (0.01):    Diverges, loss spikes
Too low (0.00001):  Converges too slowly
Sweet spot:         0.0001 - 0.001
```

### Batch Size
```
Small (8):          Noisy, faster training
Large (256):        Stable, slower training
Optimal for PPO:    32-64
```

### Network Architecture
```
Shallow (1 layer):  Fast, limited capacity
Deep (4+ layers):   Slow, high capacity
Optimal:            2-3 hidden layers
                    128-256 units per layer
```

### Reward Function
```
Pure returns:       Ignores risk (too volatile)
Risk-adjusted:      (returns - risk_penalty)
Optimal for trading: Sharpe ratio or return/drawdown
```

## Troubleshooting Guide

### Problem: Low Sharpe Ratio (< 1.0)
**Quick Fixes**:
1. Increase learning rate (0.0001 → 0.0003)
2. Add layer to network
3. Increase batch size
4. Add risk penalty to reward

### Problem: High Drawdown (> 20%)
**Quick Fixes**:
1. Reduce position size by 50%
2. Increase stop-loss buffer
3. Add portfolio diversification
4. Increase risk penalty in reward

### Problem: Low Win Rate (< 40%)
**Quick Fixes**:
1. Tighten entry signal conditions
2. Increase exit flexibility
3. Add confirmation signals
4. Reduce trade frequency

### Problem: Training Loss Not Decreasing
**Quick Fixes**:
1. Check data quality (missing values?)
2. Reset network weights
3. Reduce learning rate (0.0001 instead of 0.001)
4. Increase training steps/epochs
5. Verify reward is increasing

### Problem: No Convergence
**Quick Fixes**:
1. Verify reward stability
2. Reduce environment complexity
3. Reset model
4. Change optimizer (Adam → SGD)
5. Increase target network update frequency

## Trading-Specific Metrics

```
Sharpe Ratio:       > 1.0 (return per unit risk)
Maximum Drawdown:   < 15% (worst peak-to-trough)
Win Rate:           > 45% (trades with profit)
Profit Factor:      > 2.0 (total wins / total losses)
Trades per Month:   5-20 (optimal for stability)
Return/Month:       1-3% (realistic for live trading)
```

## Output Format

```
## RL Optimization Analysis

**Current Metrics**:
- Sharpe Ratio: [X]
- Max Drawdown: [X%]
- Win Rate: [X%]

**Issues Identified**:
1. [Primary issue]
2. [Secondary issue]

**Recommended Changes** (in order):
1. [Fix 1 - impact: X%]
2. [Fix 2 - impact: X%]
3. [Fix 3 - impact: X%]

**Implementation Steps**:
1. Step 1
2. Step 2
3. Validate on out-of-sample data

**Expected Improvement**:
- Sharpe: [current] → [target]
- Drawdown: [current] → [target]
```

## Context for agentEA Project

For the agentEA trading platform:
- PPO preferred for trading (stability over speed)
- Trading metrics: Sharpe > 1.0, Drawdown < 15%
- Risk control: Daily loss limit 5%, individual position < 2%
- Real-time environment with MT5 API
- Portfolio Manager: Multi-strategy ensemble
- Janosik EA: Single strategy deep optimization
- Remember: Stability and risk control > maximum profit
