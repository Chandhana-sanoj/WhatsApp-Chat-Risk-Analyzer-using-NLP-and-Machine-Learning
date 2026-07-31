# AI WhatsApp Chat Investigation System - Streamlit Entrypoint

import time
import importlib
import pandas as pd
import streamlit as st
import plotly.express as px

# Import custom helper modules
import styles
import parser
import preprocess
import predictor

# Force Python to reload modified modules from disk on rerun
importlib.reload(styles)
importlib.reload(parser)
importlib.reload(preprocess)
importlib.reload(predictor)

# Set page configuration
st.set_page_config(
    page_title="AI WhatsApp Chat Investigation System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session states
if "current_screen" not in st.session_state:
    st.session_state.current_screen = "upload"
if "parsed_data" not in st.session_state:
    st.session_state.parsed_data = None

# Inject custom CSS dynamically based on the active screen
styles.load_css(st.session_state.current_screen)

# Determine the algorithm name dynamically from the loaded model
model_algorithm_formatted = "Logistic Regression / Linear SVM"
try:
    if predictor.check_models_exist():
        _, classifier = predictor.load_models()
        model_algorithm = type(classifier).__name__
        if model_algorithm == "LogisticRegression":
            model_algorithm_formatted = "Logistic Regression"
        elif model_algorithm == "LinearSVC":
            model_algorithm_formatted = "Linear Support Vector Machine (Linear SVM)"
        elif model_algorithm == "SVC":
            model_algorithm_formatted = "Support Vector Machine (SVC)"
        else:
            model_algorithm_formatted = model_algorithm
except Exception:
    pass

# ==================================================
# SCREEN 1: Upload Page
# ==================================================
if st.session_state.current_screen == "upload":
    # Sidebar elements for the Upload page
    with st.sidebar:
        styles.render_logo()
        
    st.markdown('<div class="main-heading">Upload WhatsApp Chat Folder</div>', unsafe_allow_html=True)
    st.markdown(
        """
        Select all exported WhatsApp chat (**.txt**) files inside the subject's folder, 
        or **drag and drop the folder directly** into the box below.
        The system will parse, clean, and run forensic predictions using your trained classifier.
        """
    )
    
    # Enter the Person Name under investigation (corresponds to 'Person' in notebook)
    person_name = st.text_input(
        "Person Name (Subject of Investigation)", 
        value="Subject A",
        help="Specify the name of the person whose chats are being analysed."
    )
    
    # Multiple Files Uploader simulating a folder upload
    uploaded_files = st.file_uploader(
        "Upload WhatsApp Chat Files (Select All Inside Folder)",
        type=["txt"],
        accept_multiple_files=True,
        help="Click here or drag files to select multiple WhatsApp chat logs (.txt) from a folder."
    )
    
    st.write("") # Spacing
    
    # Analyze Button
    analyze_clicked = st.button("Analyze Chat Collection")
    
    if analyze_clicked:
        if not person_name.strip():
            st.warning("⚠️ Please specify a valid Person Name before running the analysis.")
        elif uploaded_files and len(uploaded_files) > 0:
            # Check if models exist before running pipeline
            if not predictor.check_models_exist():
                st.error(
                    "❌ ML Model Loading Error: The trained model files 'tfidf_vectorizer.pkl' and "
                    "'message_classifier.pkl' are not present in the 'models/' directory. "
                    "Please place your trained .pkl files inside the models/ folder."
                )
            else:
                # Progressive forensic pipeline status
                status_box = st.status("Initializing Forensic Analysis...", expanded=True)
                
                try:
                    # 1. Read Chats
                    status_box.update(label="Read Chat...", state="running")
                    file_contents = []
                    for uploaded_file in uploaded_files:
                        file_bytes = uploaded_file.read()
                        content = file_bytes.decode("utf-8-sig", errors="ignore")
                        # Extract chat name from filename (e.g. "Anna.txt" -> "Anna")
                        chat_name = uploaded_file.name.replace(".txt", "").replace("WhatsApp Chat with ", "").strip()
                        file_contents.append((chat_name, content))
                    time.sleep(0.3)
                    
                    # 2. Parse Chats
                    status_box.update(label="Parse Chat...", state="running")
                    all_messages = []
                    for name, content in file_contents:
                        parsed = parser.parse_chat(content, person_name.strip(), name)
                        all_messages.extend(parsed)
                            
                    if not all_messages:
                        status_box.update(label="Analysis failed: No valid WhatsApp messages found.", state="error")
                        st.error("None of the uploaded files could be parsed as valid WhatsApp logs. Check file formats.")
                    else:
                        combined_df = pd.DataFrame(all_messages)
                        time.sleep(0.3)
                        
                        # 3. Preprocess
                        status_box.update(label="Preprocess...", state="running")
                        cleaned_df = preprocess.preprocess_dataframe(combined_df)
                        time.sleep(0.3)
                        
                        # 4. Load TF-IDF
                        status_box.update(label="Load TF-IDF...", state="running")
                        # Verify successful models loading
                        vectorizer, classifier = predictor.load_models()
                        time.sleep(0.3)
                        
                        # 5. Predict
                        status_box.update(label="Predict...", state="running")
                        predictions_df = predictor.predict_whatsapp_risk(cleaned_df)
                        time.sleep(0.3)
                        
                        # 6. Generate Dashboard
                        status_box.update(label="Generate Dashboard...", state="running")
                        st.session_state.parsed_data = predictions_df
                        time.sleep(0.4)
                        
                        status_box.update(label="Forensic Analysis Completed successfully!", state="complete")
                        
                        # Move to Screen 2
                        st.session_state.current_screen = "dashboard"
                        st.rerun()
                        
                except Exception as e:
                    status_box.update(label="Pipeline error encountered during analysis.", state="error")
                    st.error(f"Error during execution: {str(e)}")
        else:
            st.warning("⚠️ Please select one or more exported WhatsApp chat text files before starting.")

# ==================================================
# SCREEN 2: Dashboard
# ==================================================
elif st.session_state.current_screen == "dashboard":
    df = st.session_state.parsed_data
    
    if df is None or df.empty:
        st.warning("No parsed data found in session. Please upload files first.")
        st.session_state.current_screen = "upload"
        st.rerun()
        
    # --- METRICS CALCULATIONS (Matching notebook aggregations) ---
    total_messages = len(df)
    normal_msg_count = sum(df["Predicted_Risk"] == "Normal")
    suspicious_msg_count = sum(df["Predicted_Risk"] == "Suspicious")
    high_risk_msg_count = sum(df["Predicted_Risk"] == "High Risk")
    
    # 1. Group by Chat_Name to build chat statistics (matches your notebook's chat_summary cells)
    chat_stats = df.groupby("Chat_Name").agg(
        Total_Messages=("Message", "count"),
        Normal=("Predicted_Risk", lambda x: (x == "Normal").sum()),
        Suspicious=("Predicted_Risk", lambda x: (x == "Suspicious").sum()),
        High_Risk=("Predicted_Risk", lambda x: (x == "High Risk").sum()),
        Average_Risk=("Risk_Score", "mean"),
        Max_Risk=("Risk_Score", "max")
    ).reset_index()
    
    # 2. Compute risk level for each chat file based on message percentages
    def compute_chat_risk(row):
        total = row["Total_Messages"]
        if total == 0:
            return "Low"
        high_pct = (row["High_Risk"] / total) * 100
        susp_pct = (row["Suspicious"] / total) * 100
        
        if high_pct > 15 or susp_pct > 30:
            return "High"
        elif (5 <= high_pct <= 15) or (15 <= susp_pct <= 30):
            return "Medium"
        else:
            return "Low"
            
    chat_stats["overall_risk"] = chat_stats.apply(compute_chat_risk, axis=1)
    
    # Sort chats by risk: High (0), Medium (1), Low (2)
    risk_order_map = {"High": 0, "Medium": 1, "Low": 2}
    chat_stats["risk_order"] = chat_stats["overall_risk"].map(risk_order_map)
    chat_stats = chat_stats.sort_values(by=["risk_order", "Average_Risk"], ascending=[True, False]).reset_index(drop=True)
    
    # 3. Calculate summary metrics (matches your notebook's person_summary cells)
    total_chats = len(chat_stats)
    high_risk_chats = sum(chat_stats["overall_risk"] == "High")
    suspicious_chats = sum(chat_stats["overall_risk"] == "Medium")
    
    # Overall risk score is the mean Average_Risk scaled to 0-100% (since risk score is 0, 1, or 2)
    overall_avg_risk = chat_stats["Average_Risk"].mean() if total_chats > 0 else 0.0
    overall_score = (overall_avg_risk / 2.0) * 100.0
    
    if high_risk_chats > 0:
        overall_level = "HIGH"
        overall_class = "risk-high"
    elif suspicious_chats > 0:
        overall_level = "MEDIUM"
        overall_class = "risk-medium"
    else:
        overall_level = "LOW"
        overall_class = "risk-low"
        
    # Most suspicious chat file
    if not chat_stats.empty:
        most_suspicious_chat = chat_stats.iloc[0]["Chat_Name"]
        most_susp_score = chat_stats.iloc[0]["Average_Risk"]
        # Scale score to percentage
        most_susp_score_pct = (most_susp_score / 2.0) * 100.0
    else:
        most_suspicious_chat = "N/A"
        most_susp_score_pct = 0.0
        
    # Header layout: Title and Action Button
    header_col, action_col = st.columns([5, 1])
    with header_col:
        st.markdown('<div class="main-heading" style="margin-bottom: 0;">AI Chat Forensic Investigation Dashboard</div>', unsafe_allow_html=True)
    with action_col:
        if st.button("← Upload New Collection"):
            st.session_state.parsed_data = None
            st.session_state.current_screen = "upload"
            st.rerun()
            
    st.write("") # Spacing
    
    # Model Metadata Box
    meta_col, spacer_col = st.columns([2.5, 3.5])
    with meta_col:
        styles.render_model_info_card(algorithm_name=model_algorithm_formatted)
        
    # --- TOP SUMMARY CARDS ---
    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    with m_col1:
        styles.render_summary_card("Total Chats", total_chats)
    with m_col2:
        styles.render_summary_card("Total Messages", total_messages)
    with m_col3:
        styles.render_summary_card("High Risk Chats", high_risk_chats, style_class="risk-high" if high_risk_chats > 0 else "")
    with m_col4:
        styles.render_summary_card("Suspicious Messages", suspicious_msg_count, style_class="risk-medium" if suspicious_msg_count > 0 else "")
    with m_col5:
        styles.render_summary_card(
            label="Overall Risk Level",
            val=overall_level,
            sublabel=f"Risk Score: {overall_score:.1f}%",
            style_class=overall_class
        )
        
    st.write("") # Spacing
    st.write("") # Spacing
    
    # --- CHARTS AND DETAILS ROW 1 ---
    row1_col1, row1_col2 = st.columns([3, 2])
    
    with row1_col1:
        st.subheader("Section 1: Chat Risk Ranking")
        st.write("Aggregated message classifications by individual chat:")
        # Render scrollable area for chat rankings table
        st.markdown('<div style="max-height: 380px; overflow-y: auto; padding-right: 0.5rem;">', unsafe_allow_html=True)
        # Convert columns to match expected schema: ['chat_name', 'high_risk_count', 'suspicious_count', 'overall_risk']
        display_stats = chat_stats.rename(columns={
            "Chat_Name": "chat_name",
            "High_Risk": "high_risk_count",
            "Suspicious": "suspicious_count"
        })
        styles.render_chat_ranking_table(display_stats)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with row1_col2:
        st.subheader("Section 2: Risk Distribution")
        
        # Plotly Pie Chart for message risk distribution
        dist_df = pd.DataFrame({
            "Class": ["Normal", "Suspicious", "High Risk"],
            "Count": [normal_msg_count, suspicious_msg_count, high_risk_msg_count]
        })
        dist_df = dist_df[dist_df["Count"] > 0]
        
        if not dist_df.empty:
            fig_pie = px.pie(
                dist_df,
                names="Class",
                values="Count",
                color="Class",
                color_discrete_map={
                    "Normal": "#2D6A4F",
                    "Suspicious": "#F77F00",
                    "High Risk": "#D90429"
                },
                hole=0.45
            )
            fig_pie.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#1B4332",
                margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
                height=320
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No message records found to show risk distribution.")
            
    st.write("") # Spacing
    st.write("") # Spacing
    
    # --- CHARTS AND DETAILS ROW 2 ---
    row2_col1, row2_col2 = st.columns([1, 1])
    
    with row2_col1:
        st.subheader("Section 3: Top Suspicious Keywords")
        
        # Extract keywords strictly from messages predicted as Suspicious or High Risk
        from collections import Counter
        flagged_msgs = df[df["Predicted_Risk"].isin(["Suspicious", "High Risk"])]["Processed_Message"].dropna()
        
        all_words = []
        for text in flagged_msgs:
            # Grab tokens of length > 2
            words = [w.strip() for w in text.split() if len(w.strip()) > 2]
            all_words.extend(words)
            
        word_counts = Counter(all_words)
        top_words = word_counts.most_common(10)
        
        if top_words:
            words_df = pd.DataFrame(top_words, columns=["Keyword", "Frequency"]).sort_values(by="Frequency", ascending=True)
            fig_bar = px.bar(
                words_df,
                x="Frequency",
                y="Keyword",
                orientation="h",
                color="Frequency",
                color_continuous_scale=["#95D5B2", "#2D6A4F", "#1B4332"],
                labels={"Frequency": "Count", "Keyword": "Term"}
            )
            fig_bar.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#1B4332",
                coloraxis_showscale=False,
                margin=dict(l=10, r=10, t=15, b=10),
                height=300
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No suspicious or high-risk keywords found in the flagged messages.")
            
    with row2_col2:
        st.subheader("Section 4: Suspicious Activity Timeline")
        
        # Calculate hourly profiles for flagged messages
        timeline_df = df.copy()
        timeline_df["is_flagged"] = timeline_df["Predicted_Risk"].isin(["Suspicious", "High Risk"]).astype(int)
        hourly_flagged = timeline_df.groupby("Hour")["is_flagged"].sum().reset_index()
        
        # Fill in missing hours (0 to 23)
        hours_df = pd.DataFrame({"Hour": list(range(24))})
        hourly_flagged = pd.merge(hours_df, hourly_flagged, on="Hour", how="left").fillna(0)
        hourly_flagged["is_flagged"] = hourly_flagged["is_flagged"].astype(int)
        
        fig_line = px.line(
            hourly_flagged,
            x="Hour",
            y="is_flagged",
            labels={"Hour": "Hour of Day", "is_flagged": "Flagged Messages"}
        )
        fig_line.update_traces(
            line_color="#2D6A4F",
            line_width=3.5,
            mode="lines+markers",
            marker=dict(size=6, color="#1B4332")
        )
        fig_line.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#1B4332",
            margin=dict(l=10, r=10, t=15, b=10),
            xaxis=dict(tickmode="linear", tick0=0, dtick=2, gridcolor="rgba(45, 106, 79, 0.08)"),
            yaxis=dict(gridcolor="rgba(45, 106, 79, 0.08)"),
            height=300
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
    st.write("") # Spacing
    st.write("") # Spacing
    
    # --- SECTION 5: AI INVESTIGATION SUMMARY ---
    st.subheader("Section 5: AI Investigation Summary")
    
    # Pick recommendations based on overall alert levels
    if overall_level == "HIGH":
        rec_text = (
            f"The forensic analysis indicates a HIGH RISK classification. "
            f"Multiple high-risk indicators were detected in conversations involving the chat collection. "
            f"The most suspicious chat is associated with '{most_suspicious_chat}' (Average Message Risk Score: {most_susp_score:.2f}). "
            f"Recommendation: Further manual investigation is recommended due to multiple high-risk conversations. "
            f"Isolate files and logs for deep security auditing."
        )
    elif overall_level == "MEDIUM":
        rec_text = (
            f"The forensic analysis indicates a MODERATE RISK classification. "
            f"Some suspicious topics and keywords were identified. Most flagged logs involve the chat "
            f"'{most_suspicious_chat}'. "
            f"Recommendation: Perform routine audits and continue monitoring communication paths."
        )
    else:
        rec_text = (
            f"The forensic analysis indicates a LOW RISK classification. "
            f"Conversations appear benign and standard. "
            f"Recommendation: No immediate threats detected. No manual investigation required."
        )
        
    # Render detailed stats in the summary section
    sum_col1, sum_col2 = st.columns([1, 2])
    with sum_col1:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; padding: 15px; border-radius: 8px; border: 1px solid rgba(45, 106, 79, 0.15); box-shadow: 0 2px 8px rgba(27, 67, 50, 0.01);">
                <p style="margin: 0 0 10px 0; color: #1B4332; font-size: 0.95rem;"><strong>Chats Analysed:</strong> {total_chats}</p>
                <p style="margin: 0 0 10px 0; color: #1B4332; font-size: 0.95rem;"><strong>Total Messages:</strong> {total_messages}</p>
                <p style="margin: 0 0 10px 0; color: #1B4332; font-size: 0.95rem;"><strong>High Risk Chats:</strong> {high_risk_chats}</p>
                <p style="margin: 0 0 10px 0; color: #1B4332; font-size: 0.95rem; word-break: break-all;"><strong>Most Suspicious Contact:</strong> {most_suspicious_chat}</p>
                <p style="margin: 0; color: #1B4332; font-size: 0.95rem;"><strong>Overall Risk Level:</strong> {overall_level} ({overall_score:.1f}%)</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    with sum_col2:
        styles.render_recommendation_card(overall_level == "HIGH", rec_text)
        
    # --- FOOTER ---
    styles.render_footer()

