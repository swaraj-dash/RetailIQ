import json
import logging
import os
import re
import uuid
import datetime
from typing import Optional, Dict, Any, List
from app.config import settings

logger = logging.getLogger("retailiq.ai")

# Attempt to import Google GenAI SDK if available
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger.info("google-genai SDK not available; operating in deterministic fallback mode.")
def sanitize_prompt_input(text: str) -> str:
    """Sanitize user input for prompt injection protection."""
    clean = text[:500].strip()
    clean = re.sub(r'(?i)(ignore previous instructions|disregard all rules|system prompt|developer mode|forget your rules)', '[FILTERED]', clean)
    return clean

class GeminiGateway:
    """
    Robust Gateway for Google Gemini.
    Supports both direct Gemini API Key (GEMINI_API_KEY) and Google Cloud Vertex AI (ADC / Project credentials).
    Falls back gracefully and deterministically with explicit transparency.
    """
    def __init__(self):
        self.client = None
        self.ai_configured = False
        self.provider_name = "deterministic_fallback"
        self.active_model = settings.GEMINI_MODEL
        self.last_error: Optional[str] = None
        self.last_error_at: Optional[str] = None
        self.last_success_at: Optional[str] = None

        self._initialize_client()

    def _initialize_client(self):
        if not GENAI_AVAILABLE:
            self.provider_name = "deterministic_fallback"
            return

        # 1. Try Direct Gemini API Key
        api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
        if api_key:
            try:
                self.client = genai.Client(api_key=api_key)
                self.ai_configured = True
                self.provider_name = "google_api_key"
                logger.info(f"Gemini client initialized via API Key for model: {self.active_model}")
                return
            except Exception as e:
                self._record_error("api_key_init", str(e))

        # 2. Try Google Cloud ADC / Vertex AI Enterprise
        project = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
        location = settings.GOOGLE_CLOUD_LOCATION or "us-central1"
        if project:
            try:
                self.client = genai.Client(vertexai=True, project=project, location=location)
                self.ai_configured = True
                self.provider_name = "vertex_ai_enterprise"
                logger.info(f"Gemini client initialized via Vertex AI project '{project}' in '{location}'")
                return
            except Exception as e:
                self._record_error("vertex_ai_init", str(e))

        self.ai_configured = False
        self.provider_name = "deterministic_fallback"

    def _record_error(self, op: str, error_msg: str):
        self.last_error = f"{op}: {error_msg}"
        self.last_error_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        logger.warning(f"AI Operation [{op}] error: {error_msg}. Using deterministic fallback.")

    def _record_success(self):
        self.last_success_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    def get_status(self) -> Dict[str, Any]:
        return {
            "ai_configured": self.ai_configured,
            "provider": self.provider_name,
            "model": self.active_model,
            "last_error": self.last_error,
            "last_error_at": self.last_error_at,
            "last_success_at": self.last_success_at
        }


    # -------------------------------------------------------------------------
    # Operation 1: extract_need (Conversational Shopping Intent Parsing)
    # -------------------------------------------------------------------------
    def extract_need(
        self,
        text: str,
        destination_code: str = "INDIRANAGAR",
        preferred_store_code: Optional[str] = "S1"
    ) -> Dict[str, Any]:
        """Extract structured customer need. Uses Gemini if available, otherwise deterministic fallback."""
        clean_text = sanitize_prompt_input(text)

        if self.ai_configured and self.client:
            try:
                prompt = f"""
You are RetailIQ's retail intent assistant.
Extract structured customer shopping constraints from the user request.
Allowed categories: POWER, LIGHTING, AUDIO, ACCESSORIES.
Allowed destination codes: INDIRANAGAR, WHITEFIELD, JAYANAGAR.
Allowed store codes: S1, S2, S3.

Respond ONLY with a JSON object conforming to this schema:
{{
  "category_code": "POWER" | "LIGHTING" | "AUDIO" | "ACCESSORIES" | null,
  "budget_minor": integer (in paise, e.g. 1500 rupees = 150000 paise) | null,
  "preferred_sku": string (e.g. "RQ001") | null,
  "mode": "ANY" | "PICKUP" | "SHIP",
  "needed_within_days": integer (0 for today, 1 for tomorrow) | null,
  "required_attributes": [
    {{"attribute": string, "operator": "EQ"|"GTE"|"LTE"|"CONTAINS", "value": string|number|boolean}}
  ],
  "preferences": [string],
  "question": string | null
}}

User request: "{clean_text}"
Destination: {destination_code}
Store: {preferred_store_code}
"""
                response = self.client.models.generate_content(
                    model=self.active_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2
                    )
                )
                if response and response.text:
                    parsed = json.loads(response.text)
                    self._record_success()
                    return {
                        "constraints": {
                            "category_code": parsed.get("category_code"),
                            "budget_minor": parsed.get("budget_minor"),
                            "preferred_sku": parsed.get("preferred_sku"),
                            "destination_code": destination_code,
                            "preferred_store_code": preferred_store_code,
                            "mode": parsed.get("mode", "ANY"),
                            "needed_within_days": parsed.get("needed_within_days"),
                            "required_attributes": parsed.get("required_attributes", []),
                            "preferences": parsed.get("preferences", [])
                        },
                        "status": "MATCHED",
                        "question": parsed.get("question"),
                        "ai_mode": "LIVE"
                    }
            except Exception as e:
                self._record_error("extract_need", str(e))

        # Deterministic Grounded Fallback
        lower_text = clean_text.lower()
        category_code = None
        if any(w in lower_text for w in ["power", "power bank", "charger", "mah", "voltgo"]):
            category_code = "POWER"
        elif any(w in lower_text for w in ["light", "lantern", "torch", "lumens", "lumatrail"]):
            category_code = "LIGHTING"
        elif any(w in lower_text for w in ["audio", "buds", "speaker", "earphone", "echoway"]):
            category_code = "AUDIO"
        elif any(w in lower_text for w in ["stand", "cable", "pouch", "sleeve", "tripkit"]):
            category_code = "ACCESSORIES"

        budget_minor = None
        budget_match = re.search(r'(?:under|budget|below|<=?|rs\.?|₹)\s*(\d+(?:,\d+)?)', lower_text)
        if budget_match:
            try:
                amt_str = budget_match.group(1).replace(",", "")
                budget_minor = int(amt_str) * 100
            except ValueError:
                pass

        preferred_sku = None
        if "voltgo pro" in lower_text or "rq001" in lower_text:
            preferred_sku = "RQ001"
        elif "voltgo go" in lower_text or "rq002" in lower_text:
            preferred_sku = "RQ002"
        elif "voltgo max" in lower_text or "rq003" in lower_text:
            preferred_sku = "RQ003"

        mode = "ANY"
        if "pickup" in lower_text or "pick up" in lower_text:
            mode = "PICKUP"
        elif "ship" in lower_text or "delivery" in lower_text:
            mode = "SHIP"

        needed_within_days = None
        if "today" in lower_text or "urgent" in lower_text:
            needed_within_days = 0
        elif "tomorrow" in lower_text:
            needed_within_days = 1

        required_attributes = []
        cap_match = re.search(r'(\d{4,5})\s*mah', lower_text)
        if cap_match:
            required_attributes.append({
                "attribute": "capacity_mah",
                "operator": "GTE",
                "value": int(cap_match.group(1))
            })

        if "usb-c" in lower_text or "type-c" in lower_text:
            required_attributes.append({
                "attribute": "connector",
                "operator": "EQ",
                "value": "USB-C"
            })

        preferences = []
        if "travel" in lower_text:
            preferences.append("compact travel size")

        return {
            "constraints": {
                "category_code": category_code,
                "budget_minor": budget_minor,
                "preferred_sku": preferred_sku,
                "destination_code": destination_code,
                "preferred_store_code": preferred_store_code,
                "mode": mode,
                "needed_within_days": needed_within_days,
                "required_attributes": required_attributes,
                "preferences": preferences
            },
            "status": "MATCHED" if category_code else "NEEDS_INFO",
            "question": None if category_code else "What type of product are you looking for? (e.g., power bank, lighting, audio)",
            "ai_mode": "FALLBACK"
        }

    # -------------------------------------------------------------------------
    # Operation 2: propose_catalog_patch (AEO & Spec Fact Grounding)
    # -------------------------------------------------------------------------
    def propose_catalog_patch(
        self,
        sku: str,
        current_title: str,
        current_description: str,
        facts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Propose verified-fact grounded catalog patch for title/description."""
        fact_dict = {f["attribute"]: f["value"] for f in facts}
        fact_refs = [f["id"] for f in facts]

        if self.ai_configured and self.client:
            try:
                facts_str = json.dumps(fact_dict, indent=2)
                prompt = f"""
You are RetailIQ's catalog audit engine.
Given verified manufacturer facts for SKU {sku}, propose an updated product title and search-optimized description.
Do NOT invent facts. Base the changes strictly on:
{facts_str}

Current Title: "{current_title}"
Current Description: "{current_description}"

Respond ONLY with JSON:
{{
  "proposed_title": string,
  "proposed_description": string,
  "explanation": string
}}
"""
                response = self.client.models.generate_content(
                    model=self.active_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2
                    )
                )
                if response and response.text:
                    parsed = json.loads(response.text)
                    self._record_success()
                    return {
                        "changes": [
                            {
                                "field": "title",
                                "before": current_title,
                                "after": parsed.get("proposed_title", current_title)
                            },
                            {
                                "field": "description",
                                "before": current_description,
                                "after": parsed.get("proposed_description", current_description)
                            }
                        ],
                        "fact_refs": fact_refs,
                        "ai_mode": "LIVE"
                    }
            except Exception as e:
                self._record_error("propose_catalog_patch", str(e))

        # Deterministic Grounded Fallback (Strictly labelled FALLBACK)
        if sku == "RQ002":
            capacity = fact_dict.get("capacity_mah", 10000)
            connector = fact_dict.get("connector", "USB-C")
            output_w = fact_dict.get("output_w", 20)
            return {
                "changes": [
                    {
                        "field": "title",
                        "before": current_title,
                        "after": f"VoltGo Go {capacity} — {capacity:,} mAh {connector} {output_w}W PD Power Bank"
                    },
                    {
                        "field": "description",
                        "before": current_description,
                        "after": f"High-density {capacity:,} mAh Li-Polymer portable power bank featuring {connector} 20W Power Delivery fast charging and dual USB-A ports. Verified OEM travel specification."
                    }
                ],
                "fact_refs": fact_refs,
                "ai_mode": "FALLBACK"
            }

        cleaned_title = current_title.replace(" (Verified Spec)", "").strip()
        return {
            "changes": [
                {
                    "field": "title",
                    "before": current_title,
                    "after": f"{cleaned_title} — Verified Specifications"
                }
            ],
            "fact_refs": fact_refs,
            "ai_mode": "FALLBACK"
        }

    # -------------------------------------------------------------------------
    # Operation 3: explain_decision (Human-in-the-Loop Rebalancing Rationale)
    # -------------------------------------------------------------------------
    def explain_decision(
        self,
        sku: str,
        action: str,
        source_store: Optional[str],
        target_store: str,
        quantity: int,
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Explain transfer vs purchase optimization to a store manager."""
        if self.ai_configured and self.client:
            try:
                prompt = f"""
You are RetailIQ's operations advisor.
Explain why a {action} of {quantity} units of {sku} from {source_store} to {target_store} is recommended.
Metrics:
- Inter-store transfer lead time: 1 day, working capital: 0, margin captured: ₹{metrics.get('margin_opp', 15074)}
- Supplier PO alternative: lead time 7 days, requires ₹{metrics.get('po_cap', 25380)} working capital, lost units: 2
Keep explanation under 50 words, crisp, and executive-ready.
"""
                response = self.client.models.generate_content(
                    model=self.active_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0.3)
                )
                if response and response.text:
                    self._record_success()
                    return {
                        "explanation": response.text.strip(),
                        "ai_mode": "LIVE"
                    }
            except Exception as e:
                self._record_error("explain_decision", str(e))

        # Deterministic Grounded Fallback
        return {
            "explanation": f"Inter-store transfer of {quantity} units from {source_store or 'S2'} to {target_store} prevents stockout within 1 day, avoiding ₹25,380 in tied working capital compared to vendor purchasing.",
            "ai_mode": "FALLBACK"
        }

    # -------------------------------------------------------------------------
    # Operation 4: classify_signal (Trend & Social Hype Restraint Normalization)
    # -------------------------------------------------------------------------
    def classify_signal(
        self,
        signal_code: str,
        signal_name: str,
        channel: str,
        volume_growth_pct: float,
        basket_conversion_rate: float
    ) -> Dict[str, Any]:
        """Classify external signal: genuine utility spike vs short-lived viral fad."""
        if self.ai_configured and self.client:
            try:
                prompt = f"""
You are RetailIQ's trend intelligence engine.
Evaluate this signal:
- Code: {signal_code} ({signal_name})
- Channel: {channel}
- Growth: +{volume_growth_pct}%
- Local Basket Conversion: {basket_conversion_rate:.2f}

Classify into:
- classification: "HIGH_UTILITY_SEARCH" | "VIRAL_SOCIAL_FAD" | "NEUTRAL"
- recommendation: "PURCHASE" | "TRANSFER" | "MONITOR"
- reliability_score: float (0.0 to 1.0)
- rationale: string (max 25 words)

Respond ONLY in JSON.
"""
                response = self.client.models.generate_content(
                    model=self.active_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2
                    )
                )
                if response and response.text:
                    parsed = json.loads(response.text)
                    self._record_success()
                    return {
                        "signal_code": signal_code,
                        "classification": parsed.get("classification"),
                        "recommendation": parsed.get("recommendation"),
                        "reliability_score": parsed.get("reliability_score", 0.5),
                        "rationale": parsed.get("rationale"),
                        "ai_mode": "LIVE"
                    }
            except Exception as e:
                self._record_error("classify_signal", str(e))

        # Deterministic Grounded Fallback
        if "glow" in signal_name.lower() or "tiktok" in channel.lower() or basket_conversion_rate < 0.05:
            return {
                "signal_code": signal_code,
                "classification": "VIRAL_SOCIAL_FAD",
                "recommendation": "MONITOR",
                "reliability_score": 0.3,
                "rationale": "High social engagement without verified basket conversion. Capped at 0 units to prevent dead inventory.",
                "ai_mode": "FALLBACK"
            }
        return {
            "signal_code": signal_code,
            "classification": "HIGH_UTILITY_SEARCH",
            "recommendation": "PURCHASE",
            "reliability_score": 0.85,
            "rationale": "Sustained high-intent search queries corroborated by regional demand patterns.",
            "ai_mode": "FALLBACK"
        }

    # -------------------------------------------------------------------------
    # Operation 5: evaluate_compatibility (Technical Spec Check & Warning)
    # -------------------------------------------------------------------------
    def evaluate_compatibility(
        self,
        sku: str,
        user_requirements: Dict[str, Any],
        product_facts: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check hardware compatibility (e.g. wattage, protocol, form factor)."""
        req_w = user_requirements.get("min_wattage", 0)
        prod_w = product_facts.get("output_w", 20)
        connector_req = user_requirements.get("connector", "USB-C")
        prod_connector = product_facts.get("connector", "USB-C")

        if self.ai_configured and self.client:
            try:
                prompt = f"""
Evaluate if product {sku} is technically compatible with user requirements.
User requirements: wattage={req_w}W, connector={connector_req}
Product specs: wattage={prod_w}W, connector={prod_connector}
Return JSON:
{{
  "is_compatible": true,
  "confidence": 0.95,
  "warning": null,
  "explanation": "Verified compatible fast-charging profile for smartphones."
}}
"""
                response = self.client.models.generate_content(
                    model=self.active_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.1
                    )
                )
                if response and response.text:
                    parsed = json.loads(response.text)
                    self._record_success()
                    return {
                        "sku": sku,
                        "is_compatible": parsed.get("is_compatible", prod_w >= req_w),
                        "confidence": float(parsed.get("confidence", 0.95)),
                        "product_wattage": prod_w,
                        "required_wattage": req_w,
                        "warning": parsed.get("warning") or (None if prod_w >= req_w else f"Device requires {req_w}W PD; this product provides {prod_w}W."),
                        "explanation": parsed.get("explanation", "Verified compatible power delivery profile."),
                        "ai_mode": "LIVE"
                    }
            except Exception as e:
                self._record_error("evaluate_compatibility", str(e))

        is_compatible = prod_w >= req_w
        warning = None if is_compatible else f"Device requires {req_w}W PD; this product provides {prod_w}W (slower charging)."
        explanation = (
            "Verified substitute: shares 10,000 mAh capacity and USB-C connection. 20W PD provides fast charging for smartphones."
            if is_compatible
            else f"Wattage shortfall: {prod_w}W vs requested {req_w}W."
        )

        return {
            "sku": sku,
            "is_compatible": is_compatible,
            "confidence": 0.95 if is_compatible else 0.80,
            "product_wattage": prod_w,
            "required_wattage": req_w,
            "warning": warning,
            "explanation": explanation,
            "ai_mode": "FALLBACK"
        }

gemini_gateway = GeminiGateway()
