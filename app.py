"""EcoSort AI - AI-Powered Waste Intelligence System.

Aligned with UN Sustainable Development Goal 12: Responsible Consumption and Production.
Developed for the 1M1B AI for Sustainability Internship.
Modern Editorial / Neo-Brutalist Architecture with Full Light & Dark Mode Support.
Zero Emoji Dependency • Professional Inline SVG Iconography • Multimodal Vision.
"""

import io
import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel, Field, ValidationError
import streamlit as st

# Load environment variables from .env if present
load_dotenv()

# ==============================================================================
# Constants & Categories
# ==============================================================================
ALLOWED_CATEGORIES = ["Wet Waste", "Dry Waste", "E-Waste", "Hazardous Waste"]
SUPPORTED_IMAGE_FORMATS = ["JPEG", "JPG", "PNG", "WEBP"]


# ==============================================================================
# Professional Line Iconography (Clean SVGs, No Emojis)
# ==============================================================================
SVG_ICONS: Dict[str, str] = {
    "logo": (
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/>'
        '<path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>'
        "</svg>"
    ),
    "sparkles": (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21'
        'l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>'
        "</svg>"
    ),
    "sun": (
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/>'
        '<path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/>'
        '<path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>'
        "</svg>"
    ),
    "moon": (
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>'
        "</svg>"
    ),
    "upload": (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/>'
        '<line x1="12" x2="12" y1="3" y2="15"/>'
        "</svg>"
    ),
    "camera": (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/>'
        '<circle cx="12" cy="13" r="3"/>'
        "</svg>"
    ),
    "check": (
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="20 6 9 17 4 12"/>'
        "</svg>"
    ),
    "check_circle": (
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>'
        "</svg>"
    ),
    "alert_triangle": (
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>'
        '<line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/>'
        "</svg>"
    ),
    "info": (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="16" y2="12"/>'
        '<line x1="12" x2="12.01" y1="8" y2="8"/>'
        "</svg>"
    ),
    "refresh_cw": (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/>'
        '<path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>'
        "</svg>"
    ),
    "tool": (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91'
        'a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>'
        "</svg>"
    ),
    "shield": (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'
        "</svg>"
    ),
    "trash": (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="3 6 5 6 21 6"/>'
        '<path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>'
        "</svg>"
    ),
    "globe": (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="10"/><line x1="2" x2="22" y1="12" y2="12"/>'
        '<path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>'
        "</svg>"
    ),
    "file_text": (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>'
        '<line x1="16" x2="8" y1="13" y2="13"/><line x1="16" x2="8" y1="17" y2="17"/><polyline points="10 9 9 9 8 9"/>'
        "</svg>"
    ),
    "arrow_right": (
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>'
        "</svg>"
    ),
    "empty_inbox": (
        '<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/>'
        '<path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>'
        "</svg>"
    ),
}


def icon(name: str) -> str:
    """Return inline SVG string by name."""
    return SVG_ICONS.get(name, "")


# ==============================================================================
# Theme-Aware Hero Vector Illustration (Clean HTML String, Zero 4-Space Indent)
# ==============================================================================
def get_hero_vector_illustration(theme: str) -> str:
    """Generate high-contrast, theme-aware hero vector illustration as a clean unindented string."""
    is_dark = theme.lower() == "dark"

    # Explicit theme colors for guaranteed contrast and zero disappearance
    bg_surface = "#151821" if is_dark else "#FFFFFF"
    border_color = "#3F475E" if is_dark else "#191A23"
    carbon_surface = "#11141C" if is_dark else "#191A23"
    text_on_carbon = "#F5F5F5"
    text_primary = "#F5F5F5" if is_dark else "#191A23"
    text_muted = "#8E9AA8" if is_dark else "#6E7787"
    lime_accent = "#B9FF66"
    text_on_lime = "#191A23"
    card_light = "#1A1D27" if is_dark else "#F2F4F0"
    shadow_col = "#000000" if is_dark else "#191A23"
    dot_col = "#8E9AA8" if is_dark else "#191A23"

    # Built as single continuous string to prevent Markdown from interpreting any lines as code blocks
    svg_elements = [
        '<div class="hero-illustration-wrapper">',
        '<svg class="hero-illustration-svg" viewBox="0 0 460 340" width="100%" height="auto" fill="none" xmlns="http://www.w3.org/2000/svg">',
        '<defs>',
        f'<pattern id="dotGrid" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="{dot_col}" opacity="0.15" /></pattern>',
        f'<filter id="hardShadow" x="0" y="0" width="200%" height="200%"><feDropShadow dx="4" dy="4" stdDeviation="0" flood-color="{shadow_col}" flood-opacity="1" /></filter>',
        f'<filter id="hardShadowLime" x="0" y="0" width="200%" height="200%"><feDropShadow dx="4" dy="4" stdDeviation="0" flood-color="{border_color}" flood-opacity="1" /></filter>',
        '</defs>',
        f'<rect width="460" height="340" rx="24" fill="{bg_surface}" stroke="{border_color}" stroke-width="2" />',
        '<rect width="460" height="340" rx="24" fill="url(#dotGrid)" />',
        f'<ellipse cx="230" cy="170" rx="140" ry="105" stroke="{border_color}" stroke-width="2" stroke-dasharray="6 6" opacity="0.35" />',
        f'<ellipse cx="230" cy="170" rx="90" ry="65" stroke="{lime_accent}" stroke-width="2.5" opacity="0.85" />',
        '<g filter="url(#hardShadow)">',
        f'<rect x="155" y="115" width="150" height="110" rx="18" fill="{carbon_surface}" stroke="{border_color}" stroke-width="2" />',
        f'<circle cx="230" cy="155" r="22" fill="{lime_accent}" />',
        '<path d="M225 162 A6 6 0 0 1 224 150 C228 149 230 148 232 146 C233 148 234 150 234 153 C234 157 230 162 225 162 Z" fill="#191A23" />',
        '<path d="M220 162 C220 160 221 157 224 156 C227 155 229 154 230 152" stroke="#191A23" stroke-width="1.8" stroke-linecap="round" />',
        f'<text x="230" y="202" fill="{text_on_carbon}" font-size="11" font-weight="800" text-anchor="middle" letter-spacing="1">ECOSORT AI</text>',
        '</g>',
        '<g filter="url(#hardShadowLime)">',
        f'<rect x="30" y="45" width="135" height="52" rx="14" fill="{lime_accent}" stroke="{border_color}" stroke-width="2" />',
        f'<text x="45" y="67" fill="{text_on_lime}" font-size="10" font-weight="800" letter-spacing="0.5">UN SDG 12.5</text>',
        f'<text x="45" y="84" fill="{text_on_lime}" font-size="12" font-weight="700">Substantial Reduction</text>',
        '</g>',
        '<g filter="url(#hardShadow)">',
        f'<rect x="290" y="40" width="140" height="56" rx="14" fill="{bg_surface}" stroke="{border_color}" stroke-width="2" />',
        f'<circle cx="312" cy="68" r="10" fill="{lime_accent}" opacity="0.3" stroke="{lime_accent}" stroke-width="1.5" />',
        f'<circle cx="312" cy="68" r="4" fill="{lime_accent}" />',
        f'<text x="330" y="63" fill="{text_primary}" font-size="11" font-weight="800">Vision + Text</text>',
        f'<text x="330" y="78" fill="{text_muted}" font-size="10" font-weight="600">Dual Multimodal</text>',
        '</g>',
        '<g filter="url(#hardShadow)">',
        f'<rect x="35" y="240" width="135" height="60" rx="14" fill="{card_light}" stroke="{border_color}" stroke-width="2" />',
        f'<text x="48" y="262" fill="{text_muted}" font-size="9" font-weight="800" letter-spacing="0.5">SOURCE ROUTING</text>',
        f'<text x="48" y="282" fill="{text_primary}" font-size="12" font-weight="800">4 Clear Streams</text>',
        '</g>',
        '<g filter="url(#hardShadowLime)">',
        f'<rect x="295" y="235" width="135" height="62" rx="14" fill="{lime_accent}" stroke="{border_color}" stroke-width="2" />',
        f'<text x="310" y="258" fill="{text_on_lime}" font-size="9" font-weight="800" letter-spacing="0.5">CIRCULAR RECOVERY</text>',
        f'<text x="310" y="278" fill="{text_on_lime}" font-size="12" font-weight="800">100% Upcycling</text>',
        '</g>',
        f'<circle cx="105" cy="170" r="6" fill="{border_color}" />',
        f'<circle cx="355" cy="170" r="6" fill="{lime_accent}" stroke="{border_color}" stroke-width="1.5" />',
        f'<circle cx="230" cy="50" r="5" fill="{lime_accent}" />',
        f'<circle cx="230" cy="290" r="5" fill="{border_color}" />',
        '</svg>',
        '</div>'
    ]
    return "".join(svg_elements)


# ==============================================================================
# Data Models for Structured Analysis
# ==============================================================================
class WasteAnalysis(BaseModel):
    """Structured response schema for text-based waste classification."""

    primary_category: str = Field(
        description="Must be exactly one of: 'Wet Waste', 'Dry Waste', 'E-Waste', 'Hazardous Waste'."
    )
    disposal_action: str = Field(
        description="Clear, actionable, step-by-step instructions for responsible disposal."
    )
    environmental_risk: str = Field(
        description="Explanation of the ecological damage or safety hazard caused by improper disposal."
    )
    diy_upcycling_suggestion: str = Field(
        description="A practical, creative, and safe DIY reuse or upcycling suggestion if applicable, or safe repurposing advice."
    )


class DiscreteItem(BaseModel):
    """Structured schema for a single identifiable waste item in multimodal analysis."""

    item_name: str = Field(description="Recognizable name of the waste item.")
    material: str = Field(description="Visual material estimate or 'material uncertain'.")
    waste_category: str = Field(
        description="Must be one of: 'Wet Waste', 'Dry Waste', 'E-Waste', 'Hazardous Waste'."
    )
    disposal_action: str = Field(
        description="Practical disposal instructions and routing."
    )
    preparation_steps: List[str] = Field(
        default_factory=list,
        description="Step-by-step preparation steps (e.g. empty, rinse, separate cap).",
    )
    environmental_risk: str = Field(
        description="Ecological or environmental harm if improperly discarded."
    )
    upcycling_suggestion: str = Field(
        description="Practical, safe reuse or upcycling suggestion."
    )


