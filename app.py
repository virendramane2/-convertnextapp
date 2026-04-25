import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image
import fitz  # PyMuPDF for PDF to Image conversion
from google import genai
import qrcode
import io
import yfinance as yf
from rembg import remove
import secrets
import string
import base64
import zipfile

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="convertnext.in - Ultimate All-in-One Suite", 
    layout="wide", 
    page_icon="⚡"
)

# --- BRANDING ---
st.markdown("""
    <style>
    .stApp { background: #f8fafc; }
    .main-title { 
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        font-size: 3.5rem; font-weight: 800; text-align: center; padding: 10px;
    }
    .sub-header { color: #475569; text-align: center; margin-bottom: 20px; font-weight: 500; }
    </style>
    <div class="main-title">𝕔𝕠𝕟𝕧𝕖𝕣𝕥𝕟𝕖𝕩𝕥.𝕚𝕟</div>
    <div class="sub-header">Advanced PDF, AI & Finance Intelligence</div>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://placehold.co/200x50/6366f1/ffffff?text=ConvertNext", use_column_width=True)
menu = st.sidebar.selectbox("Select Category", 
    ["📄 PDF Pro", "🖼️ AI Image Lab", "📝 Text Intelligence", "💰 Finance & Stocks", "🛠️ Smart Utilities"])

api_key = st.sidebar.text_input("Gemini API Key", type="password", placeholder="Paste key for AI tools")

# --- 1. PDF PRO SUITE (ALL TOOLS MERGED) ---
if menu == "📄 PDF Pro":
    st.header("Comprehensive PDF Toolset")
    pdf_tool = st.tabs([
        "Merge & Rearrange", 
        "Images to PDF", 
        "PDF to Image", 
        "Text Extraction", 
        "Delete Pages", 
        "Security & Unlock"
    ])

    # Merge & Rearrange
    with pdf_tool[0]:
        st.subheader("Merge & Reorder PDFs")
        files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, key="merge_tool")
        if files:
            file_names = [f.name for f in files]
            order = st.multiselect("Set Merge Order", file_names, default=file_names)
            if st.button("Combine Now"):
                merger = PdfMerger()
                file_map = {f.name: f for f in files}
                for name in order:
                    merger.append(file_map[name])
                out = io.BytesIO()
                merger.write(out)
                st.download_button("Download Merged PDF", out.getvalue(), "merged.pdf")

    # Images to PDF
    with pdf_tool[1]:
        st.subheader("Convert Images to PDF")
        img_files = st.file_uploader("Upload JPG/PNG", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        if st.button("Generate PDF from Images") and img_files:
            images = [Image.open(img).convert("RGB") for img in img_files]
            pdf_bytes = io.BytesIO()
            images[0].save(pdf_bytes, format="PDF", save_all=True, append_images=images[1:])
            st.download_button("Download Image-PDF", pdf_bytes.getvalue(), "images_to_pdf.pdf")

    # PDF to Image
    with pdf_tool[2]:
        st.subheader("Extract PDF Pages as Images")
        p2i_file = st.file_uploader("Select PDF", type="pdf", key="p2i")
        if p2i_file and st.button("Convert Pages to PNG"):
            doc = fitz.open(stream=p2i_file.read(), filetype="pdf")
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
                for i in range(len(doc)):
                    page = doc.load_page(i)
                    pix = page.get_pixmap(dpi=150)
                    img_data = pix.tobytes("png")
                    zip_file.writestr(f"page_{i+1}.png", img_data)
                    st.image(img_data, caption=f"Page {i+1}", width=200)
            st.download_button("Download All Images (ZIP)", zip_buffer.getvalue(), "pdf_to_images.zip")

    # Text Extraction
    with pdf_tool[3]:
        st.subheader("PDF Text Extractor")
        ext_file = st.file_uploader("Upload PDF", type="pdf", key="ext")
        if ext_file:
            reader = PdfReader(ext_file)
            full_text = "\n\n".join([page.extract_text() for page in reader.pages])
            st.text_area("Extracted Text", full_text, height=300)
            st.download_button("Download as Text File", full_text, "extracted.txt")

    # Delete Pages
    with pdf_tool[4]:
        st.subheader("Delete/Remove Pages")
        del_file = st.file_uploader("Upload PDF", type="pdf", key="del")
        if del_file:
            reader = PdfReader(del_file)
            st.info(f"Total Pages: {len(reader.pages)}")
            keep = st.text_input("Pages to KEEP (e.g. 1,2,5-8)", "1")
            if st.button("Process Removal"):
                writer = PdfWriter()
                indices = []
                try:
                    for part in keep.split(','):
                        if '-' in part:
                            s_idx, e_idx = map(int, part.split('-'))
                            indices.extend(range(s_idx, e_idx + 1))
                        else: indices.append(int(part))
                    for i in indices:
                        if 1 <= i <= len(reader.pages): writer.add_page(reader.pages[i-1])
                    out = io.BytesIO()
                    writer.write(out)
                    st.download_button("Download Edited PDF", out.getvalue(), "deleted_pages.pdf")
                except:
                    st.error("Format error. Please use numbers like 1,2,3 or ranges like 1-5")

    # Security (Rotate & Unlock)
    with pdf_tool[5]:
        st.subheader("Security & Rotation Tools")
        sec_file = st.file_uploader("Upload PDF", type="pdf", key="sec")
        if sec_file:
            mode = st.radio("Choose Action", ["Rotate & Protect", "Unlock PDF (Remove Password)"])
            
            if mode == "Rotate & Protect":
                col1, col2 = st.columns(2)
                angle = col1.selectbox("Rotate Pages", [0, 90, 180, 270])
                new_pw = col2.text_input("Set New Password", type="password", help="Leave blank if no password needed")
                if st.button("Apply Security/Rotate"):
                    reader = PdfReader(sec_file)
                    writer = PdfWriter()
                    for page in reader.pages:
                        writer.add_page(page)
                        if angle != 0: writer.pages[-1].rotate(angle)
                    if new_pw: writer.encrypt(new_pw)
                    out = io.BytesIO()
                    writer.write(out)
                    st.download_button("Download Result", out.getvalue(), "secured.pdf")
            
            elif mode == "Unlock PDF (Remove Password)":
                st.warning("This tool removes the password from a protected PDF.")
                current_pw = st.text_input("Enter Current Password", type="password")
                if st.button("Unlock & Download"):
                    try:
                        reader = PdfReader(sec_file)
                        if reader.is_encrypted:
                            reader.decrypt(current_pw)
                        
                        writer = PdfWriter()
                        for page in reader.pages:
                            writer.add_page(page)
                        
                        out = io.BytesIO()
                        writer.write(out)
                        st.success("PDF Unlocked Successfully!")
                        st.download_button("Download Unlocked PDF", out.getvalue(), "unlocked.pdf")
                    except Exception as e:
                        st.error(f"Failed to unlock. Ensure the password is correct. Error: {e}")

# --- 2. AI IMAGE LAB ---
# Move the import FROM the top of the file...
# ...TO inside the logic like this:

elif menu == "🖼️ Image Lab":
    if img_tab_index == 0: # BG Remover tab
        file = st.file_uploader("Upload Image")
        if file and st.button("Remove Background"):
            from rembg import remove  # <--- IMPORT HERE ONLY WHEN NEEDED
            res = remove(file.read())
            st.image(res)
    else:
        link = st.text_input("Link/Text", "https://convertnext.in")
        color = st.color_picker("Color", "#6366f1")
        if st.button("Generate QR"):
            qr = qrcode.QRCode(box_size=10, border=2)
            qr.add_data(link)
            qr_img = qr.make_image(fill_color=color, back_color="white")
            st.image(img, use_container_width=True)
            buf = io.BytesIO()
            qr_img.save(buf)
            st.download_button("Download QR", buf.getvalue(), "qr.png")

# --- 3. TEXT INTELLIGENCE ---
elif menu == "📝 Text Intelligence":
    st.header("AI Text Lab")
    if api_key:
        try:
            client = genai.Client(api_key=api_key)
            user_text = st.text_area("Input Text")
            action = st.selectbox("Action", ["Summarize", "Fix Grammar", "Professional Email"])
            if st.button("✨ Run AI") and user_text:
                resp = client.models.generate_content(model="gemini-2.0-flash", contents=f"{action}: {user_text}")
                st.markdown(resp.text)
        except Exception as e: st.error(f"API Error: {e}")
    else: st.info("Enter Gemini API Key in Sidebar")

# --- 4. FINANCE & STOCKS ---
elif menu == "💰 Finance & Stocks":
    st.header("Market Tools")
    t1, t2 = st.tabs(["EMI Calculator", "Stock Tracker"])
    with t1:
        p = st.number_input("Principal", 100000)
        r = st.number_input("Interest %", 8.5)
        y = st.slider("Years", 1, 30, 5)
        if st.button("Calculate EMI"):
            rate = r/(12*100)
            n = y*12
            emi = (p * rate * (1+rate)**n) / ((1+rate)**n - 1)
            st.metric("Monthly EMI", f"₹{round(emi, 2)}")
    with t2:
        ticker = st.text_input("Ticker (e.g. AAPL)", "AAPL")
        if st.button("Get Price"):
            s = yf.Ticker(ticker)
            st.metric(ticker, f"${s.fast_info['last_price']:.2f}")

# --- 5. SMART UTILITIES ---
elif menu == "🛠️ Smart Utilities":
    st.header("Daily Helpers")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Generate Secure Password"):
            pw = ''.join(secrets.choice(string.ascii_letters + string.digits + "!@#$%") for _ in range(16))
            st.code(pw)
    with c2:
        txt = st.text_input("Base64 Encode")
        if txt and st.button("Encode"):
            st.code(base64.b64encode(txt.encode()).decode())

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write("© 2026 **convertnext.in**")
st.sidebar.caption("Made with ♥ by Virendra Mane")
