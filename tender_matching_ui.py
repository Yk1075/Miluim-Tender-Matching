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

# הצגת לוגו כתמונה מהשורש
st.image("apm_logo.png", width=90)

# Simple CSS for RTL and blue theme
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    .main {
        background-color: #ffffff;
        padding: 1rem;
    }
    
    .stApp {
        background-color: #f5f5f5;
    }
    
    /* Force center alignment for header */
    .center-header {
        text-align: center !important;
        direction: ltr !important;
        width: 100% !important;
        display: block !important;
    }
    
    .center-header h1 {
        text-align: center !important;
        margin: 0 auto !important;
        display: block !important;
    }
    
    .center-header h3 {
        text-align: center !important;
        margin: 0 auto !important;
        display: block !important;
    }
    
    /* Blue theme for info boxes */
    .stInfo {
        background-color: #f0f8ff !important;
        border: 1px solid #1e3a8a !important;
    }
    
    /* Hide streamlit elements */
    .stDeployButton, .stDecoration, #MainMenu, footer {
        display: none !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: #1e3a8a !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: bold !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background: #1e40af !important;
    }
    
    /* Form inputs */
    .stSelectbox label, .stNumberInput label {
        font-weight: bold !important;
        color: #374151 !important;
    }
    
    /* Simple RTL styling for better Hebrew display */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    
    /* Make expander headers larger and bold */
    .stExpander details summary {
        font-size: 18px !important;
        font-weight: bold !important;
    }
    
    .stExpander details summary p {
        font-size: 18px !important;
        font-weight: bold !important;
        margin: 0 !important;
    }
    
    /* Compact, bold, square APM logo */
    .top-left-logo {
        position: fixed;
        top: 15px;
        left: 15px;
        z-index: 999;
        background: #000;
        width: 90px;
        height: 90px;
        padding: 6px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.18);
        font-family: 'Arial', 'Helvetica', sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .logo-main {
        font-size: 26px;
        font-weight: 900;
        color: white;
        letter-spacing: 6px;
        margin-bottom: 2px;
        line-height: 1.1;
    }
    .logo-second-row {
        font-size: 18px;
        font-weight: 900;
        color: white;
        letter-spacing: 6px;
        margin-bottom: 2px;
        line-height: 1.1;
    }
    .logo-subtitle {
        font-size: 7px;
        color: white;
        font-weight: 400;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        line-height: 1.2;
        white-space: nowrap;
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

def render_tender_with_streamlit(tender):
    """Render tender card with blue background using expander"""
    
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
    
    # Create blue card using expander with custom styling
    header_text = f"🏆 מכרז #{tender['מספר מכרז']} | 📍 {location_display}"
    with st.expander(header_text, expanded=True):
        
        # Row 1: Priority (RIGHT) and Plot count (LEFT) - same size
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            # Plot count on the LEFT - normal size
            st.markdown(f"🏠 {tender['מספר מגרשים']}")
        
        with col_right:
            # Priority on the RIGHT - normal size
            priority_status = str(tender.get('אזור עדיפות', ''))
            if priority_status == "A":
                st.error("🔥 עדיפות א'")
            elif priority_status == "B":
                st.warning("⚡ עדיפות ב'")
            else:
                st.info("📋 ללא עדיפות לאומית")
        
        # Row 2: Dates - same size as plot count and priority
        date_col_left, date_col_right = st.columns([1, 1])
        
        with date_col_left:
            st.markdown(f"📅 תאריך פרסום חוברת המכרז: {tender['תאריך פרסום חוברת המכרז']}")
        
        with date_col_right:
            st.markdown(f"⏰ מועד אחרון: {tender['מועד אחרון להגשה']}")
        
        # Row 3: Button on the left side
        button_col_left, button_col_right = st.columns([1, 1])
        
        with button_col_left:
            # Direct link button - opens immediately without additional clicks
            st.markdown("""
            <a href="https://apps.land.gov.il/MichrazimSite/#/search" target="_blank" style="
                display: inline-block;
                padding: 0.5rem 1rem;
                background-color: #1f2937;
                color: white;
                text-decoration: none;
                border-radius: 0.375rem;
                font-weight: 500;
                text-align: center;
                border: none;
                cursor: pointer;
            ">
                🌐 למערכת המכרזים של רמ״י
            </a>
            """, unsafe_allow_html=True)

def main():
    # Override Streamlit CSS to center everything
    st.markdown("""
    <style>
    .main > div {
        text-align: center !important;
    }
    .stMarkdown > div {
        text-align: center !important;
    }
    h1 {
        text-align: center !important;
    }
    h3 {
        text-align: center !important;
    }
    .stTitle {
        text-align: center !important;
    }
    .stSubheader {
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Use Streamlit's built-in title and subheader
    st.title("🏠 מילואים וזוכים - מערכת התאמת מכרזים")
    st.subheader("מצא את המכרז המושלם עבורך בהתאם לפרופיל השירות והעדפותיך")
    
    # Info sections using Streamlit columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **💡 איך זה עובד?**
        
        המערכת בודקת את הזכאות שלך על בסיס ימי המילואים, נכות וסטטוס דיור, ומציגה רק מכרזים רלוונטיים לפרופיל שלך
        """)
    
    with col2:
        st.info("""
        **💰 ההטבות העיקריות**
        
        • הנחות של 10-35% באזורי עדיפות לאומית
        
        • הנחות נוספות של 10-35% ממחיר המגרש
        
        • קדימות בהגרלות למילואים ונכי צה"ל
        """)

    st.markdown("---")

    # Layout: Search (30%) + Results (70%)
    search_col, results_col = st.columns([0.3, 0.7], gap="medium")

    # Initialize session state
    if 'search_performed' not in st.session_state:
        st.session_state.search_performed = False
    if 'matches' not in st.session_state:
        st.session_state.matches = pd.DataFrame()

    with search_col:
        with st.container():
            st.markdown("### 📋 פרטים אישיים")
            
            days_since_oct = st.number_input(
                "ימי מילואים מ-7.10.23",
                min_value=0,
                value=0,
                help="מספר ימי המילואים שביצעת מתאריך 7.10.23, שים לב כי בהגשת המכרז יהיה עליך לצרף אישור על שירות של מעל 45 ימים בזמן מלחמת 'חרבות ברזל'.",
                key="days_since_oct"
            )
            
            active_card = st.selectbox(
                "תעודת מילואים פעיל?",
                options=["לא", "כן"],
                help="בחר 'כן' אם יש ברשותך תעודת מילואים פעיל, שים לב כי בהגשת המכרז יהיה עליך לצרף אישור למשרת מילואים פעיל שש שנתי או אישור למשרת מילואים פעיל שש שנתי בעבר.",
                key="active_card"
            )
            
            days_in_6_years = st.number_input(
                "ימי מילואים ב-6 שנים",
                min_value=0,
                value=0,
                help="סך ימי המילואים שביצעת במצטבר (מאז שנת 2000), בפרק זמן של עד 6 שנים קלנדריות.",
                key="days_in_6_years"
            )
            
            disability_status = st.selectbox(
                "סיווג נכות",
                options=["אין", "נכות קשה", "100% ומעלה"],
                help="בחר את סיווג הנכות המתאים לך - זה משפיע על הזכאות למכרזים מיוחדים ועל היקף ההטבות",
                key="disability_status"
            )
            
            housing_status = st.selectbox(
                "חסר/ת דיור?",
                options=["לא", "כן"],
                help="בחר 'כן' אם הינך מוגדר כחסר דיור לפי האתר הממשלתי: https://www.gov.il/he/service/certificate-of-homelessness - זה משפיע על היקף ההטבות שלך",
                key="housing_status"
            )
            
            preferred_area = st.selectbox(
                "אזור מועדף",
                options=["דרום", "צפון", "ירושלים", "מרכז", "יהודה ושומרון"],
                help="בחר את האזור המועדף עליך למגורים - המערכת תציג רק מכרזים באזור הנבחר",
                key="preferred_area"
            )
            
            spouse_eligible = st.selectbox(
                "בן/בת זוג זכאי/ת?",
                options=["לא", "כן"],
                help="בחר 'כן' אם בן/בת הזוג זכאי/ת להטבות (גם הוא/היא מילואים או נכה) - זה יכול להכפיל את ההטבות שלכם",
                key="spouse_eligible"
            )

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
                
                # Show messages BEFORE the tender cards
                st.success(f"נמצאו {len(st.session_state.matches)} מכרזים מתאימים לך!")
                
                # Government website link - show prominently at the top
                st.info("🔗 **על מנת להתקדם להגשה יש להכנס למערכת המכרזים של רמ״י ולפתוח את המכרז שבחרתם לפי מספר המכרז שהוצג למטה.**\n\n**לסיוע בתהליך המלא אנו מזמינים אתכם ליצור קשר עם הצוות שלנו בכתובת הבאה:** yuvalk@apm.law")
                
                st.markdown("---")
                
                # Render tender cards using expander
                for _, tender in st.session_state.matches.iterrows():
                    render_tender_with_streamlit(tender)
                
            else:
                st.warning("😔 לא נמצאו מכרזים מתאימים")
                st.info("נסה לשנות את הקריטריונים או לבדוק שוב מאוחר יותר")
        else:
            st.info("🏠 **התחל למצוא את המכרז שלך**")
            st.write("מלא את הפרטים בטופס משמאל לקבלת מכרזים מותאמים אישית")

if __name__ == "__main__":
    main() 