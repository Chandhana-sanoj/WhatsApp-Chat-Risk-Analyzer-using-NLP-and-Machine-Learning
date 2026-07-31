# Custom HTML templates and CSS styles for the AI WhatsApp Chat Investigation System.

import streamlit as st

def load_css(screen="upload"):
    """
    Injects CSS rules as single-line HTML blocks to restore full colors,
    sidebar dark green styling, fonts, and layout without any text leakage.
    """
    if screen == "upload":
        css = "<style>html,body,.stApp{background-color:#F1FFF4!important;color:#1B4332;font-family:'Outfit',sans-serif;}h1,h2,h3,h4,h5,h6{color:#1B4332!important;font-weight:700!important;}.main-heading{font-size:2.2rem;font-weight:800;margin-bottom:1.5rem;color:#1B4332!important;}section[data-testid=\"stSidebar\"]{background-color:#1B4332!important;padding-top:2rem;border-right:1px solid rgba(255,255,255,0.05);min-width:320px!important;max-width:320px!important;}section[data-testid=\"stSidebar\"] *{color:#F1FFF4!important;}button[data-testid=\"stSidebarCollapseButton\"]{display:none!important;}div.stButton>button{background-color:#2D6A4F!important;color:#FFFFFF!important;font-weight:600!important;font-size:1rem!important;padding:0.5rem 2rem!important;border-radius:8px!important;border:none!important;width:100%!important;}div.stButton>button:hover{background-color:#1B4332!important;}div[data-testid=\"stFileUploader\"]{background-color:#FFFFFF!important;border:2px dashed rgba(45,106,79,0.3)!important;border-radius:12px!important;padding:2rem!important;}</style>"
    else:
        css = "<style>html,body,.stApp{background-color:#F1FFF4!important;color:#1B4332;font-family:'Outfit',sans-serif;}h1,h2,h3,h4,h5,h6{color:#1B4332!important;font-weight:700!important;}.main-heading{font-size:2.2rem;font-weight:800;margin-bottom:1.5rem;color:#1B4332!important;}section[data-testid=\"stSidebar\"]{display:none!important;}div[data-testid=\"collapsedSidebarCodegen\"]{display:none!important;}button[data-testid=\"stHeaderActionElements\"]{display:none!important;}header[data-testid=\"stHeader\"]{display:none!important;}div[data-testid=\"stAppViewBlockContainer\"]{max-width:93%!important;padding:2.5rem 4rem!important;}div.stButton>button{background-color:#2D6A4F!important;color:#FFFFFF!important;font-weight:600!important;font-size:1rem!important;padding:0.5rem 2rem!important;border-radius:8px!important;border:none!important;width:100%!important;}</style>"
        
    font_link = '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">'
    st.markdown(font_link + css, unsafe_allow_html=True)

def render_logo():
    """Renders the Forensic Shield & Target SVG Logo inside the sidebar."""
    logo_html = '<div style="text-align:center;margin-bottom:2rem;"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="width:75px;height:75px;fill:#F1FFF4;margin:0 auto 15px auto;display:block;"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 6c1.93 0 3.5 1.57 3.5 3.5 0 .95-.38 1.81-1 2.44l3.12 3.12-1.41 1.41-3.12-3.12c-.63.62-1.49 1-2.44 1-1.93 0-3.5-1.57-3.5-3.5S10.07 7 12 7zm0 2c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5S12.83 9 12 9z"/></svg><div style="font-size:1.5rem;font-weight:700;line-height:1.25;margin-top:1rem;margin-bottom:0.5rem;color:#FFFFFF;letter-spacing:-0.02em;">AI WhatsApp Chat<br>Investigation System</div><div style="font-size:0.85rem;font-weight:400;opacity:0.85;color:#A3E4D7;text-transform:uppercase;letter-spacing:0.05em;line-height:1.4;">AI-Assisted Suspicious Chat Detection</div></div>'
    st.markdown(logo_html, unsafe_allow_html=True)

def render_summary_card(label, val, sublabel="", style_class=""):
    """Helper to render a summary metric card with inline styles."""
    top_border_color = "#2D6A4F"
    text_color = "#2D6A4F"
    if "risk-high" in style_class:
        top_border_color = "#D90429"
        text_color = "#D90429"
    elif "risk-medium" in style_class:
        top_border_color = "#F77F00"
        text_color = "#F77F00"

    sublabel_html = f'<div style="font-size:0.75rem;color:#555555;margin-top:0.2rem;font-weight:400;">{sublabel}</div>' if sublabel else ''
    card_html = f'<div style="background-color:#FFFFFF;border-radius:12px;padding:1.2rem;border-top:4px solid {top_border_color};border-left:1px solid rgba(45,106,79,0.12);border-right:1px solid rgba(45,106,79,0.12);border-bottom:1px solid rgba(45,106,79,0.12);box-shadow:0 4px 12px rgba(27,67,50,0.03);text-align:center;height:100%;display:flex;flex-direction:column;justify-content:center;"><div style="font-size:2.2rem;font-weight:800;color:{text_color};margin-bottom:0.2rem;line-height:1.1;">{val}</div><div style="font-size:0.85rem;font-weight:600;text-transform:uppercase;letter-spacing:0.04em;color:#52B788;">{label}</div>{sublabel_html}</div>'
    st.markdown(card_html, unsafe_allow_html=True)

