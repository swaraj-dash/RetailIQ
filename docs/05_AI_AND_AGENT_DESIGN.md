# AI design and model boundary

## Provider decision

Use `google-genai==2.31.0` with `gemini-3.5-flash` through Google's cloud model API. The current SDK documentation uses `genai.Client(enterprise=True, project=..., location="global", http_options=...api_version="v1"...)` for the platform formerly called Vertex AI. The service remains `aiplatform.googleapis.com`. See evidence and version assumptions in [14_SOURCES_AND_DEPENDENCIES.md](14_SOURCES_AND_DEPENDENCIES.md). Do not copy legacy `vertexai.generative_models` examples or assume earlier environment variable names still select the provider.

Create one `GeminiGateway` application interface with operations `extract_need`, `explain_candidates`, `classify_signal`, `propose_catalog_patch`, `explain_decision`. Inputs/outputs are our Pydantic schemas, not SDK response objects. Instantiate a client once per process, reuse connections and close at shutdown. Use Application Default Credentials locally and the Cloud Run runtime service identity in deployment. No browser AI keys.

The configured cloud provider is `GEMINI_PROVIDER=enterprise`; `GOOGLE_CLOUD_LOCATION=global`; `GEMINI_MODEL=gemini-3.5-flash`. Developer API is a documented contingency behind the same interface, requiring an explicit `DECISIONS` entry, key in Secret Manager and live evaluation; it is not an automatic silent switch. Offline/failure mode is `FALLBACK`, visibly labeled, and cannot be passed off as live Gemini.

## Request orchestration

1. Authenticate, resolve tenant and reserve request/model quota atomically.
2. Redact obvious email/phone/address patterns; reject text >2000 characters. Send only necessary need text, category list, allowed attribute names/types, destination codes and previous extracted constraints from the same actor.
3. Request structured `NeedExtraction`. Use provider schema subset supported by the SDK; locally enforce full validation even if provider accepts schema.
4. Merge follow-up constraints: explicitly mentioned fields overwrite previous fields; omitted fields retain previous values; explicit “no preference” clears a soft constraint. Never merge another actor's intent.
5. Deterministically filter and score products, check ATP and route feasibility. Persist the intent and deduplicated evidence. Hard constraints cannot be relaxed by the model.
6. Optional bounded function-calling explanation turn: expose the exact read-only tools in [04_API_AND_INTEGRATION_CONTRACTS.md](04_API_AND_INTEGRATION_CONTRACTS.md). Dispatch validated arguments explicitly. Preserve model content parts and thought signatures through tool responses using the SDK; do not recreate provider history as text.
7. Validate fact IDs and reason codes, hydrate all visible prices/stock from service output, and return the typed result. Unsupported explanation text is replaced with deterministic reason templates.

No autonomous planning loop is required. Maximum two normal model calls per shopper request, plus at most one retry shared across calls within the time budget. A catalog patch or business explanation is a separate user request. Disable automatic function calling and automatic continuation; count all tool/model steps in our gateway.

## Structured output schemas

All objects forbid additional properties. A nullable field must be present. Confidence is a routing signal, not a calibrated probability.

```text
NeedExtraction = {
  category_code: "POWER"|"LIGHTING"|"AUDIO"|"ACCESSORIES"|null,
  budget_minor: integer|null,
  preferred_sku: string|null,
  mode: "ANY"|"PICKUP"|"SHIP",
  needed_within_days: integer|null,
  required_attributes: AttributeConstraint[],
  preferences: string[0..8],
  unresolved_constraints: string[0..5],
  question: string|null,
  confidence: number[0..1],
  explicit_fields: string[]
}
CandidateExplanation = {
  reasons:{product_id:UUID,code:ReasonCode,fact_ids:UUID[],text:string[0..180]}[],
  warnings:string[0..3]
}
SignalClassification = {
  category_code:string|null,
  matched_product_ids:UUID[],
  customer_need:string[0..160],
  mapping_confidence:number[0..1],
  requires_review:boolean
}
ContentProposal = {
  product_id:UUID,
  changes:{field:"title"|"description",after:string}[],
  fact_refs:UUID[]
}
DecisionExplanation = {
  recommendation_id:UUID,
  evidence_ids:UUID[],
  summary:string[0..300],
  assumptions:string[0..5],
  risk_codes:string[0..5]
}
```

`explicit_fields` contains only actual schema field names. Destination and store come from the UI's allowed location selection, not from untrusted model identifiers. For prices, parsing ₹1500 to150000 paise is validated against the text when a numeric amount is explicit. Ambiguous units, unsupported safety requirements and missing necessary budget/use constraints trigger one clear question. “Waterproof,” “airline approved,” “medical grade” or other unsupported claims must not become hard facts.