class DiscreteAnalysis(BaseModel):
    """Container for discrete items analysis."""

    items: List[DiscreteItem] = Field(default_factory=list)


class TrashHeapAnalysis(BaseModel):
    """Structured schema for open dump sites, piles, or mixed accumulations."""

    site_assessment: str = Field(
        description="Overall evaluation of the accumulation site and scale."
    )
    dominant_materials: List[str] = Field(
        default_factory=list, description="List of primary visible materials observed."
    )
    waste_categories_present: List[str] = Field(
        default_factory=list, description="Waste categories identified across the site."
    )
    environmental_risks: List[str] = Field(
        default_factory=list,
        description="Major ecological threats (leachate, fire, vectors, contamination).",
    )
    safety_measures: List[str] = Field(
        default_factory=list,
        description="Immediate safety guidelines for personnel and bystanders.",
    )
    recommended_ppe: List[str] = Field(
        default_factory=list,
        description="Appropriate PPE based strictly on visible hazards.",
    )
    tools_required: List[str] = Field(
        default_factory=list,
        description="Required tools and equipment for safe sorting and cleanup.",
    )
    cleanup_protocol: List[str] = Field(
        default_factory=list,
        description="Numbered, step-by-step safe cleanup sequence.",
    )
    municipal_routing: str = Field(
        description="Official municipal or authorized waste coordination instructions."
    )


class MultimodalWasteResponse(BaseModel):
    """Top-level structured response for multimodal scene analysis."""

    scene_type: str = Field(
        description="Must be either 'DISCRETE_ITEMS' or 'TRASH_HEAP'."
    )
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0."
    )
    observations: List[str] = Field(
        default_factory=list, description="Concise visual observations from the image."
    )
    context_used: bool = Field(
        default=False,
        description="Whether user-supplied context was utilized in the analysis.",
    )
    analysis: Dict[str, Any] = Field(
        default_factory=dict,
        description="Detailed analysis matching the scene_type schema.",
    )


# ==============================================================================
# Helper Functions: API Key, Category & Image Validation
# ==============================================================================
def get_gemini_api_key() -> Optional[str]:
    """Retrieve Gemini API key from Streamlit secrets, environment, or sidebar input."""
    try:
        if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
            return str(st.secrets["GEMINI_API_KEY"]).strip()
    except Exception:
        pass

    env_key = os.getenv("GEMINI_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()

    if "sidebar_api_key" in st.session_state and st.session_state["sidebar_api_key"]:
        return st.session_state["sidebar_api_key"].strip()

    return None


def normalize_category(raw_cat: str) -> str:
    """Ensure the returned category matches one of the 4 strict categories."""
    raw = raw_cat.strip().lower()
    if "wet" in raw or "organic" in raw or "biodegradable" in raw or "food" in raw:
        return "Wet Waste"
    elif "e-waste" in raw or "electronic" in raw or "ewaste" in raw:
        return "E-Waste"
    elif (
        "hazard" in raw
        or "toxic" in raw
        or "chemical" in raw
        or "sharp" in raw
        or "biohazard" in raw
    ):
        return "Hazardous Waste"
    elif (
        "dry" in raw
        or "recycl" in raw
        or "paper" in raw
        or "plastic" in raw
        or "metal" in raw
    ):
        return "Dry Waste"
    return "Dry Waste"


def load_and_validate_image(
    uploaded_file: Optional[Any], camera_file: Optional[Any]
) -> Tuple[Optional[Image.Image], Optional[str], Optional[str]]:
    """Safely decode and validate user-supplied image.

    If both upload and camera files are provided, uploaded_file takes priority.
    Returns: (PIL.Image or None, error_message or None, source_type or None).
    """
    target_file = None
    source_type = None

    if uploaded_file is not None:
        target_file = uploaded_file
        source_type = "upload"
    elif camera_file is not None:
        target_file = camera_file
        source_type = "camera"

    if target_file is None:
        return None, None, None

    try:
        file_bytes = target_file.getvalue()
        if not file_bytes:
            return None, "Selected image file appears to be empty.", source_type

        img = Image.open(io.BytesIO(file_bytes))
        img.load()

        img_format = (img.format or "").upper()
        if img_format not in SUPPORTED_IMAGE_FORMATS:
            return (
                None,
                f"Unsupported image format ({img_format}). Please upload a JPG, JPEG, PNG, or WEBP image.",
                source_type,
            )

        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        return img, None, source_type
    except (UnidentifiedImageError, OSError, ValueError) as err:
        return (
            None,
            f"We couldn't read this image ({str(err)}). Please upload a valid JPG, PNG, or WEBP image.",
            source_type,
        )


# ==============================================================================
# Gemini Analysis Pipelines (Text & Multimodal)
# ==============================================================================
def analyze_waste_with_gemini(item_description: str, api_key: str) -> WasteAnalysis:
    """Analyze a text-based waste item using Google's modern google-genai SDK."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    system_instruction = (
        "You are EcoSort AI, an expert waste-management and sustainability specialist assistant. "
        "Your task is to analyze household and campus waste items to promote UN SDG 12 (Responsible Consumption and Production).\n\n"
        "Rules:\n"
        "1. Classify the item into EXACTLY ONE of the following 4 categories:\n"
        "   - 'Wet Waste' (organic, kitchen scraps, food, garden waste, compostables)\n"
        "   - 'Dry Waste' (clean recyclables like paper, plastics, glass, metals, textiles)\n"
        "   - 'E-Waste' (electronic items, gadgets, circuits, cables, appliances)\n"
        "   - 'Hazardous Waste' (batteries, paints, chemicals, CFL bulbs, medical waste, sharp contaminated items)\n"
        "2. Provide practical, step-by-step disposal instructions.\n"
        "3. Describe the major environmental risk if the item is discarded improperly in landfills or nature.\n"
        "4. Suggest a realistic, safe DIY reuse/upcycling idea where appropriate. If the item is hazardous, do NOT suggest unsafe craft; instead advise safe containment or battery recycling depot drop-off.\n"
        "5. Do NOT invent specific imaginary local facilities; recommend standard authorized collection points.\n"
        "6. Return strictly the required structured fields."
    )

    prompt = f'Analyze the following waste item for responsible disposal and reuse: "{item_description}"'

    models_to_try = [
        "gemini-flash-latest",
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.8-flash",
        "gemini-2.5-flash",
    ]

    last_error: Optional[Exception] = None

    for model_name in models_to_try:
        try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        response_mime_type="application/json",
                        response_schema=WasteAnalysis,
                        temperature=0.1,
                    ),
                )
            except Exception:
                structured_prompt = (
                    f"{prompt}\n\n"
                    "Return ONLY a valid JSON object with these exact keys:\n"
                    "{\n"
                    '  "primary_category": "Wet Waste | Dry Waste | E-Waste | Hazardous Waste",\n'
                    '  "disposal_action": "Practical instructions",\n'
                    '  "environmental_risk": "Environmental harm if mismanaged",\n'
                    '  "diy_upcycling_suggestion": "Practical reuse or safe recommendation"\n'
                    "}\n"
                    "Do NOT include Markdown code blocks or any other commentary."
                )
                response = client.models.generate_content(
                    model=model_name,
                    contents=structured_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.1,
                    ),
                )

            raw_text = response.text if hasattr(response, "text") and response.text else ""
            if not raw_text:
                continue

            cleaned_text = re.sub(r"^```json\s*", "", raw_text.strip(), flags=re.IGNORECASE)
            cleaned_text = re.sub(r"^```\s*", "", cleaned_text.strip())
            cleaned_text = re.sub(r"```$", "", cleaned_text.strip())

            parsed_dict = json.loads(cleaned_text)
            analysis = WasteAnalysis(**parsed_dict)
            analysis.primary_category = normalize_category(analysis.primary_category)
            return analysis

        except (ValidationError, json.JSONDecodeError) as parse_err:
            last_error = parse_err
            continue
        except Exception as api_err:
            last_error = api_err
            err_msg = str(api_err).lower()
            if "api_key_invalid" in err_msg or "api key not valid" in err_msg or "unauthenticated" in err_msg:
                raise api_err
            continue

    if last_error:
        raise last_error

    raise RuntimeError("Failed to generate classification from Gemini models.")


def analyze_multimodal_waste_with_gemini(
    image: Image.Image, optional_context: Optional[str], api_key: str
) -> MultimodalWasteResponse:
    """Analyze a waste image and optional context using Google's modern google-genai SDK."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    system_instruction = (
        "You are EcoSort AI Vision, an expert waste-management, environmental safety, and material-recovery specialist. "
        "Your task is to analyze waste scenes from images and optional user context to support UN SDG 12 (Responsible Consumption and Production).\n\n"
        "CORE OPERATING PRINCIPLES:\n"
        "1. PRIORITIZE VISUAL EVIDENCE: Physical visual evidence in the image takes absolute priority over user-supplied context. "
        "Treat user context strictly as supplementary background; do NOT let context override what is visibly present.\n"
        "2. SCENE CLASSIFICATION: Classify the scene into EXACTLY ONE of:\n"
        "   - 'DISCRETE_ITEMS': One item or a small number of individually identifiable waste items.\n"
        "   - 'TRASH_HEAP': A pile, open dumping area, roadside heap, field accumulation, or unsorted mixed waste collection.\n"
        "   If uncertain, select the category that best matches the visible scene and note uncertainty in observations.\n"
        "3. ALLOWED WASTE CATEGORIES: For every item or category identified, use EXACTLY one of: "
        "'Wet Waste', 'Dry Waste', 'E-Waste', 'Hazardous Waste'.\n"
        "4. DO NOT INVENT: Only report materials visually supported. Use wording like 'appears to be' or 'material uncertain' where ambiguous. "
        "Never fabricate hidden contents, brands, or imaginary local facilities.\n"
        "5. SAFETY & MUNICIPAL ROUTING: For hazardous waste, chemicals, batteries, and sharps, prioritize authorized drop-off and safety. "
        "Never advise unsafe DIY handling of toxic materials. For municipal rules, state: 'Follow your local waste authority's bin and collection rules.'\n"
        "6. STRICT JSON: Return strictly a valid JSON object matching the required schema. No Markdown fences, no explanations outside JSON."
    )

    context_prompt_part = ""
    if optional_context and optional_context.strip():
        context_prompt_part = f'\nUser Provided Context (Supplementary only): "{optional_context.strip()}"\n'

    prompt = (
        "Analyze this waste image carefully and provide the structured evaluation.\n"
        f"{context_prompt_part}\n"
        "Required JSON Output Schema:\n"
        "{\n"
        '  "scene_type": "DISCRETE_ITEMS" | "TRASH_HEAP",\n'
        '  "confidence": <float between 0.0 and 1.0>,\n'
        '  "observations": [<list of concise visual observations>],\n'
        '  "context_used": <true if user context influenced details, else false>,\n'
        '  "analysis": {\n'
        '    // If scene_type is "DISCRETE_ITEMS", provide:\n'
        '    "items": [\n'
        "      {\n"
        '        "item_name": "Name of item",\n'
        '        "material": "Material composition or material uncertain",\n'
        '        "waste_category": "Wet Waste | Dry Waste | E-Waste | Hazardous Waste",\n'
        '        "disposal_action": "Disposal instruction",\n'
        '        "preparation_steps": ["Step 1", "Step 2"],\n'
        '        "environmental_risk": "Ecological harm if discarded improperly",\n'
        '        "upcycling_suggestion": "Realistic DIY upcycling or reuse idea"\n'
        "      }\n"
        "    ]\n"
        '    // If scene_type is "TRASH_HEAP", provide:\n'
        '    "site_assessment": "Assessment of accumulation site",\n'
        '    "dominant_materials": ["Material 1", "Material 2"],\n'
        '    "waste_categories_present": ["Wet Waste", "Dry Waste", "E-Waste", "Hazardous Waste"],\n'
        '    "environmental_risks": ["Risk 1", "Risk 2"],\n'
        '    "safety_measures": ["Measure 1", "Measure 2"],\n'
        '    "recommended_ppe": ["PPE 1", "PPE 2"],\n'
        '    "tools_required": ["Tool 1", "Tool 2"],\n'
        '    "cleanup_protocol": ["1. Step one...", "2. Step two..."],\n'
        '    "municipal_routing": "General routing guidance for municipal authorities"\n'
        "  }\n"
        "}\n"
        "Return ONLY the JSON object. Do not include markdown ticks or text outside JSON."
    )

    models_to_try = [
        "gemini-flash-latest",
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.8-flash",
        "gemini-2.5-flash",
    ]

    last_error: Optional[Exception] = None

    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[image, prompt],
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )

            raw_text = response.text if hasattr(response, "text") and response.text else ""
            if not raw_text:
                continue

            cleaned_text = re.sub(r"^```json\s*", "", raw_text.strip(), flags=re.IGNORECASE)
            cleaned_text = re.sub(r"^```\s*", "", cleaned_text.strip())
            cleaned_text = re.sub(r"```$", "", cleaned_text.strip())

            parsed_dict = json.loads(cleaned_text)

            scene_type = parsed_dict.get("scene_type", "").upper()
            if "DISCRETE" in scene_type:
                parsed_dict["scene_type"] = "DISCRETE_ITEMS"
            elif "HEAP" in scene_type or "TRASH" in scene_type or "PILE" in scene_type:
                parsed_dict["scene_type"] = "TRASH_HEAP"
            else:
                parsed_dict["scene_type"] = "DISCRETE_ITEMS"

            conf = float(parsed_dict.get("confidence", 0.85))
            parsed_dict["confidence"] = max(0.0, min(1.0, conf))

            analysis_dict = parsed_dict.get("analysis", {})
            if parsed_dict["scene_type"] == "DISCRETE_ITEMS":
                items_data = analysis_dict.get("items", [])
                validated_items = []
                for itm in items_data:
                    itm["waste_category"] = normalize_category(itm.get("waste_category", "Dry Waste"))
                    if not isinstance(itm.get("preparation_steps"), list):
                        itm["preparation_steps"] = [str(itm.get("preparation_steps", ""))]
                    validated_items.append(DiscreteItem(**itm))
                parsed_dict["analysis"] = DiscreteAnalysis(items=validated_items).model_dump()
            else:
                raw_categories = analysis_dict.get("waste_categories_present", [])
                normalized_categories = list(set([normalize_category(c) for c in raw_categories]))
                analysis_dict["waste_categories_present"] = normalized_categories
                parsed_dict["analysis"] = TrashHeapAnalysis(**analysis_dict).model_dump()

            result = MultimodalWasteResponse(**parsed_dict)
            return result

        except (ValidationError, json.JSONDecodeError) as parse_err:
            last_error = parse_err
            continue
        except Exception as api_err:
            last_error = api_err
            err_msg = str(api_err).lower()
            if "api_key_invalid" in err_msg or "api key not valid" in err_msg or "unauthenticated" in err_msg:
                raise api_err
            continue

    if last_error:
        raise last_error

    raise RuntimeError("Failed to generate multimodal analysis from Gemini.")