def render_model_info_card(algorithm_name="Logistic Regression"):
    """Renders the Prediction Model details panel with inline styles."""
    info_html = f'<div style="background-color:#1B4332;color:#F1FFF4;border-radius:12px;padding:1.2rem;border:1px solid rgba(255,255,255,0.1);margin-bottom:1.5rem;box-shadow:0 4px 15px rgba(0,0,0,0.1);"><div style="font-size:0.95rem;font-weight:700;color:#A3E4D7;margin-bottom:0.6rem;display:flex;align-items:center;gap:0.4rem;text-transform:uppercase;letter-spacing:0.05em;"><svg style="width:16px;height:16px;fill:currentColor;" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg> Prediction Model</div><div style="font-size:0.85rem;line-height:1.4;margin-bottom:0.4rem;color:#E2FCE8;"><strong>Algorithm:</strong> {algorithm_name}</div><div style="font-size:0.85rem;line-height:1.4;margin-bottom:0.4rem;color:#E2FCE8;"><strong>Feature Extraction:</strong> TF-IDF Vectorizer</div><div style="font-size:0.85rem;line-height:1.4;color:#E2FCE8;"><strong>Classes:</strong> Normal, Suspicious, High Risk</div></div>'
    st.markdown(info_html, unsafe_allow_html=True)

def render_chat_ranking_table(chat_stats_df):
    """Renders a styled HTML table showing the risk statistics grouped by WhatsApp chat."""
    rows = []
    for _, row in chat_stats_df.iterrows():
        risk = row["overall_risk"]
        if risk == "High":
            badge = '<span style="background-color:#FFE3E6;color:#D90429;padding:4px 8px;border-radius:12px;font-size:0.75rem;font-weight:700;">🔴 HIGH</span>'
            border = "border-left:4px solid #D90429;"
        elif risk == "Medium":
            badge = '<span style="background-color:#FFF0E0;color:#F77F00;padding:4px 8px;border-radius:12px;font-size:0.75rem;font-weight:700;">🟠 MEDIUM</span>'
            border = "border-left:4px solid #F77F00;"
        else:
            badge = '<span style="background-color:#E8F7EE;color:#2D6A4F;padding:4px 8px;border-radius:12px;font-size:0.75rem;font-weight:700;">🟢 LOW</span>'
            border = "border-left:4px solid #2D6A4F;"
            
        rows.append(f'<tr style="border-bottom:1px solid rgba(45,106,79,0.1);background-color:#FFFFFF;{border}"><td style="padding:10px 14px;font-weight:700;color:#1B4332;">{row["chat_name"]}</td><td style="padding:10px 14px;text-align:right;color:#D90429;font-weight:700;">{row["high_risk_count"]}</td><td style="padding:10px 14px;text-align:right;color:#F77F00;font-weight:700;">{row["suspicious_count"]}</td><td style="padding:10px 14px;text-align:right;">{badge}</td></tr>')
        
    table_body = "".join(rows)
    table_html = f'<div style="overflow-x:auto;border-radius:8px;border:1px solid rgba(45,106,79,0.15);"><table style="width:100%;border-collapse:collapse;text-align:left;background-color:#FFFFFF;font-size:0.9rem;"><thead><tr style="background-color:#2D6A4F;color:#FFFFFF;"><th style="padding:10px 14px;">Chat</th><th style="padding:10px 14px;text-align:right;">High Risk</th><th style="padding:10px 14px;text-align:right;">Suspicious</th><th style="padding:10px 14px;text-align:right;">Overall</th></tr></thead><tbody>{table_body}</tbody></table></div>'
    
    st.markdown(table_html, unsafe_allow_html=True)

def render_recommendation_card(is_high_risk, text):
    """Renders investigation recommendation."""
    border_color = "#D90429" if is_high_risk else "#2D6A4F"
    title = "Urgent: Manual Investigation Required" if is_high_risk else "Investigation Verdict: Routine Monitoring"
    rec_html = f'<div style="background-color:#FFFFFF;border-radius:12px;padding:1.5rem;border-left:5px solid {border_color};border-top:1px solid rgba(45,106,79,0.12);border-right:1px solid rgba(45,106,79,0.12);border-bottom:1px solid rgba(45,106,79,0.12);box-shadow:0 4px 15px rgba(27,67,50,0.03);margin-bottom:2rem;"><div style="font-weight:700;font-size:1.1rem;color:#1B4332;margin-bottom:0.5rem;">{title}</div><div style="font-size:0.95rem;line-height:1.5;color:#333333;">{text}</div></div>'
    st.markdown(rec_html, unsafe_allow_html=True)

def render_footer():
    """Renders the technical stack footer."""
    footer_html = '<div style="margin-top:4rem;padding-top:1.5rem;border-top:1px solid rgba(45,106,79,0.15);text-align:center;color:#52B788;font-size:0.85rem;"><div style="font-weight:700;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;font-size:0.8rem;">Developed Using</div><div style="font-weight:500;color:#1B4332;letter-spacing:0.02em;">Python &bull; Streamlit &bull; Scikit-learn<br>TF-IDF Vectorizer &bull; Linear SVM Classifier<br>Pandas &bull; Plotly</div></div>'
    st.markdown(footer_html, unsafe_allow_html=True)



