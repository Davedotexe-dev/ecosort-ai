<<<<<<< HEAD
# EcoSort AI
### AI-Powered Waste Intelligence for a Sustainable Future

[![Streamlit](https://img.shields.io/badge/Streamlit-1.38%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-google--genai-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![UN SDG 12](https://img.shields.io/badge/UN%20SDG-12%3A%20Responsible%20Consumption-059669)](https://sdgs.un.org/goals/goal12)
[![Internship](https://img.shields.io/badge/1M1B-AI%20for%20Sustainability-10b981)](https://www.1m1b.org/)

---

## Overview

**EcoSort AI** is an intelligent household and campus waste classification web application developed as part of the **1M1B AI for Sustainability Internship**. Powered by **Google Gemini** using the modern `google-genai` Python SDK and built on **Streamlit**, EcoSort AI empowers students, households, and campuses to practice responsible consumption and proper waste management.

The application features a professional SaaS-grade design token system supporting both **Light Mode** and **Dark Mode**, **zero emoji dependency** in favor of clean SVG line iconography, and robust multimodal scene intelligence.

---

## Core Operational Modes

1. **Text Analysis:** Enter any waste item description to receive instant categorization, disposal steps, and upcycling ideas.
2. **Visual Analysis (Image Only):** Upload a photo or use the device camera to analyze either individual discrete items or large open trash heaps.
3. **Visual Analysis (Image + Context):** Provide optional location and situational context alongside the image (with visual evidence strictly prioritized).

---

## UN SDG 12 Alignment

EcoSort AI directly supports **United Nations Sustainable Development Goal 12: Responsible Consumption and Production**, specifically **Target 12.5**:

> *"By 2030, substantially reduce waste generation through prevention, reduction, recycling, and reuse."*

### Key Contributions:
- **Source Segregation:** Eliminates municipal landfill contamination by guiding proper initial sorting across Wet, Dry, E-Waste, and Hazardous bins.
- **Circular Economy Promotion:** Suggests creative, practical DIY repurposing and upcycling methods to lengthen product lifecycles.
- **Site-Level Cleanup Protocols:** Automatically generates safety precautions, required PPE, and numbered cleanup sequences for illegal open trash heaps or campus accumulation spots.
- **Environmental Hazard Awareness:** Educates users on leachate contamination, microplastics, heavy metal soil poisoning, and methane emissions from improper dumping.

---

## UI/UX & Design System

- **Dual Theme Support:** Seamless toggle between **Light Mode** (bright `#F6FAF8` canvas, crisp typography) and **Dark Mode** (deep `#0B1220` canvas, elevated surfaces) with instant state persistence.
- **Centralized Design Tokens:** Standardized CSS variables for surfaces, borders, typography, shadows, and accessible semantic colors.
- **Professional Line Iconography:** Custom SVG vector icons replace emojis across buttons, badges, navigation, and results.
- **Accessible Categories:** Clear color-coded badges with explicit text labels:
  - **Wet Waste:** Organic, food scraps, compostables (Green)
  - **Dry Waste:** Paper, clean plastics, glass, metals, textiles (Blue)
  - **E-Waste:** Electronics, gadgets, cables, appliances (Amber)
  - **Hazardous Waste:** Batteries, chemicals, medical sharps, paints (Red)
- **Hierarchical Result Cards:** Highlights the recommended action on a prominent mint card, accompanied by preparation steps, environmental risks, and upcycling ideas.

---

## Technology Stack

| Layer | Technology |
|---|---|
| **Frontend & UI** | Streamlit (Python 3.12) |
| **Styling & Theming** | CSS Variables Design Token System (Light / Dark) |
| **LLM & Vision** | Google Gemini SDK (`google-genai`) |
| **Image Processing** | Pillow (PIL) |
| **Data Validation** | Pydantic v2 (Strict Schema Enforcement) |
| **Environment Management** | `python-dotenv` & Streamlit Secrets |

---

## Project Structure

```text
EcoSort-AI/
│
├── app.py                  # Main Streamlit web application, UI design system & Gemini vision pipeline
├── requirements.txt        # Minimal application dependencies
├── README.md               # Comprehensive project documentation
├── .env.example            # Environment variable template
├── .gitignore              # Git exclusion rules for secrets and virtualenvs
├── test_app.py             # Automated unit tests for data models, theme & image validation
├── test_live_scenarios.py  # End-to-end integration test suite for Gemini API
└── venv/                   # Isolated Python virtual environment
```

---

## Getting Started

### 1. Prerequisites
- Python 3.10 or newer (tested on Python 3.12)
- A Google Gemini API Key (obtain one free at [Google AI Studio](https://aistudio.google.com/))

### 2. Setup Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API Key
Create a `.env` file from the example:
```bash
cp .env.example .env
```
And add your API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
*(Alternatively, enter your key directly in the application sidebar or `.streamlit/secrets.toml`)*

### 5. Launch Application
```bash
streamlit run app.py
```
Open your browser to: `http://localhost:8501`

---

## Automated Testing

### Run Offline Unit Tests
```bash
.\venv\Scripts\python.exe test_app.py
```

### Run Live Gemini API Tests
```bash
.\venv\Scripts\python.exe test_live_scenarios.py
```

---

## Safety & Disclaimer

*EcoSort AI provides general sustainability guidance based on supplied inputs, images, and context. It cannot guarantee material composition or universal municipal disposal rules. Follow your local waste-management regulations and seek professional guidance for hazardous, medical, chemical, or unknown waste.*

---

**Developed for the 1M1B AI for Sustainability Internship | Advancing UN SDG 12**
=======
# ecosort-ai
Internship project for 1m1b internship 
>>>>>>> cb738a117bef695257d315773131c839c2d24320



## 🚀 Quick Start (Windows 1-Click Launch)

1. Click the green **Code** button on GitHub and select **Download ZIP**.
2. Extract the ZIP folder to your PC.
3. Open the folder and double-click **`run.bat`**.
   * It will automatically set up the environment and launch EcoSort AI in your browser.
4. If prompted, open the created `.env` file and enter your free Gemini API Key.