# ==============================================================================
# Design Token System (Neo-Brutalist Light & Dark Mode)
# ==============================================================================
def get_theme_css(theme: str) -> str:
    """Generate modern editorial / neo-brutalist scoped CSS variables and styles."""
    is_dark = theme.lower() == "dark"

    if is_dark:
        tokens = {
            "bg": "#0D0F14",
            "surface": "#151821",
            "surface_elevated": "#1D202A",
            "surface_card_light": "#1A1D27",
            "surface_carbon": "#11141C",
            "surface_lime": "#B9FF66",
            "text_primary": "#F5F5F5",
            "text_secondary": "#CBD5E1",
            "text_muted": "#8E9AA8",
            "text_on_carbon": "#F5F5F5",
            "text_on_lime": "#191A23",
            "border": "#2E3446",
            "border_strong": "#3F475E",
            "border_subtle": "#222735",
            "shadow_color": "#000000",
            "accent": "#B9FF66",
            "accent_hover": "#A8F052",
            "uploader_btn_bg": "#B9FF66",
            "uploader_btn_fg": "#191A23",
            "uploader_btn_border": "#B9FF66",
            "cat_wet_bg": "#0A291E",
            "cat_wet_fg": "#4ADE80",
            "cat_wet_border": "#166534",
            "cat_dry_bg": "#0C243B",
            "cat_dry_fg": "#60A5FA",
            "cat_dry_border": "#1E40AF",
            "cat_ewaste_bg": "#2E2108",
            "cat_ewaste_fg": "#FBBF24",
            "cat_ewaste_border": "#854D0E",
            "cat_hazard_bg": "#331215",
            "cat_hazard_fg": "#F87171",
            "cat_hazard_border": "#991B1B",
        }
    else:
        tokens = {
            "bg": "#F6FAF8",
            "surface": "#FFFFFF",
            "surface_elevated": "#FFFFFF",
            "surface_card_light": "#F2F4F0",
            "surface_carbon": "#191A23",
            "surface_lime": "#B9FF66",
            "text_primary": "#191A23",
            "text_secondary": "#3D4451",
            "text_muted": "#6E7787",
            "text_on_carbon": "#F5F5F5",
            "text_on_lime": "#191A23",
            "border": "#191A23",
            "border_strong": "#191A23",
            "border_subtle": "#E5E8EB",
            "shadow_color": "#191A23",
            "accent": "#B9FF66",
            "accent_hover": "#A8F052",
            "uploader_btn_bg": "#191A23",
            "uploader_btn_fg": "#B9FF66",
            "uploader_btn_border": "#191A23",
            "cat_wet_bg": "#E9F9EE",
            "cat_wet_fg": "#14532D",
            "cat_wet_border": "#191A23",
            "cat_dry_bg": "#EBF4FF",
            "cat_dry_fg": "#1E3A8A",
            "cat_dry_border": "#191A23",
            "cat_ewaste_bg": "#FEF9C3",
            "cat_ewaste_fg": "#713F12",
            "cat_ewaste_border": "#191A23",
            "cat_hazard_bg": "#FEE2E2",
            "cat_hazard_fg": "#991B1B",
            "cat_hazard_border": "#191A23",
        }

    return f"""
    <style>
    :root {{
        --bg: {tokens['bg']};
        --surface: {tokens['surface']};
        --surface-elevated: {tokens['surface_elevated']};
        --surface-card-light: {tokens['surface_card_light']};
        --surface-carbon: {tokens['surface_carbon']};
        --surface-lime: {tokens['surface_lime']};
        --text-primary: {tokens['text_primary']};
        --text-secondary: {tokens['text_secondary']};
        --text-muted: {tokens['text_muted']};
        --text-on-carbon: {tokens['text_on_carbon']};
        --text-on-lime: {tokens['text_on_lime']};
        --border: {tokens['border']};
        --border-strong: {tokens['border_strong']};
        --border-subtle: {tokens['border_subtle']};
        --shadow-color: {tokens['shadow_color']};
        --accent: {tokens['accent']};
        --accent-hover: {tokens['accent_hover']};
        --uploader-btn-bg: {tokens['uploader_btn_bg']};
        --uploader-btn-fg: {tokens['uploader_btn_fg']};
        --uploader-btn-border: {tokens['uploader_btn_border']};
        --cat-wet-bg: {tokens['cat_wet_bg']};
        --cat-wet-fg: {tokens['cat_wet_fg']};
        --cat-wet-border: {tokens['cat_wet_border']};
        --cat-dry-bg: {tokens['cat_dry_bg']};
        --cat-dry-fg: {tokens['cat_dry_fg']};
        --cat-dry-border: {tokens['cat_dry_border']};
        --cat-ewaste-bg: {tokens['cat_ewaste_bg']};
        --cat-ewaste-fg: {tokens['cat_ewaste_fg']};
        --cat-ewaste-border: {tokens['cat_ewaste_border']};
        --cat-hazard-bg: {tokens['cat_hazard_bg']};
        --cat-hazard-fg: {tokens['cat_hazard_fg']};
        --cat-hazard-border: {tokens['cat_hazard_border']};
    }}

    /* Global page layout */
    .stApp {{
        background-color: var(--bg) !important;
        color: var(--text-primary) !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }}

    header, [data-testid="stHeader"] {{
        background-color: var(--bg) !important;
    }}

    .main .block-container {{
        padding-top: 1.25rem !important;
        padding-bottom: 4rem !important;
        max-width: 1120px !important;
    }}

    /* Editorial Brand Nav */
    .editorial-nav {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.85rem 0 1.25rem 0;
        border-bottom: 2px solid var(--border);
        margin-bottom: 2rem;
    }}
    .brand-group {{
        display: flex;
        align-items: center;
        gap: 0.85rem;
    }}
    .brand-mark {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        background-color: var(--surface-carbon);
        color: var(--accent);
        border: 2px solid var(--border);
        border-radius: 14px;
        box-shadow: 0 4px 0 var(--shadow-color);
    }}
    .brand-title {{
        font-size: 1.45rem;
        font-weight: 900;
        letter-spacing: -0.03em;
        color: var(--text-primary);
        line-height: 1.1;
    }}
    .brand-descriptor {{
        font-size: 0.78rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}

    /* Neo-Brutalist Hero Section */
    .hero-container {{
        margin-bottom: 1.5rem;
    }}
    .hero-pill {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background-color: var(--surface-lime);
        color: var(--text-on-lime);
        border: 2px solid var(--border);
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 800;
        padding: 0.35rem 0.9rem;
        box-shadow: 0 3px 0 var(--shadow-color);
        margin-bottom: 1.25rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    .hero-headline {{
        font-size: clamp(2.2rem, 4.2vw, 3.4rem);
        font-weight: 900;
        letter-spacing: -0.04em;
        line-height: 1.08;
        color: var(--text-primary);
        margin-bottom: 1.1rem;
    }}
    .highlight-lime {{
        background-color: var(--surface-lime);
        color: var(--text-on-lime);
        padding: 0 0.4rem;
        border-radius: 6px;
        border: 2px solid var(--border);
        display: inline-block;
        box-shadow: 0 3px 0 var(--shadow-color);
    }}
    .hero-subhead {{
        font-size: 1.06rem;
        line-height: 1.55;
        color: var(--text-secondary);
        font-weight: 500;
        max-width: 540px;
        margin-bottom: 1.4rem;
    }}
    .hero-cta-row {{
        display: flex;
        align-items: center;
        gap: 0.85rem;
        flex-wrap: wrap;
    }}
    .hero-cta-primary {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background-color: var(--surface-carbon);
        color: var(--accent) !important;
        border: 2px solid var(--border);
        border-radius: 14px;
        font-weight: 800;
        font-size: 0.92rem;
        padding: 0.7rem 1.4rem;
        box-shadow: 0 4px 0 var(--shadow-color);
        text-decoration: none !important;
        transition: transform 0.12s ease, box-shadow 0.12s ease, background-color 0.12s ease;
    }}
    .hero-cta-primary:hover {{
        background-color: var(--accent);
        color: var(--text-on-lime) !important;
        transform: translate(-2px, -2px);
        box-shadow: 0 6px 0 var(--shadow-color);
    }}
    .hero-cta-secondary {{
        display: inline-flex;
        align-items: center;
        background-color: var(--surface);
        color: var(--text-primary) !important;
        border: 2px solid var(--border);
        border-radius: 14px;
        font-weight: 700;
        font-size: 0.92rem;
        padding: 0.7rem 1.3rem;
        box-shadow: 0 4px 0 var(--shadow-color);
        text-decoration: none !important;
        transition: transform 0.12s ease, box-shadow 0.12s ease;
    }}
    .hero-cta-secondary:hover {{
        background-color: var(--surface-card-light);
        transform: translate(-2px, -2px);
        box-shadow: 0 6px 0 var(--shadow-color);
    }}

    /* Hero SVG Wrapper & Responsiveness */
    .hero-illustration-wrapper {{
        width: 100%;
        max-width: 460px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    .hero-illustration-svg {{
        width: 100%;
        height: auto;
        max-width: 100%;
        display: block;
    }}

    /* Capabilities Strip */
    .capabilities-strip {{
        display: flex;
        align-items: center;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 0.75rem;
        background-color: var(--surface);
        border: 2px solid var(--border);
        border-radius: 18px;
        padding: 0.9rem 1.25rem;
        box-shadow: 0 4px 0 var(--shadow-color);
        margin: 2.5rem 0 3.5rem 0;
    }}
    .cap-item {{
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        font-size: 0.85rem;
        font-weight: 800;
        color: var(--text-primary);
        letter-spacing: 0.02em;
    }}
    .cap-divider {{
        color: var(--border-subtle);
        font-weight: 900;
    }}

    /* Section Headings */
    .eco-section-header {{
        margin-bottom: 1.75rem;
    }}
    .section-meta-pill {{
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        background-color: var(--surface-card-light);
        color: var(--text-muted);
        padding: 0.25rem 0.65rem;
        border: 1.5px solid var(--border);
        border-radius: 9999px;
        margin-bottom: 0.5rem;
    }}
    .section-main-title {{
        font-size: 2rem;
        font-weight: 900;
        letter-spacing: -0.03em;
        color: var(--text-primary);
        line-height: 1.15;
        margin-bottom: 0.35rem;
    }}
    .section-desc {{
        font-size: 0.95rem;
        color: var(--text-secondary);
        font-weight: 500;
    }}

    /* Process 01-04 Cards */
    .process-card {{
        border: 2px solid var(--border);
        border-radius: 22px;
        padding: 1.4rem;
        box-shadow: 0 5px 0 var(--shadow-color);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .process-card:hover {{
        transform: translate(-2px, -2px);
        box-shadow: 0 7px 0 var(--shadow-color);
    }}
    .card-white {{
        background-color: var(--surface);
        color: var(--text-primary);
    }}
    .card-lime {{
        background-color: var(--surface-lime);
        color: var(--text-on-lime);
    }}
    .card-carbon {{
        background-color: var(--surface-carbon);
        color: var(--text-on-carbon);
    }}
    .card-light {{
        background-color: var(--surface-card-light);
        color: var(--text-primary);
    }}
    .card-num-tag {{
        font-size: 1.6rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        line-height: 1;
        margin-bottom: 0.75rem;
    }}
    .card-header-title {{
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }}
    .card-body-text {{
        font-size: 0.88rem;
        line-height: 1.5;
        font-weight: 500;
        opacity: 0.92;
    }}

    /* Streamlit Input Fields */
    .stTextArea textarea, .stTextInput input {{
        background-color: var(--surface) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border) !important;
        border-radius: 14px !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        box-shadow: 0 3px 0 var(--shadow-color) !important;
        padding: 0.75rem 1rem !important;
    }}
    .stTextArea textarea:focus, .stTextInput input:focus {{
        border-color: var(--accent) !important;
        outline: none !important;
        box-shadow: 0 4px 0 var(--shadow-color) !important;
    }}
    .stTextArea textarea::placeholder, .stTextInput input::placeholder {{
        color: var(--text-muted) !important;
    }}

    /* Primary Tactile Button */
    .stButton > button[kind="primary"] {{
        background-color: var(--surface-carbon) !important;
        color: var(--accent) !important;
        border: 2px solid var(--border) !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.02em !important;
        padding: 0.7rem 1.75rem !important;
        box-shadow: 0 5px 0 var(--shadow-color) !important;
        transition: transform 0.12s ease, box-shadow 0.12s ease, background-color 0.12s ease !important;
    }}
    .stButton > button[kind="primary"]:hover {{
        background-color: var(--accent) !important;
        color: var(--text-on-lime) !important;
        transform: translate(-2px, -2px) !important;
        box-shadow: 0 7px 0 var(--shadow-color) !important;
    }}
    .stButton > button[kind="primary"]:active {{
        transform: translate(0, 3px) !important;
        box-shadow: 0 2px 0 var(--shadow-color) !important;
    }}

    /* Secondary Tactile Button */
    .stButton > button[kind="secondary"] {{
        background-color: var(--surface) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border) !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        padding: 0.65rem 1.4rem !important;
        box-shadow: 0 4px 0 var(--shadow-color) !important;
        transition: transform 0.12s ease, box-shadow 0.12s ease !important;
    }}
    .stButton > button[kind="secondary"]:hover {{
        background-color: var(--surface-card-light) !important;
        transform: translate(-2px, -2px) !important;
        box-shadow: 0 6px 0 var(--shadow-color) !important;
    }}

    /* Quick Example Pills */
    div[data-testid="column"] .stButton > button {{
        background-color: var(--surface) !important;
        color: var(--text-primary) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 9999px !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        padding: 0.4rem 0.8rem !important;
        box-shadow: 0 2.5px 0 var(--shadow-color) !important;
        transition: all 0.12s ease !important;
    }}
    div[data-testid="column"] .stButton > button:hover {{
        background-color: var(--surface-lime) !important;
        color: var(--text-on-lime) !important;
        transform: translate(-1.5px, -1.5px) !important;
        box-shadow: 0 4px 0 var(--shadow-color) !important;
    }}

    /* Streamlit Tabs - Seamless Design Integration */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.75rem !important;
        border-bottom: none !important;
        background-color: transparent !important;
        margin-bottom: 1.5rem !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: var(--surface-card-light) !important;
        color: var(--text-secondary) !important;
        border: 2px solid var(--border) !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        padding: 0.65rem 1.6rem !important;
        box-shadow: 0 3px 0 var(--shadow-color) !important;
        transition: all 0.15s ease !important;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        color: var(--text-primary) !important;
        transform: translate(-1.5px, -1.5px) !important;
        box-shadow: 0 5px 0 var(--shadow-color) !important;
    }}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background-color: var(--surface-lime) !important;
        color: var(--text-on-lime) !important;
        border-color: var(--border) !important;
        box-shadow: 0 4px 0 var(--shadow-color) !important;
    }}
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {{
        display: none !important;
    }}

    /* File Uploader - Complete High-Contrast Integration */
    [data-testid="stFileUploader"] {{
        background-color: var(--surface) !important;
        border: 2px dashed var(--border) !important;
        border-radius: 18px !important;
        padding: 0.85rem !important;
        box-shadow: 0 4px 0 var(--shadow-color) !important;
    }}
    [data-testid="stFileUploaderDropzone"] {{
        background-color: var(--surface-card-light) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 14px !important;
        padding: 0.75rem 1rem !important;
    }}
    [data-testid="stFileUploaderDropzone"] button,
    [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"] {{
        background-color: var(--uploader-btn-bg) !important;
        color: var(--uploader-btn-fg) !important;
        border: 2px solid var(--uploader-btn-border) !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        font-size: 0.88rem !important;
        padding: 0.45rem 1.1rem !important;
        box-shadow: 0 3px 0 var(--shadow-color) !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
    }}
    [data-testid="stFileUploaderDropzone"] button:hover,
    [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"]:hover {{
        background-color: var(--accent-hover) !important;
        color: var(--text-on-lime) !important;
        transform: translate(-1.5px, -1.5px) !important;
        box-shadow: 0 4px 0 var(--shadow-color) !important;
    }}
    [data-testid="stFileUploaderDropzoneInstructions"],
    [data-testid="stFileUploaderDropzoneInstructions"] span,
    [data-testid="stFileUploaderDropzoneInstructions"] div {{
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
    }}
    [data-testid="stFileUploader"] section {{
        background-color: var(--surface-card-light) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 10px !important;
    }}
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] {{
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }}

    /* Camera Component - High-Contrast Dark & Light Support */
    [data-testid="stCameraInput"] {{
        background-color: var(--surface) !important;
        border: 2px dashed var(--border) !important;
        border-radius: 18px !important;
        padding: 0.85rem !important;
        box-shadow: 0 4px 0 var(--shadow-color) !important;
    }}
    [data-testid="stCameraInput"] [data-testid="stCameraInputWebcamComponent"] {{
        background-color: var(--surface-card-light) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 14px !important;
        overflow: hidden !important;
    }}
    [data-testid="stCameraInput"] p,
    [data-testid="stCameraInput"] span {{
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }}
    [data-testid="stCameraInput"] a {{
        color: var(--accent) !important;
        font-weight: 700 !important;
        text-decoration: underline !important;
    }}
    [data-testid="stCameraInputButton"],
    [data-testid="stCameraInput"] button {{
        background-color: var(--uploader-btn-bg) !important;
        color: var(--uploader-btn-fg) !important;
        border: 2px solid var(--uploader-btn-border) !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        font-size: 0.9rem !important;
        padding: 0.55rem 1.25rem !important;
        box-shadow: 0 3px 0 var(--shadow-color) !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
    }}
    [data-testid="stCameraInputButton"]:hover:not(:disabled),
    [data-testid="stCameraInput"] button:hover:not(:disabled) {{
        background-color: var(--accent-hover) !important;
        color: var(--text-on-lime) !important;
        transform: translate(-1.5px, -1.5px) !important;
        box-shadow: 0 4px 0 var(--shadow-color) !important;
    }}
    [data-testid="stCameraInputButton"]:disabled {{
        background-color: var(--surface-card-light) !important;
        color: var(--text-muted) !important;
        border-color: var(--border-subtle) !important;
        cursor: not-allowed !important;
        box-shadow: none !important;
    }}

    /* Expanders / FAQ */
    .stExpander {{
        background-color: var(--surface) !important;
        border: 2px solid var(--border) !important;
        border-radius: 16px !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 4px 0 var(--shadow-color) !important;
        overflow: hidden !important;
    }}
    .stExpander details summary {{
        color: var(--text-primary) !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        padding: 0.85rem 1rem !important;
    }}

    /* Category Badges */
    .cat-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.02em;
        border: 1.5px solid var(--border);
        box-shadow: 0 2px 0 var(--shadow-color);
    }}
    .cat-badge-wet {{
        background-color: var(--cat-wet-bg);
        color: var(--cat-wet-fg);
    }}
    .cat-badge-dry {{
        background-color: var(--cat-dry-bg);
        color: var(--cat-dry-fg);
    }}
    .cat-badge-ewaste {{
        background-color: var(--cat-ewaste-bg);
        color: var(--cat-ewaste-fg);
    }}
    .cat-badge-hazard {{
        background-color: var(--cat-hazard-bg);
        color: var(--cat-hazard-fg);
    }}

    /* Result Cards */
    .result-container-card {{
        border: 2px solid var(--border);
        border-radius: 24px;
        padding: 1.6rem;
        box-shadow: 0 6px 0 var(--shadow-color);
        margin-bottom: 1.25rem;
    }}
    .result-card-a {{
        background-color: var(--surface-carbon);
        color: var(--text-on-carbon);
    }}
    .result-card-b {{
        background-color: var(--surface-lime);
        color: var(--text-on-lime);
    }}
    .result-card-c {{
        background-color: var(--surface-card-light);
        color: var(--text-primary);
    }}
    .result-title-row {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 1.2rem;
        font-weight: 900;
        letter-spacing: -0.02em;
        margin-bottom: 0.75rem;
    }}
    .result-body-text {{
        font-size: 0.98rem;
        line-height: 1.6;
        font-weight: 500;
    }}

    /* Safety Alert Banner */
    .hazard-safety-banner {{
        background-color: var(--cat-hazard-bg);
        border: 2px solid var(--border);
        border-radius: 18px;
        padding: 1.2rem 1.4rem;
        color: var(--cat-hazard-fg);
        box-shadow: 0 5px 0 var(--shadow-color);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: flex-start;
        gap: 0.85rem;
    }}
    .hazard-banner-title {{
        font-size: 1rem;
        font-weight: 900;
        letter-spacing: -0.01em;
        margin-bottom: 0.25rem;
    }}

    /* SDG 12 Mission Panel */
    .mission-panel {{
        background-color: var(--surface-carbon);
        color: var(--text-on-carbon);
        border: 2px solid var(--border);
        border-radius: 28px;
        padding: 2.5rem 2rem;
        box-shadow: 0 8px 0 var(--shadow-color);
        margin: 3.5rem 0 2.5rem 0;
    }}
    .mission-pill {{
        display: inline-block;
        background-color: var(--surface-lime);
        color: var(--text-on-lime);
        border: 2px solid var(--border);
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 900;
        padding: 0.35rem 0.85rem;
        box-shadow: 0 3px 0 var(--shadow-color);
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    .mission-title {{
        font-size: 2.2rem;
        font-weight: 900;
        letter-spacing: -0.03em;
        line-height: 1.15;
        margin-bottom: 0.9rem;
    }}
    .mission-desc {{
        font-size: 1.02rem;
        line-height: 1.6;
        color: #E2E8F0;
        max-width: 740px;
        margin-bottom: 2rem;
    }}
    .mission-stat-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.25rem;
    }}
    .mission-stat-box {{
        background-color: rgba(255, 255, 255, 0.05);
        border: 1.5px solid var(--border);
        border-radius: 18px;
        padding: 1.25rem;
    }}
    .stat-number {{
        font-size: 1.8rem;
        font-weight: 900;
        color: var(--accent);
        line-height: 1;
        margin-bottom: 0.35rem;
    }}
    .stat-label {{
        font-size: 0.85rem;
        font-weight: 700;
        color: #CBD5E1;
    }}

    /* Editorial Footer */
    .editorial-footer {{
        border-top: 2px solid var(--border);
        padding-top: 2rem;
        margin-top: 3.5rem;
    }}
    .footer-top-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }}
    .footer-brand-row {{
        display: flex;
        align-items: center;
        gap: 0.65rem;
    }}
    .footer-brand-title {{
        font-size: 1.15rem;
        font-weight: 900;
        color: var(--text-primary);
    }}
    .footer-sub {{
        font-size: 0.78rem;
        color: var(--text-muted);
        font-weight: 600;
    }}
    .footer-note {{
        font-size: 0.8rem;
        line-height: 1.6;
        color: var(--text-muted);
    }}

    /* Radio theme switcher widget styling */
    [data-testid="stRadio"] > div {{
        background-color: var(--surface) !important;
        border: 2px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 0.25rem 0.5rem !important;
        box-shadow: 0 3px 0 var(--shadow-color) !important;
    }}
    [data-testid="stRadio"] label span {{
        color: var(--text-primary) !important;
        font-weight: 800 !important;
        font-size: 0.85rem !important;
    }}
    </style>
    """


