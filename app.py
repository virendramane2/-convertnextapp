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
    
    fin_tab1, fin_tab2, fin_tab3 = st.tabs(["Loan EMI", "Compound Interest", "🇮🇳 Tax (FY 25-26)"])
    
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

elif page == "📄 PDF":
    st.header("📄 PDF Management")
    
    pdf_tab1, pdf_tab2, pdf_tab3, pdf_tab4 = st.tabs(["Merge & Split", "Text Extraction", "Images to PDF", "PDF to Images"])
    
    with pdf_tab1:
        st.subheader("Merge PDFs")
        uploaded_pdfs = st.file_uploader("Upload 2 or more PDFs to merge", type="pdf", accept_multiple_files=True, key="merge_up")
        
        if st.button("Merge Files", type="primary") and uploaded_pdfs:
            if len(uploaded_pdfs) < 2:
                st.warning("Please upload at least 2 PDFs to merge.")
            else:
                merged_pdf = fitz.open()
                for pdf_file in uploaded_pdfs:
                    pdf_doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
                    merged_pdf.insert_pdf(pdf_doc)
                
                pdf_bytes = merged_pdf.write()
                st.success("PDFs merged successfully!")
                st.download_button("Download Merged PDF", data=pdf_bytes, file_name="merged_convertnext.pdf", mime="application/pdf")

        st.divider()
        
        st.subheader("Split PDF")
        split_pdf = st.file_uploader("Upload 1 PDF to split into individual pages", type="pdf", key="split_up")
        if st.button("Split PDF") and split_pdf:
            doc = fitz.open(stream=split_pdf.read(), filetype="pdf")
            for page_num in range(len(doc)):
                new_doc = fitz.open()
                new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
                st.download_button(
                    f"Download Page {page_num + 1}", 
                    data=new_doc.write(), 
                    file_name=f"page_{page_num + 1}.pdf", 
                    mime="application/pdf",
                    key=f"dl_page_{page_num}"
                )

    with pdf_tab2:
        st.subheader("Extract Text from PDF")
        extract_pdf = st.file_uploader("Upload PDF for text extraction", type="pdf", key="ext_up")
        
        if extract_pdf:
            doc = fitz.open(stream=extract_pdf.read(), filetype="pdf")
            extracted_text = ""
            for page in doc:
                extracted_text += page.get_text() + "\n\n"
                
            st.text_area("Extracted Text:", value=extracted_text, height=300)
            
            if api_key and st.button("✨ Analyze with AI", type="primary"):
                with st.spinner("Analyzing document..."):
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content(f"Analyze this document and provide a detailed summary and key takeaways: {extracted_text[:10000]}")
                    st.markdown("### AI Analysis")
                    st.write(response.text)

    with pdf_tab3:
        st.subheader("Convert Images to a single PDF")
        img_files = st.file_uploader("Select Images (JPG, PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="img_to_pdf")
        
        if st.button("Generate PDF") and img_files:
            images = []
            for img_file in img_files:
                img = Image.open(img_file).convert("RGB")
                images.append(img)
                
            if images:
                pdf_bytes = io.BytesIO()
                images[0].save(pdf_bytes, format="PDF", save_all=True, append_images=images[1:])
                st.success("PDF generated from images!")
                st.download_button("Download Image PDF", data=pdf_bytes.getvalue(), file_name="images_convertnext.pdf", mime="application/pdf")

    with pdf_tab4:
        st.subheader("Render PDF Pages as Images")
        pdf_to_render = st.file_uploader("Upload PDF", type="pdf", key="pdf_to_img")
        scale = st.slider("Quality Scale", min_value=1.0, max_value=4.0, value=2.0, step=0.5)
        
        if st.button("Convert to Images") and pdf_to_render:
            doc = fitz.open(stream=pdf_to_render.read(), filetype="pdf")
            mat = fitz.Matrix(scale, scale) 
            
            img_cols = st.columns(3) 
            for i, page in enumerate(doc):
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                
                with img_cols[i % 3]:
                    st.image(img_data, caption=f"Page {i+1}", use_container_width=True)
                    st.download_button(f"⬇️ Page {i+1}", data=img_data, file_name=f"page_{i+1}.png", mime="image/png", key=f"dl_img_{i}")

elif page == "🖼️ Image":
    st.header("🖼️ Image Studio")
    
    img_tab1, img_tab2, img_tab3, img_tab4 = st.tabs(["✂️ Edit & Compress", "✨ AI & Enhance", "🔄 Convert & Collage", "📝 Text & Generators"])
    
    # --- TAB 1: EDIT & COMPRESS ---
    with img_tab1:
        st.subheader("✂️ Crop & Rotate")
        crop_file = st.file_uploader("Upload Image to Crop", type=["jpg", "png", "jpeg"], key="crop_up")
        if crop_file and st_cropper:
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
            st.write(f"Original Size: {img.width}x{img.height} px")
            rs_col1, rs_col2 = st.columns(2)
            new_w = rs_col1.number_input("New Width (px)", value=img.width)
            new_h = rs_col2.number_input("New Height (px)", value=img.height)
            if st.button("Resize Image"):
                resized = img.resize((int(new_w), int(new_h)))
                buf = io.BytesIO()
                resized.save(buf, format="PNG")
                st.success(f"Resized to {int(new_w)}x{int(new_h)}!")
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
                while quality > 10:
                    buf.seek(0)
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
                # Standard aspect ratio for passport is usually 3.5 x 4.5
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
                st.image(img, width=200)
                st.download_button("Download Passport Photo", data=buf.getvalue(), file_name="passport.jpg", mime="image/jpeg")

    # --- TAB 2: AI & ENHANCE ---
    with img_tab2:
        st.subheader("🎨 AI Background Removal")
        bg_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"], key="bg_up")
        if bg_file:
            if not remove:
                st.error("rembg library not installed. Add it to requirements.txt")
            elif st.button("✨ Remove Background", type="primary"):
                with st.spinner("AI is processing the image..."):
                    img_bytes = bg_file.read()
                    result_bytes = remove(img_bytes)
                    st.image(result_bytes, caption="Background Removed")
                    st.download_button("Download PNG", data=result_bytes, file_name="nobg.png", mime="image/png")
        
        st.divider()
        st.subheader("✨ Photo Enhancer")
        enh_file = st.file_uploader("Upload Image to Enhance", type=["jpg", "png", "jpeg"], key="enh_up")
        if enh_file:
            img = Image.open(enh_file)
            e_col1, e_col2, e_col3, e_col4 = st.columns(4)
            c = e_col1.slider("Contrast", 0.5, 2.0, 1.0)
            b = e_col2.slider("Brightness", 0.5, 2.0, 1.0)
            s = e_col3.slider("Sharpness", 0.0, 3.0, 1.0)
            col = e_col4.slider("Color", 0.0, 2.0, 1.0)
            
            img = ImageEnhance.Contrast(img).enhance(c)
            img = ImageEnhance.Brightness(img).enhance(b)
            img = ImageEnhance.Sharpness(img).enhance(s)
            img = ImageEnhance.Color(img).enhance(col)
            
            st.image(img)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button("Download Enhanced", data=buf.getvalue(), file_name="enhanced.png", mime="image/png")

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
                st.info("No EXIF data found in this image.")

    # --- TAB 3: CONVERT & COLLAGE ---
    with img_tab3:
        st.subheader("🔄 Image Format & DPI Converter")
        conv_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg", "webp", "bmp"], key="conv_up")
        if conv_file:
            c1, c2 = st.columns(2)
            out_format = c1.selectbox("Output Format", ["PNG", "JPEG", "WEBP", "BMP"])
            dpi_val = c2.number_input("Target DPI", value=300)
            
            if st.button("Convert Image"):
                img = Image.open(conv_file)
                if out_format == "JPEG" and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
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

    # --- TAB 4: TEXT & GENERATORS ---
    with img_tab4:
        st.subheader("📅 Add Name & DOB")
        nd_file = st.file_uploader("Upload Photo", type=["jpg", "png", "jpeg"], key="nd_up")
        nd_name = st.text_input("Name")
        nd_dob = st.text_input("Date of Birth")
        if st.button("Generate Photo") and nd_file and nd_name:
            img = Image.open(nd_file)
            new_img = Image.new("RGB", (img.width, img.height + 150), "white")
            new_img.paste(img, (0, 0))
            draw = ImageDraw.Draw(new_img)
            # Use default font, scaled up roughly
            draw.text((img.width/2, img.height + 30), nd_name, fill="black", anchor="mm", font=ImageFont.load_default(size=40))
            draw.text((img.width/2, img.height + 90), f"DOB: {nd_dob}", fill="black", anchor="mm", font=ImageFont.load_default(size=30))
            
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
            img = Image.open(meme_file)
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default(size=int(img.width * 0.08))
            draw.text((img.width/2, 20), m_top, fill="white", stroke_width=2, stroke_fill="black", anchor="ma", font=font)
            draw.text((img.width/2, img.height - 20), m_bot, fill="white", stroke_width=2, stroke_fill="black", anchor="md", font=font)
            st.image(img)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button("Download Meme", data=buf.getvalue(), file_name="meme.png", mime="image/png")

        st.divider()
        st.subheader("QR Code Maker")
        qr_text = st.text_input("Enter URL or Text for QR Code")
        if st.button("Generate QR"):
            qr_img = qrcode.make(qr_text)
            buf = io.BytesIO()
            qr_img.save(buf, format="PNG")
            st.image(qr_img, width=200)
            st.download_button("Download QR", data=buf.getvalue(), file_name="qr.png", mime="image/png")

        st.divider()
        st.subheader("📝 OCR (Image to Text)")
        ocr_file = st.file_uploader("Upload Image with Text", type=["jpg", "png", "jpeg"], key="ocr_up")
        if st.button("Extract Text") and ocr_file:
            with st.spinner("Extracting text..."):
                try:
                    img = Image.open(ocr_file)
                    extracted = pytesseract.image_to_string(img)
                    st.text_area("Extracted Text:", value=extracted, height=200)
                except Exception as e:
                    st.error("Tesseract-OCR is not installed on the system. Please ensure the Tesseract binary is installed on your server.")

elif page == "✒️ Signature":
    st.header("✒️ Signature Pad")
    st.info("Coming soon: Streamlit-drawable-canvas integration.")

elif page == "⚖️ Units":
    st.header("⚖️ Unit Converter")
    st.info("Coming soon: Unit conversion dictionary logic.")

elif page == "🎓 Education":
    st.header("🎓 Education & Math Tools")
    st.info("Coming soon: Education calculators.")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 convertnext.in | Powered by Streamlit")
