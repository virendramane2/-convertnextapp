 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/app.py b/app.py
index 2c0f111713ae3dff10a5d8f19f4b3c367e2e6580..9ac008fa20c47f673f82084c987156ed0df50b96 100644
--- a/app.py
+++ b/app.py
@@ -1,154 +1,165 @@
-import streamlit as st
-from PyPDF2 import PdfMerger, PdfReader, PdfWriter
-from PIL import Image
-import google.generativeai as genai
-import qrcode
-import requests
-import io
-import uuid
-import yfinance as yf
-from rembg import remove
-
-# --- PAGE CONFIG ---
-st.set_page_config(page_title="convertnext.in - Python Suite", layout="wide", page_icon="⚡")
-
-# --- BRANDING ---
-st.markdown("""
-    <style>
-    .stApp { background: #f8fafc; }
-    .main-title { 
-        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); 
-        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
-        font-size: 3rem; font-weight: 800; text-align: center;
-    }
-    </style>
-    <div class="main-title">𝕔𝕠𝕟𝕧𝕖𝕣𝕥𝕟𝕖𝕩𝕥.𝕚𝕟</div>
-    """, unsafe_allow_html=True)
-
-# --- SIDEBAR NAVIGATION ---
-st.sidebar.image("https://placehold.co/200x50/6366f1/ffffff?text=ConvertNext", use_column_width=True)
-menu = st.sidebar.selectbox("Select Category", 
-    ["📄 PDF Pro", "🖼️ AI Image Lab", "📝 Text Intelligence", "💰 Finance & Stocks", "🛠️ Smart Utilities"])
-
-api_key = st.sidebar.text_input("Gemini API Key", type="password", placeholder="Paste key for AI tools")
-
-# --- 1. PDF PRO TOOLS ---
-if menu == "📄 PDF Pro":
-    st.header("Advanced PDF Suite")
-    tab1, tab2, tab3 = st.tabs(["Merge/Split", "Protect PDF", "PDF Metadata"])
-
-    with tab1:
-        files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
-        if st.button("Combine Documents") and files:
-            merger = PdfMerger()
-            for f in files: merger.append(f)
-            out = io.BytesIO()
-            merger.write(out)
-            st.download_button("Download Merged PDF", out.getvalue(), "merged.pdf")
-
-    with tab2:
-        file = st.file_uploader("Select PDF to Lock", type="pdf", key="lock")
-        password = st.text_input("Set Password", type="password")
-        if st.button("Encrypt PDF") and file and password:
-            reader = PdfReader(file)
-            writer = PdfWriter()
-            for page in reader.pages: writer.add_page(page)
-            writer.encrypt(password)
-            out = io.BytesIO()
-            writer.write(out)
-            st.download_button("Download Protected PDF", out.getvalue(), "locked.pdf")
-
-# --- 2. AI IMAGE LAB ---
-elif menu == "🖼️ AI Image Lab":
-    st.header("Visual Intelligence")
-    img_mode = st.radio("Tool", ["AI BG Remover", "QR Generator", "AI Image Gen"])
-
-    if img_mode == "AI BG Remover":
-        file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
-        if file:
-            img = Image.open(file)
-            st.image(img, caption="Original", width=300)
-            if st.button("Remove Background"):
-                with st.spinner("Processing..."):
-                    result = remove(img)
-                    st.image(result, caption="Cleaned Image")
-                    buf = io.BytesIO()
-                    result.save(buf, format="PNG")
-                    st.download_button("Download PNG", buf.getvalue(), "no-bg.png")
-
-    elif img_mode == "QR Generator":
-        link = st.text_input("Enter URL or Text", "https://convertnext.in")
-        color = st.color_picker("QR Color", "#6366f1")
-        if st.button("Generate QR Code"):
-            qr = qrcode.QRCode(box_size=10, border=2)
-            qr.add_data(link)
-            qr_img = qr.make_image(fill_color=color, back_color="white")
-            st.image(qr_img, width=250)
-            buf = io.BytesIO()
-            qr_img.save(buf)
-            st.download_button("Download QR", buf.getvalue(), "qr.png")
-
-# --- 3. TEXT INTELLIGENCE ---
-elif menu == "📝 Text Intelligence":
-    st.header("Gemini AI Text Lab")
-    if api_key:
-        genai.configure(api_key=api_key)
-        model = genai.GenerativeModel('gemini-pro')
-        
-        user_text = st.text_area("Input Text", height=200)
-        action = st.selectbox("AI Action", ["Summarize", "Fix Grammar", "Rewrite as Professional Email", "Extract Key Topics"])
-        
-        if st.button("✨ Run AI"):
-            with st.spinner("Thinking..."):
-                response = model.generate_content(f"{action}: {user_text}")
-                st.markdown("### AI Result")
-                st.write(response.text)
-    else:
-        st.info("Enter your Gemini API key in the sidebar to unlock this tool.")
-
-# --- 4. FINANCE & STOCKS ---
-elif menu == "💰 Finance & Stocks":
-    st.header("Market & Loan Tools")
-    tool = st.segmented_control("Select Tool", ["EMI Calc", "Stock Tracker"])
-    
-    if tool == "EMI Calc":
-        p = st.number_input("Loan Amount", 100000)
-        r = st.number_input("Interest %", 8.5)
-        y = st.slider("Years", 1, 30, 5)
-        if st.button("Calculate EMI"):
-            rate = r/(12*100)
-            n = y*12
-            emi = (p * rate * (1+rate)**n) / ((1+rate)**n - 1)
-            st.metric("Monthly EMI", f"₹{round(emi, 2)}")
-            
-    if tool == "Stock Tracker":
-        ticker = st.text_input("Enter Stock Ticker (e.g. RELIANCE.NS or AAPL)", "AAPL")
-        if st.button("Get Price"):
-            data = yf.Ticker(ticker)
-            price = data.history(period="1d")['Close'].iloc[-1]
-            st.metric(f"{ticker} Current Price", f"${round(price, 2)}")
-
-# --- 5. SMART UTILITIES ---
-elif menu == "🛠️ Smart Utilities":
-    st.header("Daily Helpers")
-    col1, col2 = st.columns(2)
-    
-    with col1:
-        st.subheader("Password Generator")
-        length = st.slider("Length", 8, 32, 16)
-        if st.button("Generate Secure Password"):
-            pw = uuid.uuid4().hex[:length]
-            st.code(pw)
-            
-    with col2:
-        st.subheader("Base64 Converter")
-        b64_text = st.text_input("Text to Encode")
-        if st.button("Encode"):
-            import base64
-            encoded = base64.b64encode(b64_text.encode()).decode()
-            st.success(encoded)
-
-# --- FOOTER ---
-st.sidebar.markdown("---")
-st.sidebar.write("© 2026 **convertnext.in**")
+import streamlit as st
+from PyPDF2 import PdfMerger, PdfReader, PdfWriter
+from PIL import Image
+import google.generativeai as genai
+import qrcode
+import io
+import uuid
+import yfinance as yf
+from rembg import remove
+
+# --- PAGE CONFIG ---
+st.set_page_config(page_title="convertnext.in - Python Suite", layout="wide", page_icon="⚡")
+
+# --- BRANDING ---
+st.markdown("""
+    <style>
+    .stApp { background: #f8fafc; }
+    .main-title { 
+        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); 
+        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
+        font-size: 3rem; font-weight: 800; text-align: center;
+    }
+    </style>
+    <div class="main-title">𝕔𝕠𝕟𝕧𝕖𝕣𝕥𝕟𝕖𝕩𝕥.𝕚𝕟</div>
+    """, unsafe_allow_html=True)
+
+# --- SIDEBAR NAVIGATION ---
+st.sidebar.image("https://placehold.co/200x50/6366f1/ffffff?text=ConvertNext", use_column_width=True)
+menu = st.sidebar.selectbox("Select Category", 
+    ["📄 PDF Pro", "🖼️ AI Image Lab", "📝 Text Intelligence", "💰 Finance & Stocks", "🛠️ Smart Utilities"])
+
+api_key = st.sidebar.text_input("Gemini API Key", type="password", placeholder="Paste key for AI tools")
+
+# --- 1. PDF PRO TOOLS ---
+if menu == "📄 PDF Pro":
+    st.header("Advanced PDF Suite")
+    tab1, tab2, tab3 = st.tabs(["Merge/Split", "Protect PDF", "PDF Metadata"])
+
+    with tab1:
+        files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
+        if st.button("Combine Documents") and files:
+            merger = PdfMerger()
+            for f in files: merger.append(f)
+            out = io.BytesIO()
+            merger.write(out)
+            st.download_button("Download Merged PDF", out.getvalue(), "merged.pdf")
+
+    with tab2:
+        file = st.file_uploader("Select PDF to Lock", type="pdf", key="lock")
+        password = st.text_input("Set Password", type="password")
+        if st.button("Encrypt PDF") and file and password:
+            reader = PdfReader(file)
+            writer = PdfWriter()
+            for page in reader.pages: writer.add_page(page)
+            writer.encrypt(password)
+            out = io.BytesIO()
+            writer.write(out)
+            st.download_button("Download Protected PDF", out.getvalue(), "locked.pdf")
+
+    with tab3:
+        file = st.file_uploader("Select PDF for metadata", type="pdf", key="metadata")
+        if file:
+            reader = PdfReader(file)
+            meta = reader.metadata or {}
+            st.write({k: str(v) for k, v in meta.items()})
+            st.caption(f"Total Pages: {len(reader.pages)}")
+
+# --- 2. AI IMAGE LAB ---
+elif menu == "🖼️ AI Image Lab":
+    st.header("Visual Intelligence")
+    img_mode = st.radio("Tool", ["AI BG Remover", "QR Generator", "AI Image Gen"])
+
+    if img_mode == "AI BG Remover":
+        file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
+        if file:
+            img = Image.open(file)
+            st.image(img, caption="Original", width=300)
+            if st.button("Remove Background"):
+                with st.spinner("Processing..."):
+                    result = remove(img)
+                    st.image(result, caption="Cleaned Image")
+                    buf = io.BytesIO()
+                    result.save(buf, format="PNG")
+                    st.download_button("Download PNG", buf.getvalue(), "no-bg.png")
+
+    elif img_mode == "QR Generator":
+        link = st.text_input("Enter URL or Text", "https://convertnext.in")
+        color = st.color_picker("QR Color", "#6366f1")
+        if st.button("Generate QR Code"):
+            qr = qrcode.QRCode(box_size=10, border=2)
+            qr.add_data(link)
+            qr_img = qr.make_image(fill_color=color, back_color="white")
+            st.image(qr_img, width=250)
+            buf = io.BytesIO()
+            qr_img.save(buf)
+            st.download_button("Download QR", buf.getvalue(), "qr.png")
+
+# --- 3. TEXT INTELLIGENCE ---
+elif menu == "📝 Text Intelligence":
+    st.header("Gemini AI Text Lab")
+    if api_key:
+        genai.configure(api_key=api_key)
+        model = genai.GenerativeModel('gemini-pro')
+        
+        user_text = st.text_area("Input Text", height=200)
+        action = st.selectbox("AI Action", ["Summarize", "Fix Grammar", "Rewrite as Professional Email", "Extract Key Topics"])
+        
+        if st.button("✨ Run AI"):
+            with st.spinner("Thinking..."):
+                response = model.generate_content(f"{action}: {user_text}")
+                st.markdown("### AI Result")
+                st.write(response.text)
+    else:
+        st.info("Enter your Gemini API key in the sidebar to unlock this tool.")
+
+# --- 4. FINANCE & STOCKS ---
+elif menu == "💰 Finance & Stocks":
+    st.header("Market & Loan Tools")
+    tool = st.segmented_control("Select Tool", ["EMI Calc", "Stock Tracker"])
+    
+    if tool == "EMI Calc":
+        p = st.number_input("Loan Amount", 100000)
+        r = st.number_input("Interest %", 8.5)
+        y = st.slider("Years", 1, 30, 5)
+        if st.button("Calculate EMI"):
+            rate = r/(12*100)
+            n = y*12
+            emi = (p * rate * (1+rate)**n) / ((1+rate)**n - 1)
+            st.metric("Monthly EMI", f"₹{round(emi, 2)}")
+            
+    if tool == "Stock Tracker":
+        ticker = st.text_input("Enter Stock Ticker (e.g. RELIANCE.NS or AAPL)", "AAPL")
+        if st.button("Get Price"):
+            data = yf.Ticker(ticker)
+            history = data.history(period="1d")
+            if history.empty:
+                st.error("No pricing data found for this ticker.")
+            else:
+                price = history['Close'].iloc[-1]
+                st.metric(f"{ticker} Current Price", f"${round(price, 2)}")
+
+# --- 5. SMART UTILITIES ---
+elif menu == "🛠️ Smart Utilities":
+    st.header("Daily Helpers")
+    col1, col2 = st.columns(2)
+    
+    with col1:
+        st.subheader("Password Generator")
+        length = st.slider("Length", 8, 32, 16)
+        if st.button("Generate Secure Password"):
+            pw = uuid.uuid4().hex[:length]
+            st.code(pw)
+            
+    with col2:
+        st.subheader("Base64 Converter")
+        b64_text = st.text_input("Text to Encode")
+        if st.button("Encode"):
+            import base64
+            encoded = base64.b64encode(b64_text.encode()).decode()
+            st.success(encoded)
+
+# --- FOOTER ---
+st.sidebar.markdown("---")
+st.sidebar.write("© 2026 **convertnext.in**")
 st.sidebar.caption("Made with ♥ by Virendra Mane")
\ No newline at end of file
 
EOF
)