# ==============================================================================
# UI Component Renderers (Clean Design, No Emojis)
# ==============================================================================
def render_category_badge(category: str) -> str:
    """Generate high-contrast HTML category badge with explicit text and border."""
    cat = normalize_category(category)
    badge_cls = "cat-badge-dry"
    if cat == "Wet Waste":
        badge_cls = "cat-badge-wet"
    elif cat == "E-Waste":
        badge_cls = "cat-badge-ewaste"
    elif cat == "Hazardous Waste":
        badge_cls = "cat-badge-hazard"

    return f'<span class="cat-badge {badge_cls}">{cat}</span>'


def render_empty_state():
    """Render a clean editorial placeholder box before analysis is performed."""
    st.markdown(
        f"""
        <div style="text-align: center; padding: 3rem 1.5rem; border: 2px dashed var(--border); border-radius: 20px; background-color: var(--surface); margin: 1.5rem 0; box-shadow: 0 4px 0 var(--shadow-color);">
            <div style="margin-bottom: 0.85rem; color: var(--text-muted);">
                {icon("empty_inbox")}
            </div>
            <div style="font-size: 1.15rem; font-weight: 900; color: var(--text-primary); margin-bottom: 0.35rem; letter-spacing: -0.02em;">
                Ready for waste analysis
            </div>
            <div style="font-size: 0.9rem; color: var(--text-secondary); max-width: 440px; margin: 0 auto; line-height: 1.5;">
                Enter a waste item description or upload a photo to generate instant source segregation, environmental impact, and upcycling intelligence.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_text_results(res: WasteAnalysis, item_analyzed: str):
    """Render structured results for text analysis in alternating neo-brutalist cards."""
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # Result Header Bar
    badge_html = render_category_badge(res.primary_category)
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; padding: 1.1rem 1.4rem; background-color: var(--surface); border: 2px solid var(--border); border-radius: 18px; box-shadow: 0 5px 0 var(--shadow-color); margin-bottom: 1.25rem;">
            <div>
                <span class="section-meta-pill">Analyzed Item</span>
                <div style="font-size: 1.4rem; font-weight: 900; color: var(--text-primary); letter-spacing: -0.02em;">{item_analyzed}</div>
            </div>
            <div>
                {badge_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Safety Alert Banner if Hazardous Waste
    if res.primary_category == "Hazardous Waste":
        st.markdown(
            f"""
            <div class="hazard-safety-banner">
                <div style="color: var(--cat-hazard-fg); flex-shrink: 0; margin-top: 2px;">{icon("alert_triangle")}</div>
                <div>
                    <div class="hazard-banner-title">Hazardous Material Safety Protocol</div>
                    <div style="font-size: 0.9rem; line-height: 1.5;">
                        This material presents hazardous risks. Do not puncture, crush, or place in standard household waste. Route directly to authorized municipal toxic or e-waste drop-off points.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Alternating Card Architecture
    # Card B: Signature Lime (Recommended Action & Upcycling)
    st.markdown(
        f"""
        <div class="result-container-card result-card-b">
            <div class="result-title-row">
                {icon("check_circle")} <span>Recommended Action</span>
            </div>
            <div class="result-body-text" style="font-size: 1.05rem; font-weight: 700; margin-bottom: 1.25rem;">
                {res.disposal_action}
            </div>
            <div style="border-top: 2px solid var(--border); padding-top: 1rem; margin-top: 1rem;">
                <div style="font-size: 0.88rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.35rem; display: flex; align-items: center; gap: 0.4rem;">
                    {icon("refresh_cw")} Creative Upcycling & Circular Reuse
                </div>
                <div style="font-size: 0.92rem; font-weight: 600;">
                    {res.diy_upcycling_suggestion}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Card A: Carbon (Environmental Impact)
    st.markdown(
        f"""
        <div class="result-container-card result-card-a">
            <div class="result-title-row" style="color: var(--accent);">
                {icon("shield")} <span>Environmental Impact & Ecological Risk</span>
            </div>
            <div class="result-body-text" style="color: #E2E8F0;">
                {res.environmental_risk}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_vision_results(response: MultimodalWasteResponse):
    """Render structured human-readable results for multimodal vision analysis."""
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    is_discrete = response.scene_type == "DISCRETE_ITEMS"
    scene_label = "Discrete Items Detected" if is_discrete else "Trash Heap / Accumulation"
    conf_pct = int(round(response.confidence * 100))

    # Vision Status Header Bar
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; padding: 1.1rem 1.4rem; background-color: var(--surface); border: 2px solid var(--border); border-radius: 18px; box-shadow: 0 5px 0 var(--shadow-color); margin-bottom: 1.25rem;">
            <div>
                <span class="section-meta-pill">Scene Assessment</span>
                <div style="font-size: 1.35rem; font-weight: 900; color: var(--text-primary); letter-spacing: -0.02em;">{scene_label}</div>
            </div>
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="display: inline-block; padding: 0.35rem 0.8rem; background-color: var(--surface-lime); color: var(--text-on-lime); border: 1.5px solid var(--border); border-radius: 9999px; font-size: 0.82rem; font-weight: 800; box-shadow: 0 2px 0 var(--shadow-color);">
                    {conf_pct}% Confidence
                </span>
                <span style="display: inline-block; padding: 0.35rem 0.8rem; background-color: var(--surface-card-light); color: var(--text-secondary); border: 1.5px solid var(--border); border-radius: 9999px; font-size: 0.82rem; font-weight: 800; box-shadow: 0 2px 0 var(--shadow-color);">
                    {"Context Leveraged" if response.context_used else "Visual Evidence Only"}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Observations Expander
    if response.observations:
        with st.expander("Visual Observations", expanded=False):
            for obs in response.observations:
                st.markdown(f"- {obs}")

    # ==========================================================================
    # SCENE A: DISCRETE ITEMS
    # ==========================================================================
    if is_discrete:
        discrete_data = DiscreteAnalysis(**response.analysis)
        items = discrete_data.items

        if not items:
            st.info("No distinct waste items could be individually isolated in the image.")
            return

        st.markdown(f"#### Identified Waste Items ({len(items)})")

        for idx, item in enumerate(items):
            badge_html = render_category_badge(item.waste_category)

            with st.expander(f"Item {idx + 1}: {item.item_name} — {item.waste_category}", expanded=(idx == 0)):
                # Item Meta Strip
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem; padding: 0.75rem 1rem; background-color: var(--surface-card-light); border: 1.5px solid var(--border); border-radius: 12px; box-shadow: 0 3px 0 var(--shadow-color);">
                        <div>
                            <span style="font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Material Estimate:</span>
                            <strong style="color: var(--text-primary); margin-left: 0.35rem;">{item.material}</strong>
                        </div>
                        <div>
                            {badge_html}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Card B: Lime Recommended Action
                prep_html = ""
                if item.preparation_steps:
                    prep_items_html = "".join([f"<li style='margin-bottom: 0.3rem;'>{p}</li>" for p in item.preparation_steps])
                    prep_html = f"""
                    <div style="margin-top: 0.85rem; padding-top: 0.85rem; border-top: 1.5px solid var(--border);">
                        <strong style="font-size: 0.88rem; text-transform: uppercase; letter-spacing: 0.04em;">Preparation Checklist:</strong>
                        <ul style="margin: 0.4rem 0 0 1.2rem; font-size: 0.92rem; font-weight: 600;">{prep_items_html}</ul>
                    </div>
                    """

                st.markdown(
                    f"""
                    <div class="result-container-card result-card-b" style="margin-bottom: 1rem;">
                        <div class="result-title-row">
                            {icon("check_circle")} <span>Recommended Action</span>
                        </div>
                        <div class="result-body-text" style="font-size: 1.02rem; font-weight: 700;">
                            {item.disposal_action}
                        </div>
                        {prep_html}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Card A & Card C in two columns
                col_di1, col_di2 = st.columns(2)
                with col_di1:
                    st.markdown(
                        f"""
                        <div class="result-container-card result-card-a" style="margin-bottom: 0;">
                            <div class="result-title-row" style="color: var(--accent); font-size: 1.05rem;">
                                {icon("shield")} <span>Environmental Impact</span>
                            </div>
                            <div class="result-body-text" style="color: #E2E8F0; font-size: 0.9rem;">
                                {item.environmental_risk}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col_di2:
                    st.markdown(
                        f"""
                        <div class="result-container-card result-card-c" style="margin-bottom: 0;">
                            <div class="result-title-row" style="color: var(--text-primary); font-size: 1.05rem;">
                                {icon("refresh_cw")} <span>Upcycling & Reuse</span>
                            </div>
                            <div class="result-body-text" style="color: var(--text-secondary); font-size: 0.9rem; font-weight: 600;">
                                {item.upcycling_suggestion}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    # ==========================================================================
    # SCENE B: TRASH HEAP / SITE ASSESSMENT
    # ==========================================================================
    else:
        heap_data = TrashHeapAnalysis(**response.analysis)

        # Safety Banner
        st.markdown(
            f"""
            <div class="hazard-safety-banner">
                <div style="color: var(--cat-hazard-fg); flex-shrink: 0; margin-top: 2px;">{icon("alert_triangle")}</div>
                <div>
                    <div class="hazard-banner-title">Open Waste Accumulation Detected</div>
                    <div style="font-size: 0.9rem; line-height: 1.5;">
                        Hazardous or unsegregated open waste requires protective measures. Do not handle bare-handed. Avoid disturbing potential biohazards, chemicals, or broken glass.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        heap_tabs = st.tabs(
            [
                "Site Assessment",
                "Materials & Waste Types",
                "Safety & PPE",
                "Tools",
                "Cleanup Protocol",
                "Municipal Routing",
                "Environmental Risks",
            ]
        )

        with heap_tabs[0]:
            st.markdown("#### Site Assessment Overview")
            st.info(heap_data.site_assessment)
            if heap_data.dominant_materials:
                st.markdown("**Dominant Materials Observed:**")
                st.write(", ".join(heap_data.dominant_materials))

        with heap_tabs[1]:
            st.markdown("#### Waste Categories & Materials Present")
            if heap_data.waste_categories_present:
                st.markdown("**Identified Waste Categories:**")
                badge_list = " ".join([render_category_badge(c) for c in heap_data.waste_categories_present])
                st.markdown(f"<div style='margin-bottom: 0.75rem;'>{badge_list}</div>", unsafe_allow_html=True)
            if heap_data.dominant_materials:
                st.markdown("**Dominant Material Streams:**")
                for mat in heap_data.dominant_materials:
                    st.markdown(f"- {mat}")

        with heap_tabs[2]:
            st.markdown("#### Safety Measures & Recommended PPE")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.markdown("**Safety Guidelines:**")
                for measure in heap_data.safety_measures:
                    st.markdown(f"- {measure}")
            with col_s2:
                st.markdown("**Recommended PPE:**")
                for ppe in heap_data.recommended_ppe:
                    st.markdown(f"- {ppe}")

        with heap_tabs[3]:
            st.markdown("#### Required Tools & Equipment")
            for tool in heap_data.tools_required:
                st.markdown(f"- {tool}")

        with heap_tabs[4]:
            st.markdown("#### Cleanup Protocol Sequence")
            st.caption("Follow these numbered steps in sequence:")
            for idx, step in enumerate(heap_data.cleanup_protocol, 1):
                clean_step = step.lstrip("0123456789. ")
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: flex-start; gap: 0.8rem; margin-bottom: 0.6rem; background-color: var(--surface); border: 2px solid var(--border); border-radius: 12px; padding: 0.75rem 1rem; box-shadow: 0 3px 0 var(--shadow-color);">
                        <span style="display: inline-flex; align-items: center; justify-content: center; width: 26px; height: 26px; background-color: var(--surface-lime); color: var(--text-on-lime); border: 1.5px solid var(--border); border-radius: 6px; font-size: 0.82rem; font-weight: 900; flex-shrink: 0;">{idx}</span>
                        <span style="font-size: 0.94rem; font-weight: 600; color: var(--text-primary);">{clean_step}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with heap_tabs[5]:
            st.markdown("#### Municipal Coordination & Routing")
            st.write(heap_data.municipal_routing)

        with heap_tabs[6]:
            st.markdown("#### Environmental Hazards")
            for risk in heap_data.environmental_risks:
                st.markdown(f"- {risk}")


# ==============================================================================
# Streamlit Application Entrypoint
# ==============================================================================
def main():
    st.set_page_config(
        page_title="EcoSort AI",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Initialize theme in session state (default: Light)
    if "theme" not in st.session_state:
        st.session_state["theme"] = "Light"

    current_theme = st.session_state["theme"]

    # Inject dynamic design tokens and theme styles
    st.markdown(get_theme_css(current_theme), unsafe_allow_html=True)

    # ==========================================================================
    # Editorial Brand Navigation Header
    # ==========================================================================
    col_nav_brand, col_nav_theme = st.columns([4, 1.2])
    with col_nav_brand:
        st.markdown(
            f"""
            <div class="editorial-nav" style="border-bottom: none; margin-bottom: 0; padding-bottom: 0;">
                <div class="brand-group">
                    <div class="brand-mark">
                        {icon("logo")}
                    </div>
                    <div>
                        <div class="brand-title">EcoSort AI</div>
                        <div class="brand-descriptor">AI-Powered Waste Intelligence</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_nav_theme:
        selected_theme = st.radio(
            label="Theme Selection",
            options=["Light", "Dark"],
            index=0 if current_theme == "Light" else 1,
            horizontal=True,
            key="theme_switcher_widget",
            label_visibility="collapsed",
        )
        if selected_theme != current_theme:
            st.session_state["theme"] = selected_theme
            st.rerun()

    st.markdown("<div style='border-bottom: 2px solid var(--border); margin: 0.75rem 0 2rem 0;'></div>", unsafe_allow_html=True)

    # ==========================================================================
    # Asymmetric 2-Column Desktop Hero Section
    # ==========================================================================
    col_hero_text, col_hero_art = st.columns([1.15, 0.85], gap="large")
    with col_hero_text:
        st.markdown(
            f"""
            <div class="hero-container">
                <div class="hero-pill">
                    {icon("globe")} UN SDG 12 • RESPONSIBLE PRODUCTION & CONSUMPTION
                </div>
                <h1 class="hero-headline">
                    Make every piece of <span class="highlight-lime">waste count.</span>
                </h1>
                <p class="hero-subhead">
                    Harness Google Gemini AI to analyze household & campus waste, prevent landfill contamination, and turn everyday discards into valuable circular resources.
                </p>
                <div class="hero-cta-row">
                    <a href="#workspace" class="hero-cta-primary">
                        Start Waste Analysis {icon("arrow_right")}
                    </a>
                    <a href="#how-it-works" class="hero-cta-secondary">
                        How It Works
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_hero_art:
        # Render the SVG using st.markdown with unsafe_allow_html=True (single unindented string prevents code block interpretation)
        svg_html = get_hero_vector_illustration(current_theme)
        st.markdown(svg_html, unsafe_allow_html=True)

    # ==========================================================================
    # Product Capabilities Strip
    # ==========================================================================
    st.markdown(
        f"""
        <div class="capabilities-strip">
            <div class="cap-item">{icon("sparkles")} Multimodal Vision</div>
            <div class="cap-divider">•</div>
            <div class="cap-item">{icon("file_text")} Natural Language Analysis</div>
            <div class="cap-divider">•</div>
            <div class="cap-item">{icon("trash")} 4-Stream Sorting</div>
            <div class="cap-divider">•</div>
            <div class="cap-item">{icon("shield")} Safety & Hazard Detection</div>
            <div class="cap-divider">•</div>
            <div class="cap-item">{icon("refresh_cw")} DIY Circular Upcycling</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ==========================================================================
    # "How EcoSort AI Works" (01-04 Alternating Cards)
    # ==========================================================================
    st.markdown(
        """
        <div class="eco-section-header" id="how-it-works">
            <span class="section-meta-pill">Process Architecture</span>
            <div class="section-main-title">How EcoSort AI works</div>
            <div class="section-desc">A straightforward four-step pipeline from discarded item to verified circular recovery.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        st.markdown(
            """
            <div class="process-card card-white">
                <div>
                    <div class="card-num-tag">01</div>
                    <div class="card-header-title">Describe</div>
                </div>
                <div class="card-body-text">
                    Type any item, food scrap, or package description into the natural language prompt.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_p2:
        st.markdown(
            """
            <div class="process-card card-lime">
                <div>
                    <div class="card-num-tag">02</div>
                    <div class="card-header-title">Show</div>
                </div>
                <div class="card-body-text">
                    Upload an image or take a live camera snapshot of single objects or complex piles.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_p3:
        st.markdown(
            """
            <div class="process-card card-carbon">
                <div>
                    <div class="card-num-tag">03</div>
                    <div class="card-header-title">Analyze</div>
                </div>
                <div class="card-body-text">
                    Gemini multimodal intelligence classifies materials and detects environmental risks.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_p4:
        st.markdown(
            """
            <div class="process-card card-light">
                <div>
                    <div class="card-num-tag">04</div>
                    <div class="card-header-title">Act</div>
                </div>
                <div class="card-body-text">
                    Receive verified municipal disposal steps, safety protocols, and creative upcycling options.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-top: 3.5rem;'></div>", unsafe_allow_html=True)

    # Retrieve API key
    api_key = get_gemini_api_key()

    # Sidebar settings
    with st.sidebar:
        st.header("Configuration")
        st.markdown("Configure your Google Gemini API credentials for waste classification.")

        if not api_key:
            st.warning("No Gemini API key detected.")
            sidebar_key = st.text_input(
                "Gemini API Key (Temporary):",
                type="password",
                key="sidebar_api_key",
                help="Get your key from Google AI Studio (https://aistudio.google.com/)",
            )
            if sidebar_key:
                api_key = sidebar_key.strip()
                st.success("API key loaded for this session.")
        else:
            st.success("Gemini API Key configured")

        st.markdown("---")
        st.markdown("**Waste Categories:**")
        st.markdown(f"- {render_category_badge('Wet Waste')}: Food, peelings, organics", unsafe_allow_html=True)
        st.markdown(f"- {render_category_badge('Dry Waste')}: Paper, plastics, metals, glass", unsafe_allow_html=True)
        st.markdown(f"- {render_category_badge('E-Waste')}: Electronics, cables, chargers", unsafe_allow_html=True)
        st.markdown(f"- {render_category_badge('Hazardous Waste')}: Batteries, chemicals, medical", unsafe_allow_html=True)

    if not api_key:
        st.warning(
            """
            **Gemini API Key Required**
            The Gemini API key is not configured. Please set `GEMINI_API_KEY` in a `.env` file, in `.streamlit/secrets.toml`, or enter it directly in the sidebar on the left.
            """
        )

    # ==========================================================================
    # Interactive Analysis Workspace ("Let's sort it.")
    # ==========================================================================
    st.markdown(
        """
        <div class="eco-section-header" id="workspace">
            <span class="section-meta-pill">Interactive Workspace</span>
            <div class="section-main-title">Let's sort it.</div>
            <div class="section-desc">Choose text description or visual image input to classify your waste responsibly.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_text, tab_vision = st.tabs(["Text Analysis", "Visual Analysis"])

    # --------------------------------------------------------------------------
    # TAB 1: TEXT ANALYSIS
    # --------------------------------------------------------------------------
    with tab_text:
        if "waste_input" not in st.session_state:
            st.session_state["waste_input"] = ""

        st.markdown("<span style='font-size: 0.85rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em;'>Quick Examples:</span>", unsafe_allow_html=True)
        example_items = [
            "Banana peel",
            "Plastic bottle",
            "Old smartphone",
            "Used battery",
            "Cardboard box",
            "Old clothes",
            "Aluminum can",
            "Glass bottle",
        ]

        col_chips = st.columns(4)
        for idx, item_value in enumerate(example_items):
            col = col_chips[idx % 4]
            if col.button(item_value, key=f"chip_btn_{idx}", use_container_width=True):
                st.session_state["waste_input"] = item_value
                st.rerun()

        st.markdown("<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True)

        user_waste_input = st.text_area(
            label="Waste item description:",
            value=st.session_state["waste_input"],
            placeholder="Example: Old smartphone battery or plastic takeout container...",
            height=95,
            key="waste_text_input",
            label_visibility="collapsed",
        )

        col_act, col_clr = st.columns([3, 1])
        with col_act:
            analyze_clicked = st.button("Analyze Waste", type="primary", use_container_width=True)
        with col_clr:
            if st.button("Clear", key="btn_clear_text", type="secondary", use_container_width=True):
                st.session_state["waste_input"] = ""
                st.session_state.pop("last_analysis", None)
                st.rerun()

        if analyze_clicked:
            cleaned_input = user_waste_input.strip()
            if not cleaned_input:
                st.warning("Please enter a waste item to analyze.")
            elif not api_key:
                st.error("Gemini API key is missing. Please configure an API key to run analysis.")
            else:
                with st.spinner("Analyzing waste item..."):
                    try:
                        analysis = analyze_waste_with_gemini(cleaned_input, api_key)
                        st.session_state["last_analysis"] = analysis
                        st.session_state["last_item"] = cleaned_input
                    except Exception as e:
                        err_str = str(e)
                        if "API_KEY_INVALID" in err_str or "api key not valid" in err_str.lower():
                            st.error("Your Gemini API key appears invalid or expired.")
                        elif "RESOURCE_EXHAUSTED" in err_str or "quota" in err_str.lower():
                            st.error("API rate limit or quota reached. Please wait a moment.")
                        elif "connect" in err_str.lower():
                            st.error("Network issue. Please check your connection.")
                        else:
                            st.error("We couldn't complete the analysis right now. Please try again.")

        if "last_analysis" in st.session_state and st.session_state["last_analysis"]:
            render_text_results(
                st.session_state["last_analysis"],
                st.session_state.get("last_item", "Item"),
            )
        else:
            render_empty_state()

    # --------------------------------------------------------------------------
    # TAB 2: VISUAL ANALYSIS
    # --------------------------------------------------------------------------
    with tab_vision:
        st.markdown(
            f"""
            <div style="display: flex; gap: 1.5rem; margin-bottom: 1.25rem; flex-wrap: wrap;">
                <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; font-weight: 800; color: var(--text-primary);">
                    <span style="display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; background-color: var(--surface-lime); color: var(--text-on-lime); border: 1.5px solid var(--border); border-radius: 6px; font-size: 0.78rem; font-weight: 900;">01</span> Add an image
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; font-weight: 800; color: var(--text-primary);">
                    <span style="display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; background-color: var(--surface-lime); color: var(--text-on-lime); border: 1.5px solid var(--border); border-radius: 6px; font-size: 0.78rem; font-weight: 900;">02</span> Add context
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; font-weight: 800; color: var(--text-primary);">
                    <span style="display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; background-color: var(--surface-lime); color: var(--text-on-lime); border: 1.5px solid var(--border); border-radius: 6px; font-size: 0.78rem; font-weight: 900;">03</span> Analyze
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_src1, col_src2 = st.columns(2)
        with col_src1:
            st.markdown(
                f"<div style='font-size: 0.9rem; font-weight: 800; color: var(--text-primary); margin-bottom: 0.4rem; display: flex; align-items: center; gap: 0.4rem;'>{icon('upload')} Upload an image</div>",
                unsafe_allow_html=True,
            )
            uploaded_img_file = st.file_uploader(
                "Upload an image",
                type=["jpg", "jpeg", "png", "webp"],
                key="vision_uploader",
                label_visibility="collapsed",
            )
        with col_src2:
            st.markdown(
                f"<div style='font-size: 0.9rem; font-weight: 800; color: var(--text-primary); margin-bottom: 0.4rem; display: flex; align-items: center; gap: 0.4rem;'>{icon('camera')} Use camera</div>",
                unsafe_allow_html=True,
            )
            camera_img_file = st.camera_input("Use camera", key="vision_camera", label_visibility="collapsed")
            # Clear application-level helper for camera permissions
            st.markdown(
                f"""
                <div style="display: flex; align-items: flex-start; gap: 0.5rem; background-color: var(--surface-card-light); border: 1.5px solid var(--border); border-radius: 12px; padding: 0.65rem 0.85rem; margin-top: 0.65rem; box-shadow: 0 2px 0 var(--shadow-color);">
                    <div style="color: var(--text-muted); flex-shrink: 0; margin-top: 1px;">{icon("info")}</div>
                    <div style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4;">
                        <strong style="color: var(--text-primary);">Camera access:</strong> If camera access is unavailable, allow camera permissions in your browser address bar, or use the <strong>Upload an image</strong> tab.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if uploaded_img_file is not None and camera_img_file is not None:
            st.info("Both file upload and camera capture detected. Using uploaded file as primary image.")

        loaded_image, img_error, _ = load_and_validate_image(uploaded_img_file, camera_img_file)

        if img_error:
            st.error(f"{img_error}")
        elif loaded_image is not None:
            col_vprev, col_vctx = st.columns([1, 1.2])
            with col_vprev:
                st.markdown(
                    f"""
                    <div style="background-color: var(--surface); border: 2px solid var(--border); border-radius: 18px; padding: 0.85rem; text-align: center; margin-bottom: 0.75rem; box-shadow: 0 4px 0 var(--shadow-color);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; font-size: 0.82rem; font-weight: 800;">
                            <span style="color: var(--text-primary);">{icon('check_circle')} Ready for analysis</span>
                            <span style="color: var(--text-muted);">{loaded_image.size[0]}×{loaded_image.size[1]}px</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.image(loaded_image, width=380)

            with col_vctx:
                st.markdown("<span style='font-size: 0.9rem; font-weight: 800; color: var(--text-primary);'>Additional Context (Optional):</span>", unsafe_allow_html=True)
                optional_context = st.text_area(
                    "Additional Context",
                    placeholder="Example: Found behind chemistry laboratory, near campus dining hall, single item on desk...",
                    height=130,
                    key="vision_context_input",
                    label_visibility="collapsed",
                    help="Visual evidence takes precedence over context.",
                )

            col_vact, col_vclr = st.columns([3, 1])
            with col_vact:
                analyze_vision_clicked = st.button(
                    "Analyze Waste",
                    type="primary",
                    use_container_width=True,
                    key="btn_analyze_vision",
                )
            with col_vclr:
                if st.button("Clear", use_container_width=True, key="btn_clear_vision", type="secondary"):
                    st.session_state.pop("last_vision_analysis", None)
                    st.rerun()

            if analyze_vision_clicked:
                if not api_key:
                    st.error("Gemini API key is missing. Please configure an API key to run analysis.")
                else:
                    with st.spinner("Analyzing waste scene with Gemini Vision..."):
                        try:
                            vision_res = analyze_multimodal_waste_with_gemini(
                                loaded_image, optional_context, api_key
                            )
                            st.session_state["last_vision_analysis"] = vision_res
                        except Exception as e:
                            err_str = str(e)
                            if "API_KEY_INVALID" in err_str or "api key not valid" in err_str.lower():
                                st.error("Your Gemini API key appears invalid or expired.")
                            elif "RESOURCE_EXHAUSTED" in err_str or "quota" in err_str.lower():
                                st.error("API rate limit or quota reached. Please wait a moment.")
                            elif "connect" in err_str.lower():
                                st.error("Network issue. Please check your connection.")
                            else:
                                st.error("We couldn't complete the analysis right now. Please try again.")

        if "last_vision_analysis" in st.session_state and st.session_state["last_vision_analysis"]:
            render_vision_results(st.session_state["last_vision_analysis"])
        elif loaded_image is None and not img_error:
            render_empty_state()

    # ==========================================================================
    # Process & FAQ Accordion Section
    # ==========================================================================
    st.markdown(
        """
        <div class="eco-section-header" id="faq" style="margin-top: 3.5rem;">
            <span class="section-meta-pill">Knowledge & Operations</span>
            <div class="section-main-title">Waste sorting intelligence</div>
            <div class="section-desc">Essential guidelines for source segregation, e-waste hazards, and municipal worker safety.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("01 / Why is source segregation fundamental to circular recycling?"):
        st.markdown(
            """
            When wet and dry waste mix, moisture and organic decomposing materials contaminate recyclable paper,
            cardboard, plastics, and metals. Contaminated dry waste loses up to 90% of its economic recycling value
            and is ultimately dumped into landfills, where it generates methane gas. Source segregation guarantees
            high-purity waste streams that can be efficiently processed into new products.
            """
        )

    with st.expander("02 / What makes electronic waste (E-Waste) uniquely dangerous if landfilled?"):
        st.markdown(
            """
            Electronics contain heavy metals including lead, cadmium, mercury, and flame retardants.
            When left in open heaps or crushed in landfills, rainwater dissolves these toxins into dangerous leachate,
            permanently polluting groundwater reserves and agricultural soil. Dedicated e-waste recycling enables
            the recovery of precious elements (copper, gold, lithium) while isolating dangerous contaminants.
            """
        )

    with st.expander("03 / How does proper hazardous waste disposal protect municipal sanitation workers?"):
        st.markdown(
            """
            Unsegregated hazardous waste—such as spent lithium-ion batteries, broken chemical containers, needles,
            and fluorescent lamps—creates severe occupational hazards including chemical burns, puncture wounds,
            and explosive battery fires in collection trucks. Disposing of hazards through specialized municipal
            channels directly shields frontline workers.
            """
        )

    with st.expander("04 / How does EcoSort AI contribute to UN Sustainable Development Goal 12?"):
        st.markdown(
            """
            EcoSort AI directly advances **UN SDG Target 12.5**: *'By 2030, substantially reduce waste generation
            through prevention, reduction, recycling and reuse.'* By empowering individuals with accurate visual
            and text intelligence at the moment of disposal, EcoSort AI converts confusion into responsible habits.
            """
        )

    # ==========================================================================
    # High-Impact SDG 12 Mission Panel
    # ==========================================================================
    st.markdown(
        """
        <div class="mission-panel" id="sdg12">
            <div class="mission-pill">UN SDG 12 • TARGET 12.5</div>
            <div class="mission-title">Designed for a more circular future.</div>
            <div class="mission-desc">
                Sustainable Consumption and Production is not just an ideal—it is an operational necessity.
                EcoSort AI bridges the gap between consumer intentions and verified circular recovery by offering
                instant, verified sorting decisions right where waste is generated.
            </div>
            <div class="mission-stat-grid">
                <div class="mission-stat-box">
                    <div class="stat-number">12.5</div>
                    <div class="stat-label">UN SDG Target Focus</div>
                </div>
                <div class="mission-stat-box">
                    <div class="stat-number">4 Streams</div>
                    <div class="stat-label">Source Segregation</div>
                </div>
                <div class="mission-stat-box">
                    <div class="stat-number">100%</div>
                    <div class="stat-label">Circular Reuse Focus</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ==========================================================================
    # Editorial Footer
    # ==========================================================================
    st.markdown(
        f"""
        <div class="editorial-footer">
            <div class="footer-top-row">
                <div class="footer-brand-row">
                    <div style="color: var(--accent); display: inline-flex; align-items: center; justify-content: center; width: 32px; height: 32px; background: var(--surface-carbon); border-radius: 8px; border: 1.5px solid var(--border);">
                        {icon("logo")}
                    </div>
                    <div>
                        <div class="footer-brand-title">EcoSort AI</div>
                        <div class="footer-sub">AI for Responsible Consumption & Production</div>
                    </div>
                </div>
                <div style="font-size: 0.85rem; font-weight: 700; color: var(--text-secondary);">
                    1M1B AI for Sustainability Internship
                </div>
            </div>
            <div class="footer-note">
                EcoSort AI provides sustainability guidance based on user inputs and image analysis. It cannot guarantee exact material chemistry or replace municipal sanitation ordinances. For hazardous or unknown materials, always consult your local waste authority.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
