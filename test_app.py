"""Unit and Integration Tests for EcoSort AI Core Logic and Multimodal Vision."""

import io
import unittest
from PIL import Image
from pydantic import ValidationError

from app import (
    ALLOWED_CATEGORIES,
    SUPPORTED_IMAGE_FORMATS,
    DiscreteAnalysis,
    DiscreteItem,
    MultimodalWasteResponse,
    TrashHeapAnalysis,
    WasteAnalysis,
    load_and_validate_image,
    normalize_category,
)


class MockFile:
    """Mock file object simulating Streamlit UploadedFile."""

    def __init__(self, data: bytes, name: str = "test.jpg"):
        self._data = data
        self.name = name

    def getvalue(self) -> bytes:
        return self._data


class TestEcoSortAI(unittest.TestCase):
    # --------------------------------------------------------------------------
    # Categories & Normalization
    # --------------------------------------------------------------------------
    def test_allowed_categories(self):
        self.assertEqual(len(ALLOWED_CATEGORIES), 4)
        self.assertIn("Wet Waste", ALLOWED_CATEGORIES)
        self.assertIn("Dry Waste", ALLOWED_CATEGORIES)
        self.assertIn("E-Waste", ALLOWED_CATEGORIES)
        self.assertIn("Hazardous Waste", ALLOWED_CATEGORIES)

    def test_normalize_category(self):
        self.assertEqual(normalize_category("Wet Waste"), "Wet Waste")
        self.assertEqual(normalize_category("wet"), "Wet Waste")
        self.assertEqual(normalize_category("organic compost"), "Wet Waste")
        self.assertEqual(normalize_category("food scraps"), "Wet Waste")

        self.assertEqual(normalize_category("Dry Waste"), "Dry Waste")
        self.assertEqual(normalize_category("plastic"), "Dry Waste")
        self.assertEqual(normalize_category("recyclable paper"), "Dry Waste")

        self.assertEqual(normalize_category("E-Waste"), "E-Waste")
        self.assertEqual(normalize_category("electronic waste"), "E-Waste")
        self.assertEqual(normalize_category("ewaste"), "E-Waste")

        self.assertEqual(normalize_category("Hazardous Waste"), "Hazardous Waste")
        self.assertEqual(normalize_category("toxic battery"), "Hazardous Waste")
        self.assertEqual(normalize_category("chemical hazard"), "Hazardous Waste")

    # --------------------------------------------------------------------------
    # Text Analysis Schema
    # --------------------------------------------------------------------------
    def test_waste_analysis_schema_valid(self):
        data = {
            "primary_category": "Wet Waste",
            "disposal_action": "Compost in a green bin or backyard composter.",
            "environmental_risk": "Emits methane in landfills under anaerobic decomposition.",
            "diy_upcycling_suggestion": "Use banana peel as nutrient-rich plant fertilizer.",
        }
        analysis = WasteAnalysis(**data)
        self.assertEqual(analysis.primary_category, "Wet Waste")
        self.assertIn("Compost", analysis.disposal_action)
        self.assertIn("methane", analysis.environmental_risk)
        self.assertIn("fertilizer", analysis.diy_upcycling_suggestion)

    def test_waste_analysis_schema_missing_field(self):
        incomplete_data = {
            "primary_category": "Dry Waste",
            "disposal_action": "Rinse and place in blue bin.",
        }
        with self.assertRaises(ValidationError):
            WasteAnalysis(**incomplete_data)

    # --------------------------------------------------------------------------
    # Discrete Items Schema
    # --------------------------------------------------------------------------
    def test_discrete_item_schema_valid(self):
        item_data = {
            "item_name": "Plastic Water Bottle",
            "material": "PET plastic",
            "waste_category": "Dry Waste",
            "disposal_action": "Empty, rinse, and place in dry recyclables.",
            "preparation_steps": ["Empty contents", "Crush to save volume"],
            "environmental_risk": "Takes up to 450 years to decompose into microplastics.",
            "upcycling_suggestion": "Cut into a seedling starter or watering funnel.",
        }
        item = DiscreteItem(**item_data)
        self.assertEqual(item.item_name, "Plastic Water Bottle")
        self.assertEqual(item.waste_category, "Dry Waste")
        self.assertEqual(len(item.preparation_steps), 2)

        discrete_analysis = DiscreteAnalysis(items=[item])
        self.assertEqual(len(discrete_analysis.items), 1)

    # --------------------------------------------------------------------------
    # Trash Heap Schema
    # --------------------------------------------------------------------------
    def test_trash_heap_schema_valid(self):
        heap_data = {
            "site_assessment": "Unregulated open accumulation of municipal solid waste.",
            "dominant_materials": ["Plastic bags", "Packaging cardboard", "Discarded textiles"],
            "waste_categories_present": ["Dry Waste", "Wet Waste"],
            "environmental_risks": ["Leachate contamination to surrounding groundwater"],
            "safety_measures": ["Maintain safe perimeter", "Do not handle bare-handed"],
            "recommended_ppe": ["Puncture-resistant work gloves", "Closed-toe work boots"],
            "tools_required": ["Heavy-duty garbage sacks", "Litter tongs / grabbers"],
            "cleanup_protocol": [
                "1. Establish a safe perimeter.",
                "2. Equip all personnel with recommended PPE.",
                "3. Remove dry recyclables into blue bags.",
                "4. Coordinate pickup with municipal sanitation.",
            ],
            "municipal_routing": "Coordinate with municipal waste authority for commercial roll-off container transport.",
        }
        heap = TrashHeapAnalysis(**heap_data)
        self.assertEqual(heap.waste_categories_present, ["Dry Waste", "Wet Waste"])
        self.assertEqual(len(heap.cleanup_protocol), 4)

    # --------------------------------------------------------------------------
    # Top-Level Multimodal Response Schema
    # --------------------------------------------------------------------------
    def test_multimodal_response_schema(self):
        response_data = {
            "scene_type": "DISCRETE_ITEMS",
            "confidence": 0.94,
            "observations": ["Single clear plastic drink bottle on desktop surface"],
            "context_used": False,
            "analysis": {
                "items": [
                    {
                        "item_name": "Clear Bottle",
                        "material": "PET plastic",
                        "waste_category": "Dry Waste",
                        "disposal_action": "Recycle in dry bin",
                        "preparation_steps": ["Rinse"],
                        "environmental_risk": "Microplastic pollution",
                        "upcycling_suggestion": "Planter",
                    }
                ]
            },
        }
        res = MultimodalWasteResponse(**response_data)
        self.assertEqual(res.scene_type, "DISCRETE_ITEMS")
        self.assertAlmostEqual(res.confidence, 0.94)
        self.assertFalse(res.context_used)

    # --------------------------------------------------------------------------
    # Image Loading & Validation
    # --------------------------------------------------------------------------
    def test_load_and_validate_image_valid_jpeg(self):
        img = Image.new("RGB", (100, 100), color="blue")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        mock_file = MockFile(buf.getvalue(), "bottle.jpg")

        loaded_img, err, src = load_and_validate_image(mock_file, None)
        self.assertIsNone(err)
        self.assertIsNotNone(loaded_img)
        self.assertEqual(src, "upload")
        self.assertEqual(loaded_img.size, (100, 100))

    def test_load_and_validate_image_priority(self):
        img1 = Image.new("RGB", (50, 50), color="green")
        buf1 = io.BytesIO()
        img1.save(buf1, format="PNG")
        file1 = MockFile(buf1.getvalue(), "upload.png")

        img2 = Image.new("RGB", (20, 20), color="red")
        buf2 = io.BytesIO()
        img2.save(buf2, format="PNG")
        file2 = MockFile(buf2.getvalue(), "camera.png")

        loaded_img, err, src = load_and_validate_image(file1, file2)
        self.assertIsNone(err)
        self.assertEqual(src, "upload")
        self.assertEqual(loaded_img.size, (50, 50))  # Uploaded file prioritized!

    def test_load_and_validate_image_corrupted(self):
        corrupted_bytes = b"this is completely corrupted not an image"
        mock_file = MockFile(corrupted_bytes, "corrupt.jpg")

        loaded_img, err, src = load_and_validate_image(mock_file, None)
        self.assertIsNone(loaded_img)
        self.assertIsNotNone(err)
        self.assertIn("couldn't read this image", err.lower())

    def test_load_and_validate_image_empty(self):
        mock_file = MockFile(b"", "empty.jpg")
        loaded_img, err, src = load_and_validate_image(mock_file, None)
        self.assertIsNone(loaded_img)
        self.assertIn("empty", err)


if __name__ == "__main__":
    unittest.main()
