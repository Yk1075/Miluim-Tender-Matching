import streamlit as st
import pandas as pd
from create_comprehensive_matches import (
    is_miluim_soldier, 
    get_profile_category, 
    check_area_match, 
    check_eligibility_match, 
    check_housing_match
)

# Set page configuration
st.set_page_config(
    page_title="מערכת התאמת מכרזי דיור",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# RTL and styling CSS - COMPLETE REDESIGN - FORCE UPDATE
st.markdown("""
<style>
    /* FORCE BROWSER REFRESH */
    .force-refresh { display: none; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    /* Import Hebrew font */
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700&display=swap');
    
    /* Global RTL and font settings */
    html[dir="ltr"], body[dir="ltr"], .stApp {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Heebo', 'Arial', sans-serif !important;
    }
    
    /* Force RTL on all elements */
    * {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Heebo', 'Arial', sans-serif !important;
    }
    
    /* Background and main container */
    .main {
        background-color: #ffffff !important;
        padding: 2rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    }
    
    /* Headers with better styling */
    h1, h2, h3, h4, h5, h6 {
        color: #1a365d !important;
        font-weight: 700 !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
    }
    
    h1 { font-size: 2.5rem !important; }
    h2 { font-size: 2rem !important; }
    h3 { font-size: 1.5rem !important; }
    
    /* Fix input fields completely */
    .stSelectbox, .stNumberInput {
        margin-bottom: 1.5rem !important;
    }
    
    /* Labels styling */
    .stSelectbox label, .stNumberInput label, .stTextInput label {
        color: #2d3748 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
    }
    
    /* COMPLETE INPUT FIELD REDESIGN FOR PERFECT CONTRAST */
    
    /* All input containers - uniform styling */
    .stSelectbox > div, .stNumberInput > div {
        background: white !important;
        border: 3px solid #4a90e2 !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Selectbox complete overhaul */
    .stSelectbox > div[data-baseweb="select"] > div {
        background-color: white !important;
        border: none !important;
        min-height: 60px !important;
        padding: 16px 20px !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #1a202c !important;
    }
    
    /* Dropdown text */
    .stSelectbox > div[data-baseweb="select"] > div > div {
        color: #1a202c !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* Number input overhaul */
    .stNumberInput > div > div > input {
        background-color: white !important;
        border: none !important;
        padding: 16px 20px !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #1a202c !important;
        min-height: 60px !important;
        box-sizing: border-box !important;
    }
    
    /* Input placeholders */
    .stSelectbox > div[data-baseweb="select"] > div::placeholder,
    .stNumberInput > div > div > input::placeholder {
        color: #718096 !important;
        font-weight: 500 !important;
    }
    
    /* Focus states */
    .stSelectbox > div[data-baseweb="select"] > div:focus-within,
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus {
        border-color: #4299e1 !important;
        box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1) !important;
    }
    
    /* Help tooltip styling */
    .stTooltipIcon {
        color: #4299e1 !important;
        font-size: 1.2rem !important;
        margin-right: 8px !important;
    }
    
    /* Info boxes with better styling */
    .stInfo {
        background: linear-gradient(135deg, #ebf8ff 0%, #bee3f8 100%) !important;
        border: 1px solid #90cdf4 !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    }
    
    .stInfo p, .stInfo div {
        color: #2a4365 !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
    }
    
    /* Success, warning, error boxes */
    .stSuccess {
        background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%) !important;
        border: 1px solid #9ae6b4 !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fffbeb 0%, #fed7aa 100%) !important;
        border: 1px solid #f6ad55 !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%) !important;
        border: 1px solid #fc8181 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(66, 153, 225, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3182ce 0%, #2c5282 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(66, 153, 225, 0.6) !important;
    }
    
    /* IMPROVED TENDER CARD STYLING */
    .stExpander {
        border: 2px solid #4a90e2 !important;
        border-radius: 16px !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 6px 20px rgba(74, 144, 226, 0.3) !important;
        background: white !important;
    }
    
    /* LARGE TENDER CARD HEADER */
    .stExpander details summary {
        background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%) !important;
        padding: 1.5rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.4rem !important;
        color: white !important;
        border-radius: 14px !important;
        text-align: center !important;
        line-height: 1.4 !important;
        min-height: 70px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .stExpander details summary:hover {
        background: linear-gradient(135deg, #357abd 0%, #2c5aa0 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(74, 144, 226, 0.4) !important;
    }
    
    /* Ensure all text is readable */
    .stMarkdown, .stMarkdown p, .stMarkdown div,
    .stSelectbox, .stNumberInput, .stTextInput {
        color: #2d3748 !important;
    }
    
    /* Hide unwanted Streamlit elements */
    .stDeployButton, .stDecoration, #MainMenu, footer, .stToolbar {
        display: none !important;
    }
    
    /* Container spacing */
    .element-container {
        margin-bottom: 1rem !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main {
            padding: 1rem !important;
        }
        
        h1 { font-size: 2rem !important; }
        h2 { font-size: 1.5rem !important; }
    }
</style>
""", unsafe_allow_html=True)

def find_matching_tenders(profile_data):
    """Find tenders that match the user profile"""
    try:
        # Load tender data
        tenders_df = pd.read_csv('data/csv_output/טבלת מכרזים ניסיון שני_.csv')
        
        # Create profile series
        profile = pd.Series(profile_data)
        
        # Get profile category
        profile_category = get_profile_category(profile)
        
        matching_tenders = []
        
        for _, tender in tenders_df.iterrows():
            # Apply matching filters
            area_match = check_area_match(profile_data['אזור_מועדף'], tender['אזור גיאוגרפי '])
            eligibility_match = check_eligibility_match(profile_category, tender['מי רשאי להגיש'])
            housing_match = check_housing_match(profile_data['חסר_דיור'], tender['סטטוס דיור נדרש'])
            
            # Only include if all criteria match
            if area_match and eligibility_match and housing_match:
                matching_tenders.append({
                    'מספר מכרז': tender['מספר המכרז'],
                    'עיר': tender['עיר'],
                    'שכונה': tender['שכונה'],
                    'אזור גיאוגרפי': tender['אזור גיאוגרפי '],
                    'מספר מגרשים': tender['מספר מגרשים'],
                    'מגרשים לנכי צה"ל': tender['כמה מגרשים בעדיפות בהגרלה לנכי צה"ל'],
                    'מגרשים לחיילי מילואים': tender['כמה מגרשים בעדיפות בהגרלה לחיילי מילואים'],
                    'תאריך פרסום חוברת המכרז': tender['תאריך פרסום חוברת'],
                    'מועד אחרון להגשה': tender['מועד אחרון להגשת הצעות'],
                    'אזור עדיפות': tender['אזור עדיפות']
                })
        
        return pd.DataFrame(matching_tenders)
        
    except Exception as e:
        st.error(f"אירעה שגיאה בעת חיפוש המכרזים: {str(e)}")
        return pd.DataFrame()

def render_tender_card(tender):
    """Render tender card with clean styling"""
    
    # Get location info safely
    city = str(tender.get('עיר', ''))
    neighborhood = str(tender.get('שכונה', ''))
    area = str(tender.get('אזור גיאוגרפי', ''))
    
    # Build location string safely
    location_parts = []
    if neighborhood and neighborhood != 'nan' and neighborhood != 'None' and neighborhood.strip():
        location_parts.append(neighborhood.strip())
    if city and city != 'nan' and city != 'None' and city.strip():
        location_parts.append(city.strip())
    if area and area != 'nan' and area != 'None' and area.strip():
        location_parts.append(area.strip())
    
    location_display = ' • '.join(location_parts) if location_parts else 'מיקום לא צוין'
    
    # Create tender card using expander
    header_text = f"🏆 מכרז #{tender['מספר מכרז']} | 📍 {location_display}"
    with st.expander(header_text, expanded=True):
        
        # Plot count and priority
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.markdown(f"🏠 מספר מגרשים: {tender['מספר מגרשים']}")
        
        with col_right:
            priority_status = str(tender.get('אזור עדיפות', ''))
            if priority_status == "A":
                st.error("🔥 עדיפות א'")
            elif priority_status == "B":
                st.warning("⚡ עדיפות ב'")
            else:
                st.info("📋 ללא עדיפות לאומית")
        
        # Dates
        date_col_left, date_col_right = st.columns([1, 1])
        
        with date_col_left:
            st.markdown(f"📅 פרסום חוברת: {tender['תאריך פרסום חוברת המכרז']}")
        
        with date_col_right:
            st.markdown(f"⏰ מועד אחרון: {tender['מועד אחרון להגשה']}")
        
        # Link to ILA system - IMPROVED DESIGN
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <a href="https://apps.land.gov.il/MichrazimSite/#/search" target="_blank" style="
                display: inline-block;
                padding: 20px 40px;
                background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%);
                color: white;
                text-decoration: none;
                border-radius: 16px;
                font-weight: 700;
                font-size: 1.3rem;
                text-align: center;
                box-shadow: 0 8px 25px rgba(229, 62, 62, 0.4);
                transition: all 0.3s ease;
                border: 3px solid #c53030;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            " 
            onmouseover="this.style.background='linear-gradient(135deg, #c53030 0%, #9c2626 100%)'; this.style.transform='translateY(-3px)'; this.style.boxShadow='0 12px 35px rgba(229, 62, 62, 0.6)';"
            onmouseout="this.style.background='linear-gradient(135deg, #e53e3e 0%, #c53030 100%)'; this.style.transform='translateY(0px)'; this.style.boxShadow='0 8px 25px rgba(229, 62, 62, 0.4)';">
                🌐 כניסה למערכת המכרזים של רמ״י
            </a>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Display logo
    st.image("apm_logo.png", width=90)
    
    # Main title and subtitle
    st.title("🏠 מילואים וזוכים - מערכת התאמת מכרזים")
    st.subheader("מצא את המכרז המושלם עבורך בהתאם לפרופיל השירות והעדפותיך")
    
    # Info sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