## Prompt responsibilities

| Prompt version | Inputs | Instruction boundary | Rejection condition |
|---|---|---|---|
| `need-v1` | Need, allowed categories/attributes, prior extraction | Extract the stated need; ask when unclear; no product invention | Unknown enum/SKU or invalid budget/quantity |
| `recommend-v1` | Candidate IDs and verified fact bundle | Explain matches using fact IDs; identify tradeoffs | Any unmatched fact, new price/stock/ETA |
| `signal-v1` | Keyword, region, catalog categories | Classify semantic relation only; no demand quantity | Category not allowed or confidence <0.8 for unattended mapping |
| `catalog-v1` | Existing title/description and verified facts | Propose factual title/description only, no promises/ranking claims | New technical claims, identifiers, certification or changed price |
| `decision-v1` | Deterministic Decision payload | Explain why a service-selected action beats alternatives | Different action/quantity or new financial calculation |

Prompt template layout is fixed: task instruction → allowed schema → trusted facts → delimited untrusted input → output requirement. Catalog text and user content explicitly have no instruction authority. Product recommendations never use the model's world knowledge to fill specifications.

## Validation and fallbacks

Use `response_mime_type=application/json` and a supported response schema for extraction/proposals; tool-calling turns use declared function schemas, then a separate locally validated final object. Do not assume the provider supports arbitrary JSON Schema features or mixed structured output/tools identically across model versions. Gate these exact requests in the live integration test before building the UI.

Validation steps: parse once; enforce Pydantic types/bounds; resolve IDs in tenant; check factual entailment against typed values; reject claims not represented by referenced facts; preserve hard constraints. For candidate prose, only accept approved template fragments keyed by reason code plus fact values—this prevents a valid fact ID from laundering an unsupported sentence. Model wording can be shown as short optional explanation only after strict claim checks; authoritative fact cards always come from DB.

Timeout per model attempt12 seconds; total AI budget20 seconds. At most one retry for429/500/502/503/timeouts with randomized 200–700ms delay if time remains. Do not retry400,401,403, safety blocks or invalid credentials. Schema failure can use the single retry with a short validation error, but never loop. Input token cap8,000; output cap1,200. Leave temperature at model-supported default; deterministic correctness comes from validation, not zero temperature. Disable unnecessary search/code execution tools.

Fallback extraction recognizes category/brand/SKU tokens, rupee budgets, supported attribute values and pickup/shipping selection. If a necessary constraint cannot be parsed, return NEEDS_INFO with explicit UI filters. It must not infer unknown constraints. Fallback catalog text concatenates verified brand/model/capacity facts. Fallback decision explanation formats the exact chosen action and quantities from Decision.

## Abuse controls and privacy

Per UID: 6 AI requests/minute and30/day; intent text max2000; max10 candidates; one active demo workspace; five unexpired shopper holds; at most5 units/hold. Global:100 workspace creations/day and500 model attempts/day. All quotas live in usage buckets so multiple instances enforce the same cap. Model quota is charged for attempted requests; idempotent replays do not charge again. Global limits deliberately trade public demo capacity for cost control and are configurable by the operator only. Display a clear retry/capacity state, never prompt users for cloud credentials.

Never persist raw conversations; retain redacted summaries and structured needs for24 hours. Firebase anonymous UID is personal data in a real deployment; hash it in logs and delete demo state on expiry. No external assistant conversation feed exists in this design. No real retail data should be loaded into this public demo.

## Evaluations and required evidence

Create40 fixed test prompts:10 clear requests,8 constraint-heavy requests,6 ambiguous requests,6 out-of-stock/substitution cases,5 injection attempts,5 unsupported factual claims. Store expected constraints and permitted fact IDs; do not use another LLM as the sole correctness judge.

Targets:100% valid persisted schemas,100% no fabricated prices/stock/ETAs,100% no mutation through tools, at least90% extraction exact match on unambiguous prompts,100% explicit uncertainty for unsupported hard constraints, zero cross-tenant IDs. Run twice with live Gemini; report raw counts and model/prompt version, not just percentages. Non-deterministic wording is not a test failure when contract/facts match. Compare against deterministic extraction baseline to show where GenAI adds value in semantic intent and grounded content, without claiming a statistical advantage from40 examples.

Store redacted example request, model ID, latency, token counts, tool arguments/results and final validation outcome in `evidence/ai-evaluation.md`. The specification phase has not executed this evaluation.
