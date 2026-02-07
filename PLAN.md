PLAN.md

Goal
- Add pyramiding without touching code yet. Only document a clear design.
- Keep client-configurable inputs in `FVG_strategy.py`.
- Allow an alternate pyramiding mode for you in the Binance runner without code duplication or overriding existing strategy methods.

Constraints and current structure (observed)
- `FVG_Strategy` implements core logic: entry, zones, stops, checks.
- Binance/backtest subclasses mostly provide API-specific plumbing.
- `entry_logic()` currently blocks if `len(self.active_orders) > 0`.
- `fvg_zones` are marked `mitigated` when a trade is opened (single-entry today).
- Orders are stored in `active_orders`, and closing uses only `active_orders[0]` in several places.

Desired behaviors
Client pyramiding (single composite position):
- Treat pyramiding as one evolving position, not multiple independent orders.
- If a position is open and price moves in profit by X ATR, add size to the same position.
- X ATR uses the ATR value at entry; client wants "distance equivalent to TP_MULTIPLIER = 1".
- Stop/TP/trailing updates continue to operate on a single position object.
- Inputs needed:
  - allow pyramiding (bool)
  - atr step size for add-ons (float, in ATR units; default 1.0 to match TP_MULTIPLIER=1)
  - add-on size (separate from base; can be fixed or % of base)
  - optional: max add-ons (safety)
  - optional: direction (only add in same direction as open order)

Your pyramiding (simple max concurrent orders):
- Single input: max simultaneous orders.
- No "already opened" check; entries can occur while a position exists.
- Still mark FVG zones mitigated once used.

Design principles (no code yet)
- Avoid duplicating or overriding `entry_logic()` in subclasses.
- Keep only the client’s configurable constants in `FVG_strategy.py`.
- Add extension hooks that a subclass can provide without copying logic.
- Add a small, composable "pyramiding policy" object that the strategy can call.

Proposed architecture
1) Add a pyramiding policy interface (non-API, pure logic)
   - Create a small class or protocol with:
     - `should_allow_entry(strategy, zone) -> bool`
     - `should_add_on(strategy, current_price) -> AddOnSpec | None`
     - `on_position_opened(order, strategy) -> None`
     - `on_position_closed(order, strategy) -> None`
   - `AddOnSpec` only needs size (and maybe metadata), since it modifies one position.
   - Keep this in a new helper module (e.g., `helping_functions/pyramiding.py`) or inside `FVG_strategy.py` if you want less files.

2) Core changes to FVG_Strategy (later; not now)
   - Add a `pyramiding` attribute on the Strategy instance.
     - Default: "no pyramiding" policy.
   - Inside `entry_logic()`, replace the existing "one-order" guard:
     - Instead of `if len(active_orders) > 0: return`,
       call `self.pyramiding.should_allow_entry(self, zone)` and use that boolean.
   - After placing an order, call `self.pyramiding.on_position_opened(order, self)`.
   - During `update_price()` or `bar_iteration()`, call
     - `self.pyramiding.should_add_on(self, current_price)` to get a single add-on size
     - apply it to the existing order (increase `order_size`)
   - This keeps entry logic centralized and avoids subclass overrides.

3) Where to keep client-only constants
   - Add in `FVG_strategy.py`:
     - `ALLOW_PYRAMIDING = False`
     - `PYR_ATR_STEP = 1.0`
     - `PYR_ADD_ON_SIZE = 0.001` (or percent config)
     - `PYR_MAX_ADDS = 3` (optional)
   - These are the only pyramiding constants in core strategy.

4) How your alternate behavior fits (without duplicating/overriding)
   - Use a different pyramiding policy object assigned in Binance runner:
     - In `Binance_Strategy.__init__` or `init_api`, set
       `self.pyramiding = MaxOrdersPolicy(max_orders=N)`.
   - `MaxOrdersPolicy.should_allow_entry` returns `len(active_orders) < max_orders`.
   - It does not do add-on logic; it just allows multiple entries.
   - No `entry_logic()` override required.
   - No code duplication: `entry_logic()` still opens orders based on FVG zones and marks them mitigated.

5) Detailed policy behavior
   A) Client pyramiding policy (ATR add-ons, single position logic)
   - Track per-position "next add price" using entry ATR.
     - For long: `next_add = entry_price + (entry_atr * PYR_ATR_STEP * n)`
     - For short: `next_add = entry_price - (entry_atr * PYR_ATR_STEP * n)`
   - Each time price crosses next_add, treat it as adding to the same position:
     - Logically, we increase the position size on the original order object.
     - Operationally, the broker will place a new order in the same direction.
   - Use the same direction as the original order.
   - Maintain a counter of adds per position.
   - Do not add if:
     - `ALLOW_PYRAMIDING` is False
     - `max adds` reached
     - price is not in profit relative to entry
   - Stops/TP/trailing remain attached to this single position.
   - Later, partial reductions can reduce the same `order_size` without spawning new orders.

   B) Max orders policy (your mode)
   - No add-on logic.
   - `should_allow_entry`: returns True if `len(active_orders) < MAX_OPEN_ORDERS`.
   - No special tracking.
   - Can coexist with zone mitigation: once a zone triggers, it is still marked mitigated, so multiple entries require multiple zones.

6) Order management impact (important)
   - For client pyramiding as a single position, the current logic (using only
     `active_orders[0]`) still works because there is only one position object.
   - For your multi-order mode, updates must still iterate all active orders.

7) Data needed for ATR add-on triggers
   - Store entry ATR in the position (already present as `entry_atr` in `FVG_Order`).
   - Track add count (`pyramid_count`) and next trigger price on the same order object.

8) Backtest considerations
   - For client mode, position size changes should be logged as add-on events.
   - Equity updates should reflect increased size when the position closes.
   - Intracandle vs close-only entry should not affect add-on logic unless explicitly required.

9) Step-by-step implementation plan (future, not now)
   - Add policy interface and a default NoPyramiding policy.
   - Insert policy calls in `entry_logic()` and bar/price updates.
   - Add `ClientAtrPyramidingPolicy` using new constants in `FVG_strategy.py`.
     - Implementation modifies existing order size instead of creating new orders.
   - Add `MaxOrdersPolicy` and set it in Binance strategy (user preference).
   - Update order management only for your multi-order mode.
   - Add tests or logs to validate add-on triggers and size changes.

Notes
- The `subscribe()` method on the websocket client is internal; you normally call `kline()`/`continuous_kline()` to subscribe. Not part of pyramiding, but noted here.