**איך זה עובד?**

על בסיס תנאי הזכאות והמכרזים שפורסמו על ידי רשות מקרקעי ישראל המערכת יודעת להתאים לך את מכרזים ייעודיים עם התאמה מקסימלית. פשוט עונים על השאלות מטה והמכרזים הרלוונטים כבר יעלו לפניכם כך שתוכלו להתקדם מבלי לבזבז זמן חשוב על נבירה באתר של רמ״י.

שימו לב, במרבית המכרזים הפרטים המלאים יופיעו בחוברת המכרז- כך ששווה במציאת המכרזים הרלוונטים לשים לכם תזכורת לתאריך פרסום החוברת ותאריך ההגשה האחרון שלא תפספסו!
""")
    
    with col2:
        st.info("""
**💰 ההטבות העיקריות**

• הנחות של 10-35% באזורי עדיפות לאומית

• הנחות נוספות של 10-35% ממחיר המגרש

• קדימות בהגרלות למילואים ונכי צה"ל
""")

    st.markdown("---")

    # Layout: Search form (30%) + Results (70%)
    search_col, results_col = st.columns([0.3, 0.7], gap="medium")

    # Initialize session state
    if 'search_performed' not in st.session_state:
        st.session_state.search_performed = False
    if 'matches' not in st.session_state:
        st.session_state.matches = pd.DataFrame()

    with search_col:
        with st.container():
            st.markdown("### 📋 פרטים אישיים")
            
            # Days since Oct 7 with clear explanation
            st.markdown("#### 🗓️ ימי מילואים מ-7.10.23")
            days_since_oct = st.number_input(
                "הכנס מספר ימים:",
                min_value=0,
                value=0,
                key="days_since_oct"
            )
            st.info("💡 **הסבר:** מעל 45 ימים = הנחה של 10-35% ממחיר המגרש. נדרש אישור רשמי על השירות במלחמת 'חרבות ברזל'.")
            
            # Active card with explanation
            st.markdown("#### 🪖 תעודת מילואים פעיל")
            active_card = st.selectbox(
                "בחר אפשרות:",
                options=["לא", "כן"],
                key="active_card"
            )
            st.info("💡 **הסבר:** זכאות מיוחדת למכרזים ייעודיים + עדיפות בהגרלות + הנחות נוספות. נדרש אישור למשרת מילואים פעיל.")
            
            # Days in 6 years with explanation
            st.markdown("#### 📊 ימי מילואים ב-6 שנים")
            days_in_6_years = st.number_input(
                "הכנס סך הימים במצטבר:",
                min_value=0,
                value=0,
                key="days_in_6_years"
            )
            st.info("💡 **הסבר:** 50+ ימים = הנחות מיוחדות | 100+ ימים = הנחות משמעותיות. נחשב הפרק הטוב ביותר של 6 שנים רצופות.")
            
            # Disability status with explanation
            st.markdown("#### 🎖️ סיווג נכות")
            disability_status = st.selectbox(
                "בחר סיווג:",
                options=["אין", "נכות קשה", "100% ומעלה"],
                key="disability_status"
            )
            st.info("💡 **הסבר:** נכות קשה = מגרשים ייעודיים + הנחות של 35% | 100%+ = הטבות מקסימליות + עדיפות עליונה.")
            
            # Housing status with explanation
            st.markdown("#### 🏠 חסר/ת דיור")
            housing_status = st.selectbox(
                "בחר מצב:",
                options=["לא", "כן"],
                key="housing_status"
            )
            st.info("💡 **הסבר:** הנחות נוספות של 10-20% + עדיפות בהגרלות + זכאות למכרזים ייעודיים. בדוק באתר gov.il.")
            
            # Preferred area with explanation
            st.markdown("#### 🗺️ אזור מועדף")
            preferred_area = st.selectbox(
                "בחר אזור:",
                options=["דרום", "צפון", "ירושלים", "מרכז", "יהודה ושומרון"],
                key="preferred_area"
            )
            st.info("💡 **הסבר:** אזורי עדיפות לאומית (א', ב') מציעים הנחות גדולות יותר! המערכת תמצא מכרזים רק באזור שבחרת.")
            
            # Spouse eligibility with explanation
            st.markdown("#### 💑 בן/בת זוג זכאי/ת")
            spouse_eligible = st.selectbox(
                "בחר מצב:",
                options=["לא", "כן"],
                key="spouse_eligible"
            )
            st.info("💡 **הסבר:** הטבות כפולות! הנחות מצטברות (עד 70%!) + עדיפות גבוהה בהגרלות + מכרזים מיוחדים לזוגות זכאים.")

            st.markdown("---")
            
            # Search button
            if st.button("🔍 מצא מכרזים מתאימים", key="search_button"):
                profile_data = {
                    'ימי_מילואים_מ-7.10.23': days_since_oct,
                    'תעודת_מילואים_פעיל': active_card,
                    'ימי_מילואים_ב-6_שנים': days_in_6_years,
                    'סיווג_נכות': disability_status if disability_status != "אין" else "",
                    'חסר_דיור': housing_status,
                    'אזור_מועדף': preferred_area,
                    'בן/בת_זוג_זכאי': spouse_eligible
                }
                
                st.session_state.matches = find_matching_tenders(profile_data)
                st.session_state.search_performed = True
                st.rerun()

    with results_col:
        if st.session_state.search_performed:
            if not st.session_state.matches.empty:
                st.markdown("### ✅ מכרזים מתאימים לפרופיל שלך")
                
                st.success(f"נמצאו {len(st.session_state.matches)} מכרזים מתאימים לך!")
                
                st.info("🔗 **על מנת להתקדם להגשה יש להכנס למערכת המכרזים של רמ״י ולפתוח את המכרז שבחרתם לפי מספר המכרז שהוצג למטה.**\n\n**לסיוע בתהליך המלא אנו מזמינים אתכם ליצור קשר עם הצוות שלנו בכתובת הבאה:** yuvalk@apm.law")
                
                st.markdown("---")
                
                # Render tender cards
                for _, tender in st.session_state.matches.iterrows():
                    render_tender_card(tender)
                
            else:
                st.warning("😔 לא נמצאו מכרזים מתאימים")
                st.info("נסה לשנות את הקריטריונים או לבדוק שוב מאוחר יותר")
        else:
            st.info("🏠 **התחל למצוא את המכרז שלך**")
            st.write("מלא את הפרטים בטופס משמאל לקבלת מכרזים מותאמים אישית")

if __name__ == "__main__":
    main() 