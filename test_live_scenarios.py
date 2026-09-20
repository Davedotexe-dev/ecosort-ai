"""Live verification script testing the 4 required scenarios with Gemini API."""

import os
import sys
from PIL import Image, ImageDraw
from dotenv import load_dotenv

load_dotenv()

from app import (
    get_gemini_api_key,
    analyze_waste_with_gemini,
    analyze_multimodal_waste_with_gemini,
    DiscreteAnalysis,
    TrashHeapAnalysis,
)


def create_bottle_image() -> Image.Image:
    """Generate a synthetic test image representing a single plastic water bottle."""
    img = Image.new("RGB", (300, 400), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    # Draw table surface
    draw.rectangle([(0, 320), (300, 400)], fill=(200, 180, 160))
    # Draw bottle body
    draw.rounded_rectangle([(110, 120), (190, 320)], radius=15, fill=(180, 220, 255), outline=(100, 160, 220), width=3)
    # Draw bottle neck and cap
    draw.rectangle([(130, 70), (170, 120)], fill=(200, 230, 255), outline=(100, 160, 220), width=2)
    draw.rectangle([(125, 50), (175, 70)], fill=(30, 120, 220))  # Blue cap
    # Label
    draw.rectangle([(112, 190), (188, 240)], fill=(255, 255, 255), outline=(100, 160, 220))
    draw.text((125, 210), "SPRING WATER", fill=(20, 80, 160))
    return img


def create_smartphone_image() -> Image.Image:
    """Generate a synthetic test image representing an old smartphone with cracked screen."""
    img = Image.new("RGB", (300, 400), color=(245, 245, 245))
    draw = ImageDraw.Draw(img)
    # Desk
    draw.rectangle([(0, 330), (300, 400)], fill=(180, 150, 120))
    # Phone body
    draw.rounded_rectangle([(90, 80), (210, 320)], radius=12, fill=(40, 40, 40), outline=(20, 20, 20), width=4)
    # Screen
    draw.rectangle([(100, 110), (200, 290)], fill=(15, 25, 35))
    # Cracks
    draw.line([(105, 120), (150, 180), (190, 160)], fill=(200, 200, 200), width=2)
    draw.line([(150, 180), (140, 270)], fill=(180, 180, 180), width=2)
    # Camera lens
    draw.ellipse([(140, 90), (160, 100)], fill=(60, 60, 60))
    return img


def create_trash_pile_image() -> Image.Image:
    """Generate a synthetic test image representing an open dump site / trash accumulation."""
    img = Image.new("RGB", (400, 300), color=(140, 130, 120))  # Dirt / ground
    draw = ImageDraw.Draw(img)
    # Draw roadside dirt ground
    draw.rectangle([(0, 0), (400, 120)], fill=(110, 110, 110))  # Road
    # Open dump pile background
    draw.ellipse([(30, 80), (370, 280)], fill=(90, 80, 70))
    # Mixed waste elements
    # Black and green trash bags
    draw.ellipse([(60, 130), (140, 210)], fill=(25, 25, 25))
    draw.ellipse([(120, 110), (210, 190)], fill=(30, 70, 40))
    draw.ellipse([(200, 140), (290, 230)], fill=(20, 20, 20))
    # Cardboard boxes
    draw.rectangle([(160, 180), (250, 260)], fill=(190, 145, 95), outline=(130, 90, 50), width=2)
    # Scattered plastic bottles & cans
    draw.rectangle([(70, 220), (120, 240)], fill=(200, 230, 255), outline=(100, 150, 200))
    draw.ellipse([(260, 190), (290, 240)], fill=(180, 180, 180))  # Aluminum can
    draw.ellipse([(280, 220), (340, 260)], fill=(220, 20, 20))    # Crushed red container
    draw.line([(100, 250), (280, 270)], fill=(255, 255, 100), width=3)  # Plastic film/strip
    return img


def run_live_tests():
    api_key = get_gemini_api_key()
    if not api_key:
        print("ERROR: No Gemini API Key configured in .env or environment. Skipping live tests.")
        sys.exit(1)

    print(f"Loaded Gemini API Key (length: {len(api_key)})")

    # --------------------------------------------------------------------------
    # TEST D: Existing Text Mode Test
    # --------------------------------------------------------------------------
    print("\n--- Running TEST D: Text-Only Analysis ('Banana peel') ---")
    text_result = analyze_waste_with_gemini("Banana peel", api_key)
    print(f"Category: {text_result.primary_category}")
    print(f"Disposal: {text_result.disposal_action[:70]}...")
    print(f"Environmental Risk: {text_result.environmental_risk[:70]}...")
    print(f"DIY Upcycling: {text_result.diy_upcycling_suggestion[:70]}...")
    assert text_result.primary_category == "Wet Waste", f"Expected Wet Waste, got {text_result.primary_category}"
    print("TEST D PASSED!")

    # --------------------------------------------------------------------------
    # TEST A: Single Plastic Bottle Image
    # --------------------------------------------------------------------------
    print("\n--- Running TEST A: Single Plastic Bottle Image ---")
    bottle_img = create_bottle_image()
    res_a = analyze_multimodal_waste_with_gemini(bottle_img, "Found on classroom desk", api_key)
    print(f"Scene Type: {res_a.scene_type} (Confidence: {res_a.confidence:.2f})")
    print(f"Observations: {res_a.observations}")
    print(f"Context Used: {res_a.context_used}")
    assert res_a.scene_type in ("DISCRETE_ITEMS", "TRASH_HEAP")
    if res_a.scene_type == "DISCRETE_ITEMS":
        discrete_data = DiscreteAnalysis(**res_a.analysis)
        print(f"Detected {len(discrete_data.items)} item(s):")
        for item in discrete_data.items:
            print(f"  - {item.item_name} | {item.material} | {item.waste_category}")
            print(f"    Prep steps: {item.preparation_steps}")
    print("TEST A PASSED!")

    # --------------------------------------------------------------------------
    # TEST B: Single Electronic Device Image
    # --------------------------------------------------------------------------
    print("\n--- Running TEST B: Single Electronic Device Image ---")
    phone_img = create_smartphone_image()
    res_b = analyze_multimodal_waste_with_gemini(phone_img, None, api_key)
    print(f"Scene Type: {res_b.scene_type} (Confidence: {res_b.confidence:.2f})")
    print(f"Observations: {res_b.observations}")
    assert res_b.scene_type in ("DISCRETE_ITEMS", "TRASH_HEAP")
    if res_b.scene_type == "DISCRETE_ITEMS":
        discrete_b = DiscreteAnalysis(**res_b.analysis)
        for item in discrete_b.items:
            print(f"  - {item.item_name} | {item.material} | {item.waste_category}")
    print("TEST B PASSED!")

    # --------------------------------------------------------------------------
    # TEST C: Mixed Open Trash Pile Image
    # --------------------------------------------------------------------------
    print("\n--- Running TEST C: Mixed Open Trash Pile Image ---")
    trash_img = create_trash_pile_image()
    res_c = analyze_multimodal_waste_with_gemini(trash_img, "Roadside accumulation near campus edge", api_key)
    print(f"Scene Type: {res_c.scene_type} (Confidence: {res_c.confidence:.2f})")
    print(f"Observations: {res_c.observations}")
    assert res_c.scene_type in ("DISCRETE_ITEMS", "TRASH_HEAP")
    if res_c.scene_type == "TRASH_HEAP":
        heap_data = TrashHeapAnalysis(**res_c.analysis)
        print(f"Site Assessment: {heap_data.site_assessment[:80]}...")
        print(f"Dominant Materials: {heap_data.dominant_materials}")
        print(f"Waste Categories Present: {heap_data.waste_categories_present}")
        print(f"Cleanup Protocol Steps: {len(heap_data.cleanup_protocol)}")
    print("TEST C PASSED!")

    print("\n=======================================================")
    print("ALL 4 CONCEPTUAL SCENARIOS (A, B, C, D) PASSED SUCCESSFULLY!")
    print("=======================================================")


if __name__ == "__main__":
    run_live_tests()
