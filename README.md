# 𝕔𝕠𝕟𝕧𝕖𝕣𝕥𝕟𝕖𝕩𝕥.𝕚𝕟 - The Ultimate Utility Suite 🚀

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Welcome to **convertnext.in**, your everyday next-gen tool hub. This project is a massive, highly optimized web application built purely in Python and Streamlit. It consolidates over 50 complex utilities—ranging from advanced PDF manipulation and AI-powered image editing to live financial calculators and educational tools—into one blazing-fast, server-side interface.

## ✨ Key Features

This suite is divided into 8 powerhouse modules:

### 📄 Ultimate PDF Suite
* **Combine & Organize:** Merge, Split, Rotate, Remove, and Rearrange pages.
* **Convert:** Images to PDF, PDF to PNGs, Extract hidden images, and Webpage to PDF.
* **Security & Editing:** Add/Remove Passwords, Watermark, Redact text securely, Web Optimize (Linearize), Compress target sizes, and overlay Signatures.
* **AI OCR:** Extract actual text from flat, scanned PDF images using Tesseract.

### 🖼️ Image Studio
* **Edit & Compress:** Advanced Resizer, Crop & Rotate, Passport Photo Maker (35x45mm), and Target KB/MB Compressor.
* **AI & Enhance:** AI Background Removal (rembg), Photo Enhancer (Contrast/Brightness/Sharpness), and EXIF Metadata viewer.
* **Convert & Collage:** Format & DPI Converter (PNG, JPEG, WEBP) and Image Grid Collages.
* **Generators:** Add Name & DOB, Meme Generator, QR Code Maker, and Image-to-Text (OCR).

### 💰 Financial Calculators
* **Loan EMI & Compound Interest:** Instant dynamic calculations with beautiful metric displays.
* **🇮🇳 Indian Tax Calculator:** Custom built for FY 25-26 with standard deductions and exact slab rates.
* **Live Currency Converter:** Real-time exchange rates powered by the Frankfurter API.

### 🎓 Education & Math Tools
* **Calculators:** Full Interactive Scientific Calculator, General Percentage, and Expression Evaluator.
* **Algebra & Geometry:** Prime/Factor analysis, GCD/LCM, Quadratic Solver, and shape calculations.
* **Statistics & Grades:** Descriptive stats, Exam Percentage, and an interactive grid for CGPA tracking.
* **Converters:** Number Base (Dec/Bin/Hex) and Scientific Notation.

### 🛠️ Developer Utilities
* Hash (SHA-256, MD5) & UUID Generator.
* Base64 Encoder/Decoder.
* JSON Formatter & Validator.

### ⚖️ Universal Unit Converter & ✒️ Signature Pad
* Convert everything from Length, Weight, and Area to complex Temperature math.
* Smooth, touch-friendly freehand Signature Pad to draw, save, and resize digital signatures.

---

## 💻 Tech Stack

* **Frontend & Framework:** [Streamlit](https://streamlit.io/)
* **PDF Processing:** PyMuPDF (`fitz`), `pdfkit`
* **Image & Vision:** Pillow (`PIL`), `rembg`, `pytesseract`, `streamlit-cropper`
* **AI Integration:** Google Generative AI (`gemini-2.5-flash`)
* **Interactive UI:** `streamlit-drawable-canvas`, `pandas`

---

## 🚀 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/convertnext.git](https://github.com/yourusername/convertnext.git)
   cd convertnext
