# UI/UX design system and screen contract

## Product direction

One coherent RetailIQ app with Shopper, Associate and Business workspaces. Default landing is a useful shopping prompt with a visible “Explore business demo” switch. The differentiator is a persistent “How this decision was made” panel tying facts, availability and outcomes together. Avoid a wall of AI prose or a dashboard of unexplained numbers.

Use a white/light background, navy text, blue primary action, restrained cyan highlights, orange for review and green for completed states. Product imagery is original local demo illustration. Do not imitate a corporate logo or imply Broadridge affiliation.

## Tokens and components

| Token | Value/use |
|---|---|
| background / surface | `#F5F8FC` / `#FFFFFF` |
| primary text / secondary | `#001F5A` / `#475569` |
| primary / hover | `#2662EC` / `#164BDB` |
| cyan / cyan surface | `#08C2FF` / `#EAF9FF`; cyan never small text on white |
| border | `#DCE4F0` |
| success / success surface | `#166534` / `#ECFDF3` |
| review / review surface | `#9A3412` / `#FFF7ED` |
| error / error surface | `#B91C1C` / `#FEF2F2` |
| typography | System sans stack; body16px/1.5; small14px; page title28px/1.2; KPI32px; tabular numerals for quantities |
| spacing | 4,8,12,16,24,32,48px scale |
| radii / shadow | cards12px, inputs8px; shadow `0 2px 10px rgba(0,31,90,.06)` |
| layout | max width1440px; sidebar224px; content gaps24px; form width≤680px |

Use shadcn components backed by one consistent Radix system: Button, Dialog, AlertDialog, Sheet, Tabs, Select, Input, Label, Table, Tooltip, Alert, Skeleton. Copy reviewed component source into `frontend/src/components/ui`; do not layer MUI/Ant Design on top. Lucide icons accompany text. Recharts charts always have accessible tables with identical values. Error messages use human words and optional request ID, never raw SDK errors.

## Navigation and endpoint map

| Route | Screen | APIs |
|---|---|---|
| `/` and `/shop` | Needs, product matches and comparisons | API03,05–10,25 |
| `/shop/product/:id` | Product facts and network availability | API07,08,11 |
| `/shop/cart` | Single-line selected quote, hold and confirmation | API11–14,40 |
| `/shop/orders` | Orders and simulated receipt | API15–17,22,24 |
| `/associate` | Network search, stock by location, order queue | API05–08,15–24 |
| `/business` | Priority dashboard | API26,28,31 |
| `/business/forecast` | SKU/store forecast and baseline | API05–07,27 |
| `/business/decisions/:id` | Alternatives, evidence and approval | API29,30 |
| `/business/trends` | Signal-to-stock pipeline | API32,28 |
| `/business/catalog` | Audit, patch review and structured preview | API33–37 |
| `/business/outcomes` | Estimated versus observed, trace | API38,39 |

Global top bar: RetailIQ, workspace switch, store selector, “Synthetic demo” badge, scenario date, status dot. Persistent small banner states “Orders and business actions are simulated.” This is essential user context, not an infrastructure explanation. Do not show SDK names, schema versions or Cloud Run implementation details in normal shopper flows.

## Screen layouts

### Shopper discovery

Desktop: left30% needs panel, right70% matches. Heading “Find what fits—and what is available.” Input has three example prompts, location selector and submit. After extraction, show editable category, budget, brand, pickup/shipping, deadline and hard attributes. Ask one targeted question if NEEDS_INFO. Preserve user input on failures.

Product cards: image, factual title, price,2–3 supported match reasons, local availability badge, “Compare” and “View options.” When preferred item unavailable show its card with “Unavailable across this demo network” and substitutes beneath; do not remove it. Match reasons link to fact drawer. Comparison table has exactly2–3 products and explicit “Unknown” cells; no fake winner badge.

Stock labels distinguish “Available now,” “Reserved,” and “Incoming.” Exact quantity shown in product detail; listing can show visible near the quote action. No green availability badge for unreceived PO or proposed transfer. “Available as of…” timestamp is visible near the quote action.

### Product and fulfillment

Top factual product summary; middle network stock table; right option card with pickup/ship choice, store, estimated readiness, item total and fee. Shopper sees delivery as “Simulated estimate: 2 days.” If no route meets deadline, explain which constraint fails and offer editable deadline or another product; never promise the same item anyway.

### Cart and order

MVP cart contains one SKU, quantity1–5. Adding another SKU asks to replace the existing line. Display quantity, item price, fee,total, hold expiry, selected origin, and editable deadline if allowed. “Reserve for15 minutes” creates the hold; “Place demo order” converts it. Timer uses server expiry minus clock offset, while backend remains authoritative. Buttons disable during submission; retries reuse idempotency key. Successful order shows order code and trace link. Expired hold state clears confirmation controls and offers a new quote.

