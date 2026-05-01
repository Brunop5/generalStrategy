# FVG ProjectX Bot

This README documents `FVG_projectX_bot` and its architecture.  

## Goal

`FVG_projectX_bot` is a Fair Value Gap (FVG) trading system that applies one shared strategy logic across multiple execution environments:

- ProjectX / TopstepX live execution
- Binance Futures live execution
- Tradovate live execution
- Historical backtesting

The design goal is to keep entry/exit logic, risk rules, and trade management consistent while swapping only the broker adapter.

## Strategy Logic

Core strategy behavior is implemented in `FVG_projectX_bot/FVG_strategy.py` and extends generic abstractions from `strategyTemplate.py`:

- FVG detection and zone tracking
- BOS / CHoCH structure checks
- ATR-based stops and profit targets
- Optional trailing stop behavior
- Position sizing controls (fixed size or risk-based)
- Daily guardrails (trade count and PnL limits)
- Pyramiding and partial close workflows
- Session-time guards for entry cutoff and market close handling

## Directory Map (`FVG_projectX_bot`)

- `FVG_projectX_bot/FVG_strategy.py`: Shared strategy engine used by adapters.
- `FVG_projectX_bot/projectX/`: ProjectX-specific API integration and runtime.
- `FVG_projectX_bot/binance/`: Binance Futures REST/WebSocket adapter.
- `FVG_projectX_bot/tradovate/`: Tradovate REST/WebSocket adapter.
- `FVG_projectX_bot/backtest/`: Backtesting engine, optimization, and evaluation scripts.
- `FVG_projectX_bot/helping_functions/`: Indicators, data utilities, pyramiding, and partial-close helpers.
- `FVG_projectX_bot/utils/`: Configuration and settings loading.
- `FVG_projectX_bot/tryouts/`: Experimental strategy variants and prototypes.
- `FVG_projectX_bot/.env`: Local secrets and environment configuration (ignored by git).
- `FVG_projectX_bot/requirements.txt`: Python dependencies for this bot.

## Configuration

Runtime settings come from JSON inputs plus environment variables:

- `FVG_projectX_bot/projectX/inputs.json`
- `FVG_projectX_bot/binance/inputs.json`
- `FVG_projectX_bot/.env`

Credentials should be provided via `.env` variables such as:

- `PROJECTX_USERNAME`
- `PROJECTX_API_KEY`
- `BINANCE_API_KEY`
- `BINANCE_API_SECRET`
- Tradovate variables (`TRADOVATE_USERNAME`, `TRADOVATE_PASSWORD`, etc.)

## Setup

From repository root:

1. Create and activate virtual environment:
   - Linux/macOS: `python3 -m venv .venv && source .venv/bin/activate`
   - Windows: `python -m venv .venv && .venv\Scripts\activate`
2. Install dependencies:
   - `pip install -r FVG_projectX_bot/requirements.txt`
3. Populate `FVG_projectX_bot/.env` with required credentials.

## Run

From repository root:

- ProjectX live: `python -m FVG_projectX_bot.projectX.FVG_projectX`
- Binance live: `python -m FVG_projectX_bot.binance.FVG_binance`
- Tradovate live: `python -m FVG_projectX_bot.tradovate.FVG_tradovate`
- Backtest: `python -m FVG_projectX_bot.backtest.FVG_backtest`

This README file was written by AI.
