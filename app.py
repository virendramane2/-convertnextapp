import math
import statistics
import cmath
import pandas as pd
import streamlit as st
import hashlib
import uuid
import base64
import json
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ExifTags
import io
import qrcode
import numpy as np
import requests  # <--- Add this line right here!

# Safe imports for external heavy libraries
try:
    from rembg import remove
except ImportError:
    remove = None

# ... (the rest of your try-except imports stay the same)
import numpy as np

try:
    from streamlit_drawable_canvas import st_canvas
except ImportError:
    st_canvas = None
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ExifTags
import io
import qrcode

# Safe imports for external heavy libraries
try:
    from rembg import remove
except ImportError:
    remove = None

try:
    import pytesseract
except ImportError:
    pytesseract = None

try:
    from streamlit_cropper import st_cropper
except ImportError:
    st_cropper = None
from PIL import ImageDraw, ImageFont, ImageEnhance, ExifTags
import qrcode
import pytesseract
import io
try:
    from rembg import remove
except ImportError:
    remove = None
try:
    from streamlit_cropper import st_cropper
except ImportError:
    st_cropper = None
import streamlit as st
import hashlib
import uuid
import base64
import json
import google.generativeai as genai
import fitz  # PyMuPDF
from PIL import Image
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="convertnext.in - Ultimate Utility Suite", layout="wide")