### Associate workspace

Search at top; store chips and network table columns: location,on hand,blocked,existing reservations,ATP,incoming. Expand product row for alternatives and fulfillment. Separate tabs Orders/Transfers/Incoming/Returns. Each transition shows current status and one valid next action only. Receiving a return opens an inspection dialog with Restock/Damaged choices; no direct stock editing form. Show before/after stock values from server after completion.

### Business dashboard

Four KPI cards: stockout SKU/store pairs, excess stock cost, estimated contribution opportunity, pending proposals. Under them a priority decision table with SKU/store, action, quantity, stockout day, estimated benefit, confidence,status. Right rail explains current data freshness and last refresh; “Refresh intelligence” runs API26. Estimated values use a visible “Scenario estimate” label; observed values sit in a separate outcomes section. Never sum alternatives as independent opportunities.

### Forecast screen

SKU/store selectors; horizon7/14/28. Chart has history solid navy, forecast blue, scenario band pale blue, incoming supply markers. Separate toggles display baseline MA28 and selected model without changing the saved run. Beneath: WAPE/MAE, valid holdout count, exclusion reasons and assumptions. Legend explicitly says ranges are uncalibrated scenarios. Category rollups are tables/sums, not a separate model.

### Decision detail and approval

Header “Transfer32 units to Indiranagar” plus expiry/status. Left evidence timeline; center comparison table with No action, Transfer, Purchase and rejected options; right recommended action and review button. Table columns: quantity,arrival,estimated lost units,new capital,logistics,holding,unsold exposure,contribution opportunity. Show model confidence separately from forecast uncertainty.

Approval dialog repeats source,destination,quantity,cost and simulated nature. Requires a deliberate “Approve demo transfer” or “Approve demo order.” No default checked approval and no conversational command that bypasses it. Reject asks optional reason. `409 stale` state disables old approval and links to refresh. After approve, navigate to created action record and show dispatch/receive states; approval itself must not make recipient stock available.

### Trend-to-stock

Three linked panels: source evidence → mapping/normalization → business alternatives. Cards show synthetic badge, period,region,index values,reliability,internal sessions and conversion sample. Expose raw lift and capped forecast uplift. MONITOR cards have no approve button, and explain weak evidence or MOQ. Both actionable lantern and rejected glow-clip scenario appear together, demonstrating restraint.

### Catalog/AEO

Table SKU,audit score,issues,customer impact. Issue drawer lists exact failed rule and verified facts. Patch review is side-by-side current/proposed title/description with changed text highlighted; fact references below. Actions Approve/Reject. Successful approval reruns audit, shows score delta and leaves prices/stock untouched. Structured-data tab shows JSON preview plus validation issues and “Preview only—not published to search or merchant feeds.” No “AI ranking score” or promised visibility uplift.

### Outcomes and trace

Separate cards “Expected in scenario” and “Observed in demo.” Show linked order,proposal and movement IDs, timestamps and observation count. An order fulfillment is a simulated transaction, not proof of a recovered sale. Trace panel renders a compact vertical event list with expandable evidence; no horizontally sprawling graph. For forecasts with no elapsed actual horizon display “Outcome not yet observable,” never substitute expected figures as actuals.

## Responsive and accessibility behavior

Breakpoints: mobile<768px, tablet768–1199, desktop≥1200. Mobile replaces sidebar with header menu and3 primary workspace tabs; discovery stacks input above cards; review drawer becomes full-screen dialog; tables keep key fields visible and expand details rather than compressing12 columns. Only comparison data may scroll horizontally with a visible label; no page-level horizontal overflow at390px.

Minimum44×44px interactive target, text contrast≥4.5:1, large text≥3:1, visible2px focus ring. Keyboard can complete discovery, comparison, hold, review and dialogs. Dialogs trap focus. Escape closes except during a committed transition. Inputs have labels, errors use aria-describedby, async result updates use a polite live region. Status relies on text/icon as well as color. Honor reduced motion. Chart tooltip information exists in an accessible table.

## State matrix and visual acceptance

Loading: card skeletons with reserved height; long AI wait shows “Checking your needs and available products.” Empty: explain absent products/runs/orders and one relevant action. Partial AI failure: retain deterministic results and show “Language assistance unavailable; facts and stock are current.” Network failure: retry with request ID, preserve edits. Conflict: refetch authoritative state, preserve unsaved edits. Success: concise toast plus persistent state update, not toast alone.

Visual acceptance at1440×900,768×1024,390×844: no clipped text/overlap,page overflow or inaccessible approval; numeric columns aligned; consistent type/spacing; all ten scenarios reachable within navigation; no lorem ipsum; no real-business-result language; browser console has no uncaught errors. Capture screenshots only after genuine flows pass and ensure screenshots do not expose tokens/account data.
