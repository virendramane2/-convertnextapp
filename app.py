import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image, ImageDraw
import fitz  # PyMuPDF
from google import genai
import qrcode
import io
import yfinance as yf
import secrets
import string
import base64
import zipfile
import json

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="convertnext.in - Ultimate Next-Gen Utility Suite", 
    layout="wide", 
    page_icon="⚡"
)

# --- BRANDING & SEO ---
st.markdown("""
    <style>
    .stApp { background: #f8fafc; }
    .main-title { 
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        font-size: 3.5rem; font-weight: 800; text-align: center; padding: 10px;
    }
    .sub-header { color: #475569; text-align: center; margin-bottom: 20px; font-weight: 500; font-size: 1.2rem; }
    </style>
    <div class="main-title">𝕔𝕠𝕟𝕧𝕖𝕣𝕥𝕟𝕖𝕩𝕥.𝕚𝕟</div>
    <div class="sub-header">Advanced Document, Image, AI & Finance Hub</div>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://placehold.co/200x50/6366f1/ffffff?text=ConvertNext", use_container_width=True)
menu = st.sidebar.selectbox("Main Tool Category", 
    ["📄 PDF Pro", "🖼️ Image Lab", "🤖 AI Lab", "🔠 Text Tools", "⚖️ Units & Measurements", "💰 Finance & Stocks", "🔥 Student & Pro Hub", "🎯 Why ConvertNext?"])

api_key = st.sidebar.text_input("Gemini API Key", type="password", placeholder="Enter key for AI tools")

# --- 1. PDF PRO ---
elif page == "📄 PDF":
    st.header("📄 PDF Management")
    
    pdf_tab1, pdf_tab2, pdf_tab3, pdf_tab4 = st.tabs(["Merge & Split", "Text Extraction", "Images to PDF", "PDF to Images"])
    
    # --- 1. MERGE & SPLIT ---
    with pdf_tab1:
        st.subheader("Merge PDFs")
        uploaded_pdfs = st.file_uploader("Upload 2 or more PDFs to merge", type="pdf", accept_multiple_files=True, key="merge_up")
        
        if st.button("Merge Files", type="primary") and uploaded_pdfs:
            if len(uploaded_pdfs) < 2:
                st.warning("Please upload at least 2 PDFs to merge.")
            else:
                merged_pdf = fitz.open()
                for pdf_file in uploaded_pdfs:
                    # Open each uploaded file from memory
                    pdf_doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
                    merged_pdf.insert_pdf(pdf_doc)
                
                # Save to bytes for downloading
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

    # --- 2. TEXT EXTRACTION & AI ---
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
                    response = model.generate_content(f"Analyze this document and provide a detailed summary and key takeaways: {extracted_text[:10000]}") # Limiting text to prevent token overflow
                    st.markdown("### AI Analysis")
                    st.write(response.text)

    # --- 3. IMAGES TO PDF ---
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
                # Save first image, append the rest
                images[0].save(pdf_bytes, format="PDF", save_all=True, append_images=images[1:])
                st.success("PDF generated from images!")
                st.download_button("Download Image PDF", data=pdf_bytes.getvalue(), file_name="images_convertnext.pdf", mime="application/pdf")

    # --- 4. PDF TO IMAGES ---
    with pdf_tab4:
        st.subheader("Render PDF Pages as Images")
        pdf_to_render = st.file_uploader("Upload PDF", type="pdf", key="pdf_to_img")
        scale = st.slider("Quality Scale (Higher = Better quality, larger file)", min_value=1.0, max_value=4.0, value=2.0, step=0.5)
        
        if st.button("Convert to Images") and pdf_to_render:
            doc = fitz.open(stream=pdf_to_render.read(), filetype="pdf")
            # Create a zoom matrix for higher quality rendering
            mat = fitz.Matrix(scale, scale) 
            
            img_cols = st.columns(3) # Display images in a grid
            
            for i, page in enumerate(doc):
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                
                with img_cols[i % 3]:
                    st.image(img_data, caption=f"Page {i+1}", use_container_width=True)
                    st.download_button(f"⬇️ Page {i+1}", data=img_data, file_name=f"page_{i+1}.png", mime="image/png", key=f"dl_img_{i}")

# --- 2. IMAGE LAB (COMPREHENSIVE) ---
elif menu == "🖼️ Image Lab":
    st.header("Professional Image Management")
    i_tab = st.tabs(["Background & Format", "Resize & KB Reduction", "Passport Maker Pro", "DPI & Advanced"])

    with i_tab[0]:
        st.subheader("Remove Background & Convert Formats")
        img_f = st.file_uploader("Upload Photo", type=["jpg","png","jpeg","webp"])
        col1, col2 = st.columns(2)
        
        if img_f:
            if col1.button("Remove Background Free"):
                with st.spinner("AI Removing Background..."):
                    from rembg import remove
                    res = remove(img_f.read())
                    st.image(res, use_container_width=True)
                    st.download_button("Download PNG", res, "no-bg.png")
            
            target = col2.selectbox("Convert JPG to PNG / WebP", ["PNG", "JPEG", "WEBP"])
            if col2.button("Convert Image"):
                img = Image.open(img_f)
                if target == "JPEG": img = img.convert("RGB")
                out = io.BytesIO(); img.save(out, format=target)
                st.download_button(f"Download {target}", out.getvalue(), f"img.{target.lower()}")

    with i_tab[1]:
        st.subheader("Resize & Reduce Image Size (KB)")
        rs_file = st.file_uploader("Upload Image to Compress", type=["jpg","png"], key="rs")
        if rs_file:
            img = Image.open(rs_file)
            col1, col2 = st.columns(2)
            w_target = col1.number_input("Target Width (Pixels)", value=img.size[0])
            qual = col2.slider("Quality (KB Reducer)", 10, 100, 80)
            if st.button("Process Resize"):
                h_target = int((w_target / img.size[0]) * img.size[1])
                img = img.resize((w_target, h_target), Image.Resampling.LANCZOS)
                out = io.BytesIO(); img.save(out, format="JPEG", quality=qual)
                st.image(out.getvalue(), caption=f"Optimized Preview")
                st.download_button("Download Optimized JPG", out.getvalue(), "optimized.jpg")

    with i_tab[2]:
        st.subheader("Passport Photo Maker Guide")
        pass_f = st.file_uploader("Upload Portrait", type=["jpg","png"])
        p_name = st.text_input("Name on Photo")
        p_dob = st.text_input("DOB on Photo")
        if pass_f and st.button("Add Name & DOB to Photo"):
            img = Image.open(pass_f).resize((350, 450))
            draw = ImageDraw.Draw(img)
            draw.rectangle([0, 390, 350, 450], fill="white")
            draw.text((20, 400), f"NAME: {p_name.upper()}", fill="black")
            draw.text((20, 420), f"DOB: {p_dob}", fill="black")
            st.image(img)
            out = io.BytesIO(); img.save(out, format="JPEG")
            st.download_button("Download Passport Photo", out.getvalue(), "passport.jpg")

# --- 3. AI LAB (GEMINI POWERED) ---
elif menu == "🤖 AI Lab":
    st.header("AI Intelligence Laboratory")
    if api_key:
        client = genai.Client(api_key=api_key)
        mode = st.selectbox("Select AI Tool", ["Generate AI Images (Free)", "AI Text Summarizer", "Improve Writing", "Photo to HD Guide", "Social Media Enhancement"])
        user_in = st.text_area("What should the AI do?")
        if st.button("✨ Execute AI"):
            with st.spinner("AI Thinking..."):
                resp = client.models.generate_content(model="gemini-2.0-flash", contents=f"{mode}: {user_in}")
                st.markdown(resp.text)
    else: st.warning("Enter Gemini API Key in sidebar")

# --- 4. TEXT TOOLS ---
elif menu == "🔠 Text Tools":
    st.header("Smart Text Utilities")
    t_in = st.text_area("Input Text")
    col1, col2, col3 = st.columns(3)
    if col1.button("UPPER/lower Case"): st.code(f"UPPER: {t_in.upper()}\nlower: {t_in.lower()}")
    if col2.button("Format JSON"):
        try: st.json(json.loads(t_in))
        except: st.error("Invalid JSON")
    if col3.button("Text to Base64"): st.code(base64.b64encode(t_in.encode()).decode())

# --- 5. MEASUREMENTS ---
elif menu == "⚖️ Units & Measurements":
    st.header("Global Unit Converters")
    val = st.number_input("Value")
    opt = st.selectbox("Type", ["cm to Inches", "Inches to cm", "Celsius to Fahrenheit", "Kg to Pounds"])
    if st.button("Convert"):
        if "cm to Inches" in opt: st.success(f"{val/2.54:.2f} inches")
        if "Kg to Pounds" in opt: st.success(f"{val*2.204:.2f} lbs")

# --- 6. FINANCE ---
elif menu == "💰 Finance & Stocks":
    st.header("Financial Intelligence")
    f_mode = st.radio("Tool", ["EMI Calculator", "New Income Tax Slabs (India)", "Compound Interest", "USD to INR"], horizontal=True)
    if f_mode == "EMI Calculator":
        p = st.number_input("Loan Amount", 100000); r = st.number_input("Rate %", 8.5); y = st.slider("Years", 1, 30, 5)
        m_r = r/1200; n = y*12
        emi = (p * m_r * (1+m_r)**n) / ((1+m_r)**n - 1)
        st.metric("Monthly EMI", f"₹{emi:.2f}")

# --- 7. STUDENT HUB ---
elif menu == "🔥 Student & Pro Hub":
    st.header("Productivity Tools for Students & Work-from-Home")
    st.markdown("""
    - **Free Mobile Tools:** Every mobile user must know these no-install web tools.
    - **Study Faster:** Use the AI Summarizer to condense long notes.
    - **Resume Ready:** Use the PDF Compressor to meet university portal size limits.
    - **Safe File Reducer:** Reduce file size without losing quality for free.
    """)

# --- 8. ABOUT ---
elif menu == "🎯 Why ConvertNext?":
    st.header("Why convertnext.in is the Best All-in-One Tool Site")
    st.write("We process files on the client-side or use temporary memory, meaning your files stay secure. We use AI to simplify complex work like writing, resizing, and tax calculation.")
    st.info("Best AI Websites to Use in 2026: ConvertNext leads with privacy.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write("© 2026 **convertnext.in**")
st.sidebar.caption("Made with ♥ by Virendra Mane")