# --- CSS FOR CUSTOM BRANDING ---
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; font-weight: 800; text-align: center; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .sub-header { text-align: center; color: #64748b; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER & API KEY SECRETS ---
st.markdown('<div class="main-header">𝕔𝕠𝕟𝕧𝕖𝕣𝕥𝕟𝕖𝕩𝕥.𝕚𝕟</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">“𝓨𝓸𝓾𝓻 𝓔𝓿𝓮𝓻𝔂𝓭𝓪𝔂 𝓝𝓮𝔁𝓽-𝓖𝓮𝓷 𝓣𝓸𝓸𝓵⇄𝓗𝓾𝓫”</div>', unsafe_allow_html=True)

with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API key securely here.")
    if api_key:
        genai.configure(api_key=api_key)

    st.divider()
    st.title("Navigation")
    page = st.radio("Select Tool", [
        "📄 PDF", 
        "🖼️ Image", 
        "✒️ Signature", 
        "📝 Text & AI", 
        "💰 Finance", 
        "⚖️ Units", 
        "🎓 Education", 
        "🛠️ Utilities"
    ])

# ==========================================
# TOOL SECTIONS
# ==========================================

if page == "🛠️ Utilities":
    st.header("🛠️ Utilities")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔐 Password & Hash")
        if st.button("Generate UUID"):
            st.code(str(uuid.uuid4()))
            
        hash_input = st.text_input("Enter text to hash")
        h_col1, h_col2 = st.columns(2)
        with h_col1:
            if st.button("SHA-256"):
                st.info(hashlib.sha256(hash_input.encode()).hexdigest())
        with h_col2:
            if st.button("MD5"):
                st.info(hashlib.md5(hash_input.encode()).hexdigest())

    with col2:
        st.subheader("🔤 Base64 Encode / Decode")
        b64_input = st.text_area("Input text for Base64")
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("Encode"):
                st.code(base64.b64encode(b64_input.encode()).decode())
        with b_col2:
            if st.button("Decode"):
                try:
                    st.code(base64.b64decode(b64_input.encode()).decode())
                except Exception:
                    st.error("Invalid Base64 string")

    st.divider()
    st.subheader("{} JSON Formatter")
    json_input = st.text_area("Paste JSON here")
    if st.button("Format JSON"):
        try:
            parsed = json.loads(json_input)
            st.json(parsed)
        except json.JSONDecodeError:
            st.error("Invalid JSON format.")

elif page == "📝 Text & AI":
    st.header("📝 Text Tools & AI Lab")
    
    st.subheader("✨ AI Text Lab")
    ai_input = st.text_area("Paste text to analyze:")
    
    t_col1, t_col2, t_col3 = st.columns(3)
    
    if not api_key:
        st.warning("Please enter your Gemini API Key in the sidebar to use AI features.")
    else:
        model = genai.GenerativeModel('gemini-2.5-flash')
        with t_col1:
            if st.button("✨ Summarize"):
                with st.spinner("Thinking..."):
                    response = model.generate_content(f"Summarize this text concisely: {ai_input}")
                    st.write(response.text)
        with t_col2:
            if st.button("✨ Fix Grammar"):
                with st.spinner("Thinking..."):
                    response = model.generate_content(f"Fix grammar and improve style: {ai_input}")
                    st.write(response.text)
        with t_col3:
            target_lang = st.selectbox("Translate to", ["Hindi", "Marathi", "Spanish", "French"])
            if st.button("🌐 Translate"):
                with st.spinner("Translating..."):
                    response = model.generate_content(f"Translate the following into {target_lang}: {ai_input}")
                    st.write(response.text)
                    
    st.divider()
    st.subheader("Standard Text Tools")
    std_text = st.text_area("Input standard text:")
    c_col1, c_col2, c_col3 = st.columns(3)
    with c_col1:
        if st.button("UPPERCASE"): st.code(std_text.upper())
    with c_col2:
        if st.button("lowercase"): st.code(std_text.lower())
    with c_col3:
        if st.button("Title Case"): st.code(std_text.title())

elif page == "💰 Finance":
    st.header("💰 Financial Calculators")
    
    # Added the 4th tab for Currency
    fin_tab1, fin_tab2, fin_tab3, fin_tab4 = st.tabs(["Loan EMI", "Compound Interest", "🇮🇳 Tax (FY 25-26)", "💱 Currency"])
    
    with fin_tab1:
        st.subheader("Loan EMI Calculator")
        emi_col1, emi_col2, emi_col3 = st.columns(3)
        with emi_col1:
            p = st.number_input("Loan Amount (₹)", min_value=0.0, value=100000.0, step=10000.0)
        with emi_col2:
            r_annual = st.number_input("Interest Rate (%)", min_value=0.0, value=8.5, step=0.1)
        with emi_col3:
            n_years = st.number_input("Tenure (Years)", min_value=0.0, value=5.0, step=1.0)
            
        if st.button("Calculate EMI", type="primary", use_container_width=True):
            r_monthly = (r_annual / 12) / 100
            n_months = n_years * 12
            
            if p > 0 and r_monthly > 0 and n_months > 0:
                emi = (p * r_monthly * (1 + r_monthly)**n_months) / ((1 + r_monthly)**n_months - 1)
                total_amount = emi * n_months
                total_interest = total_amount - p
                
                res1, res2, res3 = st.columns(3)
                res1.metric("Monthly EMI", f"₹ {emi:,.2f}")
                res2.metric("Total Interest", f"₹ {total_interest:,.2f}")
                res3.metric("Total Amount", f"₹ {total_amount:,.2f}")
            else:
                st.warning("Please enter values greater than zero.")

    with fin_tab2:
        st.subheader("Compound Interest Calculator")
        ci_col1, ci_col2 = st.columns(2)
        with ci_col1:
            ci_p = st.number_input("Principal Amount (₹)", min_value=0.0, value=10000.0, step=1000.0)
            ci_t = st.number_input("Time Period (Years)", min_value=0.0, value=10.0, step=1.0)
        with ci_col2:
            ci_r = st.number_input("Annual Rate (%)", min_value=0.0, value=5.0, step=0.1)
            ci_n_str = st.selectbox("Compounding Frequency", ["Yearly", "Half-Yearly", "Quarterly", "Monthly"])
            
            freq_map = {"Yearly": 1, "Half-Yearly": 2, "Quarterly": 4, "Monthly": 12}
            ci_n = freq_map[ci_n_str]

        if st.button("Calculate Compound Interest", type="primary", use_container_width=True):
            amount = ci_p * (1 + (ci_r / 100) / ci_n)**(ci_n * ci_t)
            interest = amount - ci_p
            
            c_res1, c_res2 = st.columns(2)
            c_res1.metric("Total Amount", f"₹ {amount:,.2f}")
            c_res2.metric("Interest Earned", f"₹ {interest:,.2f}")

    with fin_tab3:
        st.subheader("🇮🇳 Tax Calculator (FY 25-26)")
        tax_income = st.number_input("Total Annual Income (₹)", min_value=0.0, value=750000.0, step=50000.0)
        
        if st.button("Calculate Tax", type="primary", use_container_width=True):
            net_income = max(0, tax_income - 75000)
            tax = 0.0
            
            if net_income > 1500000:
                tax += (net_income - 1500000) * 0.30
                tax += 300000 * 0.20
                tax += 200000 * 0.15
                tax += 300000 * 0.10
                tax += 400000 * 0.05
            elif net_income > 1200000:
                tax += (net_income - 1200000) * 0.20
                tax += 200000 * 0.15
                tax += 300000 * 0.10
                tax += 400000 * 0.05
            elif net_income > 1000000:
                tax += (net_income - 1000000) * 0.15
                tax += 300000 * 0.10
                tax += 400000 * 0.05
            elif net_income > 700000:
                tax += (net_income - 700000) * 0.10
                tax += 400000 * 0.05
            elif net_income <= 700000:
                tax = 0.0 
                
            cess = tax * 0.04
            total_tax = tax + cess
            
            st.markdown("### Tax Breakdown")
            t_res1, t_res2, t_res3 = st.columns(3)
            t_res1.metric("Income Tax", f"₹ {tax:,.2f}")
            t_res2.metric("Health & Edu Cess (4%)", f"₹ {cess:,.2f}")
            t_res3.metric("Total Tax Payable", f"₹ {total_tax:,.2f}", delta_color="inverse")

    with fin_tab4:
        st.subheader("💱 Live Currency Converter")
        try:
            # Using 'requests' with a timeout and a browser-like User-Agent to prevent getting blocked
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get('https://api.frankfurter.app/currencies', headers=headers, timeout=5)
            response.raise_for_status() # This checks if the API is down
            
            currencies = response.json()
            curr_list = list(currencies.keys())
            
            # Default to USD -> INR if they exist
            default_from = curr_list.index("USD") if "USD" in curr_list else 0
            default_to = curr_list.index("INR") if "INR" in curr_list else 0

            cur_col1, cur_col2, cur_col3 = st.columns(3)
            with cur_col1:
                cur_amt = st.number_input("Amount", min_value=0.0, value=1.0, step=1.0)
            with cur_col2:
                cur_from = st.selectbox("From", curr_list, index=default_from)
            with cur_col3:
                cur_to = st.selectbox("To", curr_list, index=default_to)

            if st.button("Convert Currency", type="primary", use_container_width=True):
                if cur_from == cur_to:
                    st.success(f"**{cur_amt} {cur_from}** = **{cur_amt} {cur_to}**")
                elif cur_amt > 0:
                    with st.spinner("Fetching live rates..."):
                        conv_res = requests.get(
                            f"https://api.frankfurter.app/latest?amount={cur_amt}&from={cur_from}&to={cur_to}", 
                            headers=headers, 
                            timeout=5
                        )
                        conv_res.raise_for_status()
                        conv_data = conv_res.json()
                        converted_amt = conv_data['rates'][cur_to]
                        
                        st.success(f"**{cur_amt:,.2f} {cur_from}** = **{converted_amt:,.2f} {cur_to}**")
                else:
                    st.warning("Please enter an amount greater than zero.")

        except requests.exceptions.RequestException as e:
            # This will now print the EXACT reason it failed (Timeout, SSL Error, etc.)
            st.error(f"Network Error: Could not connect to the currency API. Details: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

        except Exception as e:
            st.error("Could not fetch live exchange rates. Please check your internet connection or try again later.")

elif page == "📄 PDF":
    st.header("📄 Ultimate PDF Suite")
    
    # The massive list of 24 tools!
    pdf_tools = [
        "Merge PDF", "Split PDF", "Compress PDF (Target Size)", "Edit PDF", "Sign PDF", 
        "PDF Convert", "Images to PDF", "PDF to Images", "Extract PDF images", 
        "Protect PDF", "Unlock PDF", "Rotate PDF pages", "Remove PDF pages", 
        "Extract PDF pages", "Rearrange PDF pages", "Webpage to PDF", "PDF OCR", 
        "Add watermark", "Add page numbers", "PDF Overlay", "Compare PDFs", 
        "Web optimize PDF", "Redact PDF", "Create PDF"
    ]
    
    # Clean UI Dropdown
    selected_tool = st.selectbox("Select PDF Tool", pdf_tools)
    st.divider()
    
    # ==========================================
    # COMBINE & SPLIT
    # ==========================================
    if selected_tool == "Merge PDF":
        st.subheader("Merge Multiple PDFs")
        uploaded_pdfs = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
        if st.button("Merge Files", type="primary") and uploaded_pdfs:
            if len(uploaded_pdfs) < 2:
                st.warning("Please upload at least 2 PDFs.")
            else:
                merged_pdf = fitz.open()
                for pdf_file in uploaded_pdfs:
                    pdf_doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
                    merged_pdf.insert_pdf(pdf_doc)
                st.download_button("Download Merged PDF", data=merged_pdf.write(), file_name="merged.pdf", mime="application/pdf")

    elif selected_tool == "Split PDF":
        st.subheader("Split PDF into Pages")
        split_pdf = st.file_uploader("Upload PDF", type="pdf")
        if st.button("Split") and split_pdf:
            doc = fitz.open(stream=split_pdf.read(), filetype="pdf")
            for page_num in range(len(doc)):
                new_doc = fitz.open()
                new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
                st.download_button(f"⬇️ Download Page {page_num + 1}", data=new_doc.write(), file_name=f"page_{page_num + 1}.pdf", mime="application/pdf", key=f"split_{page_num}")

    # ==========================================
    # ORGANIZE PAGES
    # ==========================================
    elif selected_tool == "Rotate PDF pages":
        st.subheader("Rotate Pages")
        rot_pdf = st.file_uploader("Upload PDF", type="pdf")
        angle = st.selectbox("Rotation Angle", [90, 180, 270])
        if st.button("Rotate All Pages") and rot_pdf:
            doc = fitz.open(stream=rot_pdf.read(), filetype="pdf")
            for page in doc:
                page.set_rotation(angle)
            st.download_button("Download Rotated PDF", data=doc.write(), file_name="rotated.pdf", mime="application/pdf")

    elif selected_tool == "Remove PDF pages":
        st.subheader("Remove Specific Pages")
        rm_pdf = st.file_uploader("Upload PDF", type="pdf")
        pages_to_rm = st.text_input("Pages to remove (comma separated, e.g., 1, 3, 5)")
        if st.button("Remove Pages") and rm_pdf and pages_to_rm:
            try:
                doc = fitz.open(stream=rm_pdf.read(), filetype="pdf")
                # Convert 1-based user input to 0-based python index
                pages = [int(p.strip()) - 1 for p in pages_to_rm.split(",")]
                doc.delete_pages(pages)
                st.download_button("Download Updated PDF", data=doc.write(), file_name="removed_pages.pdf", mime="application/pdf")
            except Exception as e:
                st.error("Invalid page numbers.")

    # ==========================================
    # SIGN, OCR, AND CONVERT TOOLS
    # ==========================================
elif selected_tool == "PDF Convert":
        st.subheader("🔄 Advanced PDF Converter")
        st.info("Convert your documents seamlessly between formats.")
        
        # Sub-menu for the different conversion types
        conv_type = st.selectbox("Select Conversion Type", [
            "PDF to Word", 
            "PDF to Excel", 
            "PDF to JPG", 
            "PDF to Powerpoint", 
            "PDF to PDF/A", 
            "eBooks to PDF", 
            "iWork to PDF"
        ])
        
        st.divider()

        # 1. PDF TO WORD
        if conv_type == "PDF to Word":
            conv_pdf = st.file_uploader("Upload PDF to convert to Word", type="pdf", key="pdf2word")
            if st.button("Convert to Word", type="primary") and conv_pdf:
                try:
                    from pdf2docx import Converter
                    import tempfile
                    import os

                    with st.spinner("Converting to Word... This might take a minute."):
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                            tmp_pdf.write(conv_pdf.read())
                            pdf_path = tmp_pdf.name

                        docx_path = pdf_path.replace(".pdf", ".docx")
                        cv = Converter(pdf_path)
                        cv.convert(docx_path)
                        cv.close()

                        with open(docx_path, "rb") as f:
                            st.download_button("⬇️ Download Word Document", data=f, file_name="converted.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", type="primary")

                        os.remove(pdf_path)
                        os.remove(docx_path)
                except ImportError:
                    st.error("Please add `pdf2docx` to your requirements.txt file.")

        # 2. PDF TO EXCEL
        elif conv_type == "PDF to Excel":
            st.caption("Note: This extracts visible tables from the PDF into an Excel spreadsheet.")
            excel_pdf = st.file_uploader("Upload PDF with Tables", type="pdf", key="pdf2excel")
            if st.button("Convert to Excel", type="primary") and excel_pdf:
                try:
                    import pdfplumber
                    import pandas as pd
                    import io

                    with st.spinner("Extracting tables to Excel..."):
                        with pdfplumber.open(excel_pdf) as pdf:
                            all_tables = []
                            for page in pdf.pages:
                                tables = page.extract_tables()
                                for table in tables:
                                    df = pd.DataFrame(table[1:], columns=table[0])
                                    all_tables.append(df)
                            
                            if all_tables:
                                # Combine all extracted tables into one sheet for simplicity
                                final_df = pd.concat(all_tables, ignore_index=True)
                                
                                buffer = io.BytesIO()
                                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                                    final_df.to_excel(writer, index=False, sheet_name='Extracted Data')
                                
                                st.download_button("⬇️ Download Excel File", data=buffer.getvalue(), file_name="extracted_tables.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", type="primary")
                            else:
                                st.warning("No tabular data found in this PDF.")
                except ImportError:
                    st.error("Please add `pdfplumber` and `openpyxl` to requirements.txt.")

        # 3. PDF TO JPG
        elif conv_type == "PDF to JPG":
            jpg_pdf = st.file_uploader("Upload PDF to convert to JPGs", type="pdf", key="pdf2jpg")
            if st.button("Convert to JPG", type="primary") and jpg_pdf:
                import fitz
                import zipfile
                import io
                
                with st.spinner("Rendering pages to high-quality JPGs..."):
                    doc = fitz.open(stream=jpg_pdf.read(), filetype="pdf")
                    zip_buffer = io.BytesIO()
                    
                    # Package all images into a ZIP file for easy downloading
                    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                        for i, page in enumerate(doc):
                            pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
                            img_bytes = pix.tobytes("jpeg")
                            zip_file.writestr(f"page_{i+1}.jpg", img_bytes)
                            
                    st.download_button("⬇️ Download JPGs (ZIP file)", data=zip_buffer.getvalue(), file_name="converted_images.zip", mime="application/zip", type="primary")

        # 4. COMPLEX FORMATS (Placeholders for Cloud API Integration)
        elif conv_type in ["PDF to Powerpoint", "PDF to PDF/A"]:
            st.warning(f"**{conv_type}** requires deep structural file rewriting.")
            st.info("To implement this in Python, you will need to integrate a cloud service API like **CloudConvert** or **Zamzar**, or install deep system libraries like Ghostscript (for PDF/A). This UI is ready for your API keys in Phase 2!")
            st.file_uploader("Upload File (API Not Connected)", disabled=True)

        elif conv_type in ["eBooks to PDF", "iWork to PDF"]:
            st.warning(f"**{conv_type}** deals with proprietary or highly complex reflowable formats.")
            st.info("Formats like EPUB, MOBI, Pages, and Keynote cannot be perfectly converted using pure offline Python without breaking the formatting. This interface is built and ready for a third-party conversion API integration!")
            st.file_uploader("Upload File (API Not Connected)", disabled=True)
    
    elif selected_tool == "Sign PDF":
        st.subheader("✒️ Sign PDF (Overlay Signature)")
        sign_pdf = st.file_uploader("Upload PDF to Sign", type="pdf", key="sign_pdf")
        sig_img = st.file_uploader("Upload Signature Image (PNG with transparent background is best)", type=["png", "jpg", "jpeg"], key="sig_img")
        
        st.write("### Positioning")
        page_num = st.number_input("Page Number to place signature", min_value=1, value=1)
        
        c1, c2 = st.columns(2)
        x_pos = c1.number_input("X Position (Left to Right)", value=100)
        y_pos = c2.number_input("Y Position (Top to Bottom)", value=700)
        
        if st.button("Apply Signature", type="primary") and sign_pdf and sig_img:
            doc = fitz.open(stream=sign_pdf.read(), filetype="pdf")
            if 1 <= page_num <= len(doc):
                page = doc[page_num - 1]
                
                # Define the rectangle where the signature will be placed (width: 150px, height: 50px)
                rect = fitz.Rect(x_pos, y_pos, x_pos + 150, y_pos + 50)
                img_bytes = sig_img.read()
                
                # Overlay the image onto the PDF
                page.insert_image(rect, stream=img_bytes)
                st.success("Signature applied successfully!")
                st.download_button("Download Signed PDF", data=doc.write(), file_name="signed_document.pdf", mime="application/pdf")
            else:
                st.error("Invalid page number. The PDF doesn't have that many pages.")
                
    elif selected_tool == "PDF OCR":
        st.subheader("👁️‍🗨️ PDF OCR (Extract text from Scanned PDFs)")
        st.info("Standard text extraction fails on scanned PDFs. This tool uses AI (Tesseract) to read the actual images inside the PDF.")
        ocr_pdf = st.file_uploader("Upload Scanned PDF", type="pdf")
        
        if st.button("Run OCR Scan", type="primary") and ocr_pdf:
            try:
                import pytesseract
                with st.spinner("Scanning images for text... (This takes a few seconds per page)"):
                    doc = fitz.open(stream=ocr_pdf.read(), filetype="pdf")
                    full_text = ""
                    img_count = 0
                    
                    for i in range(len(doc)):
                        for img_info in doc.get_page_images(i):
                            xref = img_info[0]
                            base_image = doc.extract_image(xref)
                            img = Image.open(io.BytesIO(base_image["image"]))
                            
                            # Run optical character recognition on the extracted image
                            full_text += pytesseract.image_to_string(img) + "\n\n"
                            img_count += 1
                            
                    if img_count == 0:
                        st.warning("No images found to scan. Try using the standard 'Extract Text' tool instead.")
                    else:
                        st.success(f"Successfully scanned {img_count} images!")
                        st.text_area("Extracted OCR Text:", value=full_text, height=300)
            except ImportError:
                st.error("pytesseract is missing. Please add it to requirements.txt.")
            except Exception as e:
                st.error(f"OCR Error: Make sure Tesseract-OCR system software is installed. Details: {e}")

    elif selected_tool == "Rearrange PDF pages":
        st.subheader("Rearrange Pages")
        re_pdf = st.file_uploader("Upload PDF", type="pdf")
        page_order = st.text_input("New order (comma separated, e.g., 3, 1, 2)")
        if st.button("Rearrange") and re_pdf and page_order:
            try:
                doc = fitz.open(stream=re_pdf.read(), filetype="pdf")
                pages = [int(p.strip()) - 1 for p in page_order.split(",")]
                doc.select(pages)
                st.download_button("Download Rearranged PDF", data=doc.write(), file_name="rearranged.pdf", mime="application/pdf")
            except Exception:
                st.error("Invalid page sequence.")

    # ==========================================
    # CONVERT
    # ==========================================
    elif selected_tool == "Images to PDF":
        st.subheader("Images to PDF")
        img_files = st.file_uploader("Select Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        if st.button("Generate PDF") and img_files:
            images = [Image.open(f).convert("RGB") for f in img_files]
            if images:
                pdf_bytes = io.BytesIO()
                images[0].save(pdf_bytes, format="PDF", save_all=True, append_images=images[1:])
                st.download_button("Download PDF", data=pdf_bytes.getvalue(), file_name="images.pdf", mime="application/pdf")

    elif selected_tool == "PDF to Images":
        st.subheader("PDF to Images")
        pdf_to_img = st.file_uploader("Upload PDF", type="pdf")
        if st.button("Convert to PNGs") and pdf_to_img:
            doc = fitz.open(stream=pdf_to_img.read(), filetype="pdf")
            for i, page in enumerate(doc):
                pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
                st.image(pix.tobytes("png"), caption=f"Page {i+1}", width=300)
                st.download_button(f"Download Page {i+1}", data=pix.tobytes("png"), file_name=f"page_{i+1}.png", mime="image/png", key=f"img_{i}")

    elif selected_tool == "Extract PDF images":
        st.subheader("Extract all Images hidden inside a PDF")
        ext_img_pdf = st.file_uploader("Upload PDF", type="pdf")
        if st.button("Extract Images") and ext_img_pdf:
            doc = fitz.open(stream=ext_img_pdf.read(), filetype="pdf")
            img_count = 0
            for i in range(len(doc)):
                for img_info in doc.get_page_images(i):
                    xref = img_info[0]
                    base_image = doc.extract_image(xref)
                    st.download_button(f"Download Image {img_count+1}", data=base_image["image"], file_name=f"ext_img_{img_count}.{base_image['ext']}", key=f"ext_{img_count}")
                    img_count += 1
            if img_count == 0: st.info("No images found in this PDF.")

    # ==========================================
    # SECURITY & EDITING
    # ==========================================
    elif selected_tool == "Protect PDF":
        st.subheader("Add Password to PDF")
        lock_pdf = st.file_uploader("Upload PDF", type="pdf")
        pwd = st.text_input("Enter Password", type="password")
        if st.button("Encrypt PDF") and lock_pdf and pwd:
            doc = fitz.open(stream=lock_pdf.read(), filetype="pdf")
            doc.save("temp.pdf", encryption=fitz.PDF_ENCRYPT_AES_256, user_pw=pwd, owner_pw=pwd)
            with open("temp.pdf", "rb") as f:
                st.download_button("Download Locked PDF", data=f, file_name="locked.pdf", mime="application/pdf")

    elif selected_tool == "Unlock PDF":
        st.subheader("Remove Password from PDF")
        unlock_pdf = st.file_uploader("Upload Locked PDF", type="pdf")
        pwd = st.text_input("Enter Current Password", type="password")
        if st.button("Unlock") and unlock_pdf and pwd:
            doc = fitz.open(stream=unlock_pdf.read(), filetype="pdf")
            if doc.authenticate(pwd):
                st.download_button("Download Unlocked PDF", data=doc.write(), file_name="unlocked.pdf", mime="application/pdf")
            else:
                st.error("Incorrect Password.")

    elif selected_tool == "Add watermark":
        st.subheader("Add Text Watermark")
        wm_pdf = st.file_uploader("Upload PDF", type="pdf")
        wm_text = st.text_input("Watermark Text", value="CONFIDENTIAL")
        if st.button("Add Watermark") and wm_pdf and wm_text:
            doc = fitz.open(stream=wm_pdf.read(), filetype="pdf")
            for page in doc:
                page.insert_text((100, 100), wm_text, fontsize=50, color=(1, 0, 0), fill_opacity=0.3, rotate=45)
            st.download_button("Download Watermarked PDF", data=doc.write(), file_name="watermark.pdf", mime="application/pdf")

    elif selected_tool == "Redact PDF":
        st.subheader("Redact (Blackout) Text")
        redact_pdf = st.file_uploader("Upload PDF", type="pdf")
        search_text = st.text_input("Exact Text to Redact")
        if st.button("Redact Document") and redact_pdf and search_text:
            doc = fitz.open(stream=redact_pdf.read(), filetype="pdf")
            count = 0
            for page in doc:
                areas = page.search_for(search_text)
                for area in areas:
                    page.add_redact_annot(area, fill=(0, 0, 0))
                    count += 1
                page.apply_redactions()
            st.success(f"Redacted {count} instances.")
            st.download_button("Download Redacted PDF", data=doc.write(), file_name="redacted.pdf", mime="application/pdf")

    elif selected_tool == "Web optimize PDF":
        st.subheader("Fast Web View (Linearize)")
        opt_pdf = st.file_uploader("Upload PDF", type="pdf")
        if st.button("Optimize") and opt_pdf:
            doc = fitz.open(stream=opt_pdf.read(), filetype="pdf")
            st.download_button("Download Optimized PDF", data=doc.write(linear=True), file_name="optimized.pdf", mime="application/pdf")

    elif selected_tool == "Compress PDF (Target Size)":
        st.subheader("Compress PDF")
        comp_pdf = st.file_uploader("Upload PDF", type="pdf")
        if st.button("Basic Compression") and comp_pdf:
            doc = fitz.open(stream=comp_pdf.read(), filetype="pdf")
            # Garbage=4 and deflate removes unused objects and compresses streams
            st.download_button("Download Compressed", data=doc.write(garbage=4, deflate=True), file_name="compressed.pdf", mime="application/pdf")
            st.info("Note: Extreme target size compression (KB) requires deep image downsampling which takes longer. Basic compression applied.")

   # ==========================================
    # FINAL ADVANCED TOOLS
    # ==========================================
    elif selected_tool == "Create PDF":
        st.subheader("📝 Create PDF from Scratch")
        st.info("Type your content below to generate a brand new PDF document.")
        new_pdf_text = st.text_area("Enter Document Text", height=300)
        
        if st.button("Generate PDF", type="primary") and new_pdf_text:
            doc = fitz.open()
            page = doc.new_page()
            
            # Simple text insertion with automatic word wrapping
            rect = fitz.Rect(50, 50, page.rect.width - 50, page.rect.height - 50)
            page.insert_textbox(rect, new_pdf_text, fontsize=12, fontname="helv", color=(0,0,0))
            
            st.success("PDF Created Successfully!")
            st.download_button("Download New PDF", data=doc.write(), file_name="new_document.pdf", mime="application/pdf")

    elif selected_tool == "Edit PDF":
        st.subheader("🖍️ Edit PDF (Add Text/Annotations)")
        st.info("Since PDFs are flattened, you cannot easily delete existing text, but you can overlay new text anywhere on the page!")
        edit_pdf = st.file_uploader("Upload PDF to Edit", type="pdf")
        
        edit_page = st.number_input("Page Number", min_value=1, value=1)
        edit_text = st.text_input("Text to Add", value="APPROVED")
        
        c1, c2 = st.columns(2)
        x_pos = c1.number_input("X Position (Left to Right)", value=100)
        y_pos = c2.number_input("Y Position (Top to Bottom)", value=100)
        
        if st.button("Apply Text", type="primary") and edit_pdf and edit_text:
            doc = fitz.open(stream=edit_pdf.read(), filetype="pdf")
            if 1 <= edit_page <= len(doc):
                page = doc[edit_page - 1]
                page.insert_text((x_pos, y_pos), edit_text, fontsize=18, color=(1, 0, 0)) # Red text by default
                
                st.success("Text added successfully!")
                st.download_button("Download Edited PDF", data=doc.write(), file_name="edited.pdf", mime="application/pdf")
            else:
                st.error("Invalid page number.")

    elif selected_tool == "PDF Overlay":
        st.subheader("🥪 PDF Overlay (Merge Layers)")
        st.info("Stamps one PDF directly on top of another. Great for applying letterheads or complex watermarks.")
        base_pdf = st.file_uploader("Upload Base PDF (Bottom Layer)", type="pdf", key="base")
        top_pdf = st.file_uploader("Upload Overlay PDF (Top Layer)", type="pdf", key="top")
        
        if st.button("Overlay PDFs", type="primary") and base_pdf and top_pdf:
            doc_base = fitz.open(stream=base_pdf.read(), filetype="pdf")
            doc_top = fitz.open(stream=top_pdf.read(), filetype="pdf")
            
            # Overlay page by page up to the shortest document's length
            pages_to_process = min(len(doc_base), len(doc_top))
            
            for i in range(pages_to_process):
                # show_pdf_page places the top document over the base document
                doc_base[i].show_pdf_page(doc_base[i].rect, doc_top, i)
                
            st.success("PDFs Overlayed Successfully!")
            st.download_button("Download Overlayed PDF", data=doc_base.write(), file_name="overlayed.pdf", mime="application/pdf")

    elif selected_tool == "Compare PDFs":
        st.subheader("⚖️ Compare PDFs (Text Diff)")
        st.info("Finds the text differences between two documents.")
        comp_pdf1 = st.file_uploader("Upload Original PDF", type="pdf", key="comp1")
        comp_pdf2 = st.file_uploader("Upload Modified PDF", type="pdf", key="comp2")
        
        if st.button("Compare Text", type="primary") and comp_pdf1 and comp_pdf2:
            import difflib
            doc1 = fitz.open(stream=comp_pdf1.read(), filetype="pdf")
            doc2 = fitz.open(stream=comp_pdf2.read(), filetype="pdf")
            
            text1 = "\n".join([page.get_text() for page in doc1]).splitlines()
            text2 = "\n".join([page.get_text() for page in doc2]).splitlines()
            
            diff = list(difflib.unified_diff(text1, text2, lineterm=""))
            
            if not diff:
                st.success("The text in both PDFs is identical!")
            else:
                st.warning("Differences found:")
                diff_text = "\n".join(diff[:100]) # Limit to first 100 lines to prevent crashing on massive diffs
                st.code(diff_text, language="diff")

    elif selected_tool == "Webpage to PDF":
        st.subheader("🌐 Webpage to PDF")
        st.info("Note: This tool requires the 'wkhtmltopdf' software installed on your server.")
        url_input = st.text_input("Enter Website URL", placeholder="https://www.google.com")
        
        if st.button("Convert to PDF", type="primary") and url_input:
            try:
                import pdfkit
                with st.spinner("Fetching webpage and rendering PDF..."):
                    try:
                        # options to ignore load errors for modern websites with heavy JS
                        options = {'quiet': ''} 
                        pdf_bytes = pdfkit.from_url(url_input, False, options=options)
                        st.success("Webpage converted successfully!")
                        st.download_button("Download Web PDF", data=pdf_bytes, file_name="webpage.pdf", mime="application/pdf")
                    except OSError:
                        st.error("System Error: 'wkhtmltopdf' is not installed on this server. This library is required for URL conversions.")
            except ImportError:
                st.error("Python library 'pdfkit' is missing. Please add it to requirements.txt.")
    else:
        st.subheader(selected_tool)
        st.info(f"The logic for **{selected_tool}** is highly complex and requires additional system-level libraries (like `pdf2docx`, `wkhtmltopdf`, or Digital Signature cryptography). We will build this in the next phase!")
elif page == "🖼️ Image":
    st.header("🖼️ Image Studio")
    
    # Organize the 14 tools into 4 clean tabs
    img_tab1, img_tab2, img_tab3, img_tab4 = st.tabs([
        "✂️ Edit & Compress", 
        "✨ AI & Enhance", 
        "🔄 Convert & Collage", 
        "📝 Text & Generators"
    ])
    
    # ==========================================
    # TAB 1: EDIT & COMPRESS
    # ==========================================
    with img_tab1:
        st.subheader("✂️ Crop & Rotate")
        crop_file = st.file_uploader("Upload Image to Crop", type=["jpg", "png", "jpeg", "webp"], key="crop_up")
        if crop_file:
            if not st_cropper:
                st.error("Please add `streamlit-cropper` to your requirements.txt")
            else:
                img = Image.open(crop_file)
                st.write("Drag the box to crop:")
                cropped_img = st_cropper(img, realtime_update=True, box_color='#8b5cf6')
                
                r_col1, r_col2 = st.columns(2)
                with r_col1:
                    if st.button("Rotate 90° Left"): cropped_img = cropped_img.rotate(90, expand=True)
                with r_col2:
                    if st.button("Rotate 90° Right"): cropped_img = cropped_img.rotate(-90, expand=True)
                    
                st.image(cropped_img, caption="Preview")
                buf = io.BytesIO()
                cropped_img.save(buf, format="PNG")
                st.download_button("Download Cropped Image", data=buf.getvalue(), file_name="cropped.png", mime="image/png")

        st.divider()
        st.subheader("Advanced Photo Resizer")
        resize_file = st.file_uploader("Upload Image to Resize", type=["jpg", "png", "jpeg"], key="resize_up")
        if resize_file:
            img = Image.open(resize_file)
            st.write(f"Original Size: {img.width} x {img.height} px")
            rs_col1, rs_col2 = st.columns(2)
            new_w = rs_col1.number_input("New Width (px)", value=img.width)
            new_h = rs_col2.number_input("New Height (px)", value=img.height)
            if st.button("Resize Image"):
                resized = img.resize((int(new_w), int(new_h)))
                buf = io.BytesIO()
                resized.save(buf, format="PNG")
                st.success(f"Resized to {int(new_w)} x {int(new_h)}!")
                st.download_button("Download Resized", data=buf.getvalue(), file_name="resized.png", mime="image/png")

        st.divider()
        st.subheader("Reduce Size (KB/MB)")
        compress_file = st.file_uploader("Upload Image to Compress", type=["jpg", "jpeg", "png"], key="comp_up")
        if compress_file:
            target_kb = st.number_input("Target Size (KB)", min_value=10, value=200)
            if st.button("Compress Image"):
                img = Image.open(compress_file).convert("RGB")
                quality = 95
                buf = io.BytesIO()
                # Iterate to find the right quality
                while quality > 10:
                    buf.seek(0)
                    buf.truncate(0)
                    img.save(buf, format="JPEG", quality=quality)
                    if buf.tell() / 1024 <= target_kb:
                        break
                    quality -= 5
                st.success(f"Compressed to ~{int(buf.tell() / 1024)} KB")
                st.download_button("Download Compressed", data=buf.getvalue(), file_name="compressed.jpg", mime="image/jpeg")

        st.divider()
        st.subheader("🛂 Passport Photo Maker")
        pass_file = st.file_uploader("Upload Photo", type=["jpg", "png", "jpeg"], key="pass_up")
        if pass_file:
            if st.button("Generate Passport Photo (35x45mm ratio)"):
                img = Image.open(pass_file)
                target_ratio = 3.5 / 4.5
                current_ratio = img.width / img.height
                if current_ratio > target_ratio:
                    new_w = int(target_ratio * img.height)
                    left = (img.width - new_w) / 2
                    img = img.crop((left, 0, left + new_w, img.height))
                else:
                    new_h = int(img.width / target_ratio)
                    top = (img.height - new_h) / 2
                    img = img.crop((0, top, img.width, top + new_h))
                buf = io.BytesIO()
                img.save(buf, format="JPEG", dpi=(300, 300))
                st.image(img, width=200, caption="Passport Size Preview")
                st.download_button("Download Passport Photo", data=buf.getvalue(), file_name="passport.jpg", mime="image/jpeg")

    # ==========================================
    # TAB 2: AI & ENHANCE
    # ==========================================
    with img_tab2:
        st.subheader("🎨 AI Background Removal")
        bg_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"], key="bg_up")
        if bg_file:
            if not remove:
                st.error("`rembg` library not installed. Add it to requirements.txt")
            elif st.button("✨ Remove Background", type="primary"):
                with st.spinner("AI is processing the image... (this may take a moment on the first run)"):
                    img_bytes = bg_file.read()
                    result_bytes = remove(img_bytes)
                    st.image(result_bytes, caption="Background Removed")
                    st.download_button("Download PNG", data=result_bytes, file_name="nobg.png", mime="image/png")
        
        st.divider()
        st.subheader("✨ Photo Enhancer")
        enh_file = st.file_uploader("Upload Image to Enhance", type=["jpg", "png", "jpeg"], key="enh_up")
        if enh_file:
            img = Image.open(enh_file)
            e_col1, e_col2 = st.columns(2)
            c = e_col1.slider("Contrast", 0.5, 2.0, 1.2)
            b = e_col2.slider("Brightness", 0.5, 2.0, 1.1)
            s = e_col1.slider("Sharpness", 0.0, 3.0, 1.5)
            col = e_col2.slider("Color Saturation", 0.0, 2.0, 1.2)
            
            # Apply enhancements
            img = ImageEnhance.Contrast(img).enhance(c)
            img = ImageEnhance.Brightness(img).enhance(b)
            img = ImageEnhance.Sharpness(img).enhance(s)
            img = ImageEnhance.Color(img).enhance(col)
            
            st.image(img, caption="Enhanced Preview")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button("Download Enhanced Photo", data=buf.getvalue(), file_name="enhanced.png", mime="image/png")

        st.divider()
        st.subheader("ℹ️ EXIF Metadata Viewer")
        exif_file = st.file_uploader("Upload JPG to read Metadata", type=["jpg", "jpeg"], key="exif_up")
        if exif_file:
            img = Image.open(exif_file)
            exif_data = img._getexif()
            if exif_data:
                exif_dict = {ExifTags.TAGS.get(k, k): str(v) for k, v in exif_data.items() if k in ExifTags.TAGS}
                st.json(exif_dict)
            else:
                st.info("No EXIF metadata found in this image.")

    # ==========================================
    # TAB 3: CONVERT & COLLAGE
    # ==========================================
    with img_tab3:
        st.subheader("🔄 Image Format & DPI Converter")
        conv_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg", "webp", "bmp"], key="conv_up")
        if conv_file:
            c1, c2 = st.columns(2)
            out_format = c1.selectbox("Output Format", ["PNG", "JPEG", "WEBP", "BMP"])
            dpi_val = c2.number_input("Target DPI (e.g., 300 for print)", value=300)
            
            if st.button("Convert Image"):
                img = Image.open(conv_file)
                if out_format == "JPEG" and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB") # JPEGs don't support transparency
                buf = io.BytesIO()
                img.save(buf, format=out_format, dpi=(dpi_val, dpi_val))
                st.success("Conversion Complete!")
                st.download_button(f"Download {out_format}", data=buf.getvalue(), file_name=f"converted.{out_format.lower()}", mime=f"image/{out_format.lower()}")

        st.divider()
        st.subheader("🖼️ Image Collage (Grid)")
        col_files = st.file_uploader("Select 2 to 4 Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True, key="col_up")
        if st.button("Create Collage") and col_files:
            if len(col_files) < 2 or len(col_files) > 4:
                st.warning("Please select exactly 2, 3, or 4 images.")
            else:
                imgs = [Image.open(f).convert("RGB").resize((600, 600)) for f in col_files]
                collage = Image.new("RGB", (1200, 1200), "white")
                if len(imgs) == 2:
                    collage.paste(imgs[0], (0, 300))
                    collage.paste(imgs[1], (600, 300))
                elif len(imgs) == 3:
                    collage.paste(imgs[0], (0, 0))
                    collage.paste(imgs[1], (600, 0))
                    collage.paste(imgs[2], (300, 600))
                else:
                    collage.paste(imgs[0], (0, 0))
                    collage.paste(imgs[1], (600, 0))
                    collage.paste(imgs[2], (0, 600))
                    collage.paste(imgs[3], (600, 600))
                
                st.image(collage, use_container_width=True)
                buf = io.BytesIO()
                collage.save(buf, format="JPEG")
                st.download_button("Download Collage", data=buf.getvalue(), file_name="collage.jpg", mime="image/jpeg")

    # ==========================================
    # TAB 4: TEXT & GENERATORS
    # ==========================================
    with img_tab4:
        st.subheader("📝 OCR (Image to Text)")
        ocr_file = st.file_uploader("Upload Image with Text", type=["jpg", "png", "jpeg"], key="ocr_up")
        if ocr_file:
            if not pytesseract:
                st.error("Please add `pytesseract` to requirements.txt.")
            elif st.button("Extract Text", type="primary"):
                with st.spinner("Scanning for text..."):
                    try:
                        img = Image.open(ocr_file)
                        extracted = pytesseract.image_to_string(img)
                        if extracted.strip():
                            st.text_area("Extracted Text:", value=extracted, height=200)
                        else:
                            st.warning("No text could be found in the image.")
                    except Exception as e:
                        st.error(f"OCR Error: Make sure Tesseract-OCR software is installed on the server. Details: {e}")

        st.divider()
        st.subheader("📅 Add Name & DOB")
        nd_file = st.file_uploader("Upload Photo", type=["jpg", "png", "jpeg"], key="nd_up")
        nd_name = st.text_input("Name")
        nd_dob = st.text_input("Date of Birth")
        if st.button("Generate Photo") and nd_file and nd_name:
            img = Image.open(nd_file)
            # Create white space at the bottom for text
            new_img = Image.new("RGB", (img.width, img.height + 150), "white")
            new_img.paste(img, (0, 0))
            draw = ImageDraw.Draw(new_img)
            try:
                # Try to load a generic truetype font
                font_name = ImageFont.truetype("arial.ttf", int(img.width * 0.08))
                font_dob = ImageFont.truetype("arial.ttf", int(img.width * 0.06))
            except IOError:
                # Fallback to default if arial isn't found
                font_name = ImageFont.load_default()
                font_dob = ImageFont.load_default()

            draw.text((img.width/2, img.height + 40), nd_name, fill="black", anchor="mm", font=font_name)
            draw.text((img.width/2, img.height + 100), f"DOB: {nd_dob}", fill="black", anchor="mm", font=font_dob)
            
            st.image(new_img, width=300)
            buf = io.BytesIO()
            new_img.save(buf, format="JPEG")
            st.download_button("Download Photo", data=buf.getvalue(), file_name="namedob.jpg", mime="image/jpeg")

        st.divider()
        st.subheader("🐸 Meme Generator")
        meme_file = st.file_uploader("Upload Base Image", type=["jpg", "png", "jpeg"], key="meme_up")
        m_top = st.text_input("Top Text").upper()
        m_bot = st.text_input("Bottom Text").upper()
        if st.button("Make Meme") and meme_file:
            img = Image.open(meme_file).convert("RGBA")
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("impact.ttf", int(img.width * 0.1))
            except IOError:
                font = ImageFont.load_default()
                
            draw.text((img.width/2, 20), m_top, fill="white", stroke_width=3, stroke_fill="black", anchor="ma", font=font)
            draw.text((img.width/2, img.height - 20), m_bot, fill="white", stroke_width=3, stroke_fill="black", anchor="md", font=font)
            
            st.image(img)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button("Download Meme", data=buf.getvalue(), file_name="meme.png", mime="image/png")

        st.divider()
        st.subheader("QR Code Maker")
        qr_text = st.text_input("Enter URL or Text for QR Code")
        if st.button("Generate QR") and qr_text:
            qr_img = qrcode.make(qr_text)
            buf = io.BytesIO()
            qr_img.save(buf, format="PNG")
            st.image(qr_img, width=200)
            st.download_button("Download QR", data=buf.getvalue(), file_name="qr.png", mime="image/png")
elif page == "✒️ Signature":
    st.header("✒️ Signature Pad")
    
    sig_tab1, sig_tab2 = st.tabs(["✒️ Create Signature", "📐 Resize Signature"])
    
    # ==========================================
    # TAB 1: CREATE SIGNATURE
    # ==========================================
    with sig_tab1:
        st.subheader("Draw Your Signature")
        
        if not st_canvas:
            st.error("Please add `streamlit-drawable-canvas` to your requirements.txt")
        else:
            # Controls for the canvas
            c1, c2, c3 = st.columns(3)
            stroke_width = c1.slider("Pen Thickness", 1, 10, 3)
            stroke_color = c2.color_picker("Pen Color", "#000000")
            bg_color = c3.color_picker("Background Color", "#FFFFFF")
            
            st.write("Draw inside the box below:")
            
            # The interactive canvas component
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
                stroke_width=stroke_width,
                stroke_color=stroke_color,
                background_color=bg_color,
                update_streamlit=True,
                height=250,
                drawing_mode="freedraw",
                key="signature_canvas",
            )
            
            # If the user has drawn something, give them the option to download it
            if canvas_result.image_data is not None:
                # The canvas returns a numpy array. We convert it to a PIL Image.
                img_data = canvas_result.image_data
                
                # Only show download if the canvas isn't completely blank
                if np.any(img_data != 0): 
                    img = Image.fromarray(img_data.astype('uint8'), 'RGBA')
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    
                    st.download_button(
                        label="Download Signature (PNG)",
                        data=buf.getvalue(),
                        file_name="signature.png",
                        mime="image/png",
                        type="primary"
                    )

    # ==========================================
    # TAB 2: RESIZE SIGNATURE
    # ==========================================
    with sig_tab2:
        st.subheader("Resize Existing Signature")
        sig_file = st.file_uploader("Upload Signature Image", type=["png", "jpg", "jpeg"], key="sig_up")
        
        if sig_file:
            img = Image.open(sig_file)
            st.write(f"Current Size: {img.width} x {img.height} px")
            
            c1, c2 = st.columns(2)
            new_w = c1.number_input("Target Width (px)", value=300)
            new_h = c2.number_input("Target Height (px)", value=100)
            
            if st.button("Resize Signature"):
                resized = img.resize((int(new_w), int(new_h)))
                st.image(resized, caption="Resized Preview")
                
                buf = io.BytesIO()
                resized.save(buf, format="PNG")
                st.download_button(
                    "Download Resized Signature", 
                    data=buf.getvalue(), 
                    file_name="resized_signature.png", 
                    mime="image/png",
                    type="primary"
                )

elif page == "⚖️ Units":
    st.header("⚖️ Universal Unit Converter")
    
    # 1. The Massive Unit Dictionary (Values relative to a base unit)
    unit_data = {
        "Length": {"Meter": 1, "Kilometer": 1000, "Centimeter": 0.01, "Millimeter": 0.001, "Micrometer": 1e-6, "Nanometer": 1e-9, "Inch": 0.0254, "Foot": 0.3048, "Yard": 0.9144, "Mile": 1609.34, "Nautical Mile": 1852},
        "Weight": {"Kilogram": 1, "Gram": 0.001, "Milligram": 1e-6, "Metric Ton": 1000, "Pound": 0.453592, "Ounce": 0.0283495},
        "Area": {"Square Meter": 1, "Square Kilometer": 1e6, "Square Centimeter": 0.0001, "Hectare": 10000, "Acre": 4046.86, "Square Mile": 2.59e6, "Square Foot": 0.092903, "Square Inch": 0.00064516},
        "Volume": {"Liter": 1, "Milliliter": 0.001, "Cubic Meter": 1000, "Gallon (US)": 3.78541, "Quart (US)": 0.946353, "Pint (US)": 0.473176, "Cup": 0.236588},
        "Time": {"Second": 1, "Millisecond": 0.001, "Minute": 60, "Hour": 3600, "Day": 86400, "Week": 604800, "Month (Avg)": 2.628e6, "Year": 3.154e7},
        "Speed": {"Meters per second": 1, "Kilometers per hour": 0.277778, "Miles per hour": 0.44704, "Knot": 0.514444, "Foot per second": 0.3048},
        "Pressure": {"Pascal": 1, "Kilopascal": 1000, "Bar": 100000, "PSI": 6894.76, "Atmosphere": 101325, "Torr": 133.322},
        "Power": {"Watt": 1, "Kilowatt": 1000, "Megawatt": 1e6, "Horsepower": 745.7},
        "Energy": {"Joule": 1, "Kilojoule": 1000, "Calorie": 4.184, "Kilocalorie": 4184, "Watt-hour": 3600, "Kilowatt-hour": 3.6e6, "BTU": 1055.06},
        "Voltage": {"Volt": 1, "Millivolt": 0.001, "Kilovolt": 1000},
        "Current": {"Ampere": 1, "Milliampere": 0.001, "Kiloampere": 1000},
        "Force": {"Newton": 1, "Kilonewton": 1000, "Dyne": 1e-5, "Pound-force": 4.44822},
        "Torque": {"Newton-meter": 1, "Pound-foot": 1.35582},
        "Data Storage": {"Byte": 1, "Kilobyte": 1024, "Megabyte": 1048576, "Gigabyte": 1073741824, "Terabyte": 1099511627776, "Bit": 0.125},
        "Frequency": {"Hertz": 1, "Kilohertz": 1000, "Megahertz": 1e6, "Gigahertz": 1e9},
        "Angle": {"Degree": 1, "Radian": 57.2958, "Gradian": 0.9},
        "Density": {"Kg per cubic meter": 1, "Gram per cubic cm": 1000, "Pound per cubic foot": 16.0185},
        "Temperature": ["Celsius", "Fahrenheit", "Kelvin"] # Temperature requires custom math, not multipliers
    }

    # 2. UI Layout
    st.markdown("### Select Conversion Type")
    category = st.selectbox("Category", list(unit_data.keys()), label_visibility="collapsed")
    
    st.divider()
    
    # Dynamically load the correct units based on the chosen category
    if category == "Temperature":
        available_units = unit_data["Temperature"]
    else:
        available_units = list(unit_data[category].keys())

    col1, col2 = st.columns(2)
    with col1:
        val = st.number_input("Enter Value", value=1.0, step=0.1)
        from_unit = st.selectbox("From Unit", available_units, key="from_unit")
        
    with col2:
        # Empty space to align the button and selectbox nicely
        st.write("") 
        st.write("")
        to_unit = st.selectbox("To Unit", available_units, key="to_unit", index=1 if len(available_units) > 1 else 0)

    # 3. Calculation Logic
    if st.button("🔄 Convert", type="primary", use_container_width=True):
        if category == "Temperature":
            # Custom logic for temperature conversions
            if from_unit == to_unit:
                result = val
            elif from_unit == "Celsius" and to_unit == "Fahrenheit":
                result = (val * 9/5) + 32
            elif from_unit == "Celsius" and to_unit == "Kelvin":
                result = val + 273.15
            elif from_unit == "Fahrenheit" and to_unit == "Celsius":
                result = (val - 32) * 5/9
            elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
                result = (val - 32) * 5/9 + 273.15
            elif from_unit == "Kelvin" and to_unit == "Celsius":
                result = val - 273.15
            elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
                result = (val - 273.15) * 9/5 + 32
                
            st.success(f"### {val:,.2f} {from_unit} = {result:,.2f} {to_unit}")
            
        else:
            # Standard multiplier logic for all other units
            # Convert the input to the base unit, then divide by the target unit's base value
            base_value = val * unit_data[category][from_unit]
            result = base_value / unit_data[category][to_unit]
            
            # Use smart formatting to avoid ugly scientific notation on normal numbers
            if result < 0.0001 or result > 1000000:
                st.success(f"### {val:,.4f} {from_unit} = {result:.4e} {to_unit}")
            else:
                st.success(f"### {val:,.4f} {from_unit} = {result:,.4f} {to_unit}")

elif page == "🎓 Education":
    st.header("🎓 Education & Math Tools")
    
    edu_tab1, edu_tab2, edu_tab3, edu_tab4, edu_tab5, edu_tab6 = st.tabs([
        "🔢 Basic Math", "✖️ Algebra", "📐 Geometry", "📊 Statistics", "🎓 Grades & CGPA", "🔄 Converters"
    ])
    
  # ==========================================
    # TAB 1: BASIC MATH & CALCULATOR
    # ==========================================
    with edu_tab1:
        st.subheader("🧮 Scientific Calculator")
        
        # Initialize session state to remember button clicks
        if "calc_input" not in st.session_state:
            st.session_state.calc_input = ""
            
        def button_click(val):
            # If it currently says Error, clear it first before typing
            if st.session_state.calc_input == "Error":
                st.session_state.calc_input = ""
            st.session_state.calc_input += str(val)
            
        def calculate_result():
            import math # Imported directly here so it never fails!
            try:
                # Replace UI symbols with Python math operators
                expr = st.session_state.calc_input.replace('×', '*').replace('÷', '/')
                expr = expr.replace('^', '**')
                
                # AUTO-FIX: Automatically close missing parentheses
                open_p = expr.count('(')
                close_p = expr.count(')')
                if open_p > close_p:
                    expr += ')' * (open_p - close_p)
                
                # Create a safe execution environment using Python's math module
                safe_dict = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
                safe_dict["__builtins__"] = None
                
                result = eval(expr, safe_dict)
                
                # Clean up display: remove .0 if it's a clean integer
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                    
                st.session_state.calc_input = str(result)
            except Exception:
                st.session_state.calc_input = "Error"
                
        def clear_calc():
            st.session_state.calc_input = ""

        # Custom HTML Display Screen (Immune to Streamlit state glitches)
        display_text = st.session_state.calc_input if st.session_state.calc_input != "" else "0"
        st.markdown(f"""
            <div style="background-color: #f8fafc; padding: 20px; border-radius: 12px; border: 2px solid #cbd5e1; text-align: right; font-size: 2.5rem; font-family: monospace; min-height: 90px; margin-bottom: 20px; color: #1e293b; box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);">
                {display_text}
            </div>
        """, unsafe_allow_html=True)
        
        # Custom CSS to make the calculator buttons look uniform
        st.markdown("""
            <style>
            div[data-testid="column"] button { width: 100%; font-size: 1.2rem; font-weight: bold; height: 3.5rem; }
            </style>
        """, unsafe_allow_html=True)
        
        # Button Grid Layout (5 columns)
        r1_c1, r1_c2, r1_c3, r1_c4, r1_c5 = st.columns(5)
        r2_c1, r2_c2, r2_c3, r2_c4, r2_c5 = st.columns(5)
        r3_c1, r3_c2, r3_c3, r3_c4, r3_c5 = st.columns(5)
        r4_c1, r4_c2, r4_c3, r4_c4, r4_c5 = st.columns(5)
        r5_c1, r5_c2, r5_c3, r5_c4, r5_c5 = st.columns(5)
        
        # Row 1
        with r1_c1: st.button("AC", on_click=clear_calc, type="primary")
        with r1_c2: st.button("(", on_click=button_click, args=("(",))
        with r1_c3: st.button(")", on_click=button_click, args=(")",))
        with r1_c4: st.button("÷", on_click=button_click, args=("÷",))
        with r1_c5: st.button("sin", on_click=button_click, args=("sin(",))
        
        # Row 2
        with r2_c1: st.button("7", on_click=button_click, args=("7",))
        with r2_c2: st.button("8", on_click=button_click, args=("8",))
        with r2_c3: st.button("9", on_click=button_click, args=("9",))
        with r2_c4: st.button("×", on_click=button_click, args=("×",))
        with r2_c5: st.button("cos", on_click=button_click, args=("cos(",))
        
        # Row 3
        with r3_c1: st.button("4", on_click=button_click, args=("4",))
        with r3_c2: st.button("5", on_click=button_click, args=("5",))
        with r3_c3: st.button("6", on_click=button_click, args=("6",))
        with r3_c4: st.button("-", on_click=button_click, args=("-",))
        with r3_c5: st.button("tan", on_click=button_click, args=("tan(",))
        
        # Row 4
        with r4_c1: st.button("1", on_click=button_click, args=("1",))
        with r4_c2: st.button("2", on_click=button_click, args=("2",))
        with r4_c3: st.button("3", on_click=button_click, args=("3",))
        with r4_c4: st.button("+", on_click=button_click, args=("+",))
        with r4_c5: st.button("log", on_click=button_click, args=("log10(",))
        
        # Row 5
        with r5_c1: st.button("0", on_click=button_click, args=("0",))
        with r5_c2: st.button(".", on_click=button_click, args=(".",))
        with r5_c3: st.button("π", on_click=button_click, args=("pi",))
        with r5_c4: st.button("=", on_click=calculate_result, type="primary")
        with r5_c5: st.button("√", on_click=button_click, args=("sqrt(",))

        st.divider()
        st.subheader("General Percentage (What is X% of Y?)")
        p_col1, p_col2 = st.columns(2)
        perc_val = p_col1.number_input("What is (%)", value=20.0, step=1.0)
        perc_tot = p_col2.number_input("of (Total)", value=100.0, step=10.0)
        if st.button("Calculate Percentage"):
            st.success(f"### {perc_val}% of {perc_tot} is {(perc_val / 100) * perc_tot:,.2f}")

    # ==========================================
    # TAB 2: ALGEBRA
    # ==========================================
    with edu_tab2:
        st.subheader("Number Properties (Factors, Prime)")
        num_prop = st.number_input("Enter Integer", min_value=1, value=12, step=1)
        if st.button("Analyze Number"):
            factors = [i for i in range(1, num_prop + 1) if num_prop % i == 0]
            is_prime = len(factors) == 2
            st.info(f"**Factors:** {', '.join(map(str, factors))}")
            st.info(f"**Is Prime?** {'Yes ✅' if is_prime else 'No ❌'}")
            
        st.divider()
        st.subheader("GCD (HCF) & LCM")
        gcd_in = st.text_input("Enter numbers separated by commas (e.g., 12, 18, 24)", value="12, 18, 24")
        if st.button("Calculate GCD & LCM"):
            try:
                nums = [int(x.strip()) for x in gcd_in.split(",")]
                res_gcd = math.gcd(*nums)
                res_lcm = math.lcm(*nums)
                st.success(f"**GCD (HCF):** {res_gcd}  |  **LCM:** {res_lcm}")
            except Exception:
                st.error("Please enter valid integers separated by commas.")

        st.divider()
        st.subheader("Quadratic Equation Solver (ax² + bx + c = 0)")
        q_c1, q_c2, q_c3 = st.columns(3)
        q_a = q_c1.number_input("a", value=1.0)
        q_b = q_c2.number_input("b", value=-5.0)
        q_c = q_c3.number_input("c", value=6.0)
        if st.button("Solve Equation"):
            if q_a == 0:
                st.error("'a' cannot be zero.")
            else:
                d = (q_b**2) - (4*q_a*q_c)
                sol1 = (-q_b - cmath.sqrt(d)) / (2*q_a)
                sol2 = (-q_b + cmath.sqrt(d)) / (2*q_a)
                # Format to remove complex part if it's real
                s1_str = f"{sol1.real:.2f}" if sol1.imag == 0 else f"{sol1.real:.2f} + {sol1.imag:.2f}i"
                s2_str = f"{sol2.real:.2f}" if sol2.imag == 0 else f"{sol2.real:.2f} + {sol2.imag:.2f}i"
                st.success(f"**Roots:** x₁ = {s1_str}, x₂ = {s2_str}")

    # ==========================================
    # TAB 3: GEOMETRY
    # ==========================================
    with edu_tab3:
        shape = st.selectbox("Select Shape", ["Circle", "Right Triangle", "Rectangle", "Triangle"])
        if shape == "Circle":
            r = st.number_input("Radius (r)", min_value=0.0, value=5.0)
            if st.button("Calculate Circle"):
                st.info(f"**Area:** {math.pi * (r**2):.2f} | **Circumference:** {2 * math.pi * r:.2f}")
        elif shape == "Right Triangle":
            st.caption("Pythagorean Theorem: a² + b² = c²")
            g_c1, g_c2 = st.columns(2)
            a = g_c1.number_input("Side a", min_value=0.0, value=3.0)
            b = g_c2.number_input("Side b", min_value=0.0, value=4.0)
            if st.button("Find Hypotenuse (c)"):
                st.info(f"**Hypotenuse (c):** {math.sqrt(a**2 + b**2):.2f}")
        elif shape == "Rectangle":
            g_c1, g_c2 = st.columns(2)
            l = g_c1.number_input("Length", min_value=0.0, value=10.0)
            w = g_c2.number_input("Width", min_value=0.0, value=5.0)
            if st.button("Calculate Rectangle"):
                st.info(f"**Area:** {l * w:.2f} | **Perimeter:** {2 * (l + w):.2f}")
        elif shape == "Triangle":
            g_c1, g_c2 = st.columns(2)
            base = g_c1.number_input("Base", min_value=0.0, value=10.0)
            height = g_c2.number_input("Height", min_value=0.0, value=5.0)
            if st.button("Calculate Triangle Area"):
                st.info(f"**Area:** {0.5 * base * height:.2f}")

    # ==========================================
    # TAB 4: STATISTICS
    # ==========================================
    with edu_tab4:
        st.subheader("Descriptive Statistics")
        stats_in = st.text_area("Enter Dataset (comma separated)", value="12, 5, 7, 12, 9, 15, 21")
        if st.button("Calculate Statistics"):
            try:
                arr = sorted([float(x.strip()) for x in stats_in.split(",")])
                if not arr: raise ValueError
                st.markdown(f"""
                * **Count:** {len(arr)}
                * **Sum:** {sum(arr):.2f}
                * **Mean (Average):** {statistics.mean(arr):.2f}
                * **Median:** {statistics.median(arr)}
                * **Mode:** {statistics.mode(arr)}
                * **Range:** {max(arr) - min(arr)}
                * **Standard Deviation:** {statistics.stdev(arr) if len(arr) > 1 else 0:.2f}
                * **Sorted Data:** {arr}
                """)
            except Exception:
                st.error("Please enter valid numbers separated by commas.")

    # ==========================================
    # TAB 5: GRADES & CGPA
    # ==========================================
    with edu_tab5:
        st.subheader("📝 Exam Percentage Calculator")
        gr_c1, gr_c2 = st.columns(2)
        obt = gr_c1.number_input("Marks Obtained", min_value=0.0, value=450.0)
        tot = gr_c2.number_input("Total Marks", min_value=1.0, value=500.0)
        if st.button("Calculate Exam Percentage"):
            st.success(f"### Score: {(obt / tot) * 100:.2f}%")

        st.divider()
        st.subheader("🎓 CGPA Calculator")
        st.caption("Edit the table below to add your subjects.")
        
        # Using Pandas & Streamlit Data Editor for a highly interactive grid!
        default_cgpa_data = pd.DataFrame([{"Credit": 3.0, "Grade Point": 8.0}, {"Credit": 4.0, "Grade Point": 9.0}])
        edited_df = st.data_editor(default_cgpa_data, num_rows="dynamic", use_container_width=True)
        
        if st.button("Calculate CGPA"):
            total_credits = edited_df["Credit"].sum()
            total_points = (edited_df["Credit"] * edited_df["Grade Point"]).sum()
            if total_credits > 0:
                st.success(f"### Your CGPA is: {total_points / total_credits:.2f}")
            else:
                st.warning("Total credits cannot be zero.")

        st.divider()
        st.subheader("🔄 CGPA to Percentage Converter")
        cg_c1, cg_c2 = st.columns(2)
        cgpa_val = cg_c1.number_input("CGPA", min_value=0.0, value=8.5, step=0.1)
        cgpa_mult = cg_c2.number_input("Multiplier (e.g., 9.5)", min_value=0.0, value=9.5, step=0.1)
        if st.button("Convert to Percentage"):
            st.info(f"### Percentage: {cgpa_val * cgpa_mult:.2f}%")

    # ==========================================
    # TAB 6: CONVERTERS
    # ==========================================
    with edu_tab6:
        st.subheader("Number Base Converter")
        base_val = st.text_input("Enter a Decimal Number to convert:", value="255")
        if st.button("Convert Bases"):
            try:
                dec = int(base_val)
                c1, c2, c3 = st.columns(3)
                c1.metric("Decimal", str(dec))
                c2.metric("Binary", bin(dec)[2:])
                c3.metric("Hexadecimal", hex(dec)[2:].upper())
            except ValueError:
                st.error("Please enter a valid integer.")
                
        st.divider()
        st.subheader("Scientific Notation")
        sci_val = st.number_input("Number to convert", value=1234567.89)
        if st.button("Convert to Notation"):
            st.info(f"### {sci_val:e}")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 convertnext.in | Powered by Streamlit")
