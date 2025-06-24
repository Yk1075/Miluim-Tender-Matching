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

# RTL and styling CSS
st.markdown("""
<style>
    /* RTL and font settings */
    * {
        direction: rtl;
        text-align: right;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    /* Background and main container */
    .main {
        background-color: #ffffff;
        padding: 1rem;
    }
    
    .stApp {
        background-color: #f5f5f5;
    }
    
    /* Text color - ensure all text is dark and readable */
    * {
        color: #262626 !important;
    }
    
    .stMarkdown, .stMarkdown p, .stMarkdown div, 
    .stInfo, .stInfo p, .stInfo div,
    .stSuccess, .stSuccess p, .stSuccess div,
    .stWarning, .stWarning p, .stWarning div,
    .stError, .stError p, .stError div {
        color: #262626 !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #1f1f1f !important;
        font-weight: bold !important;
        text-align: center !important;
    }
    
    /* Center alignment for titles */
    .stTitle, .stSubheader {
        text-align: center !important;
    }
    
    /* Info boxes styling */
    .stInfo {
        background-color: #f0f8ff !important;
        border: 1px solid #1e3a8a !important;
        border-radius: 8px !important;
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
    
    /* Expander styling */
    .stExpander details summary {
        font-size: 18px !important;
        font-weight: bold !important;
        color: #1f1f1f !important;
    }
    
    /* Hide streamlit elements */
    .stDeployButton, .stDecoration, #MainMenu, footer {
        display: none !important;
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
        
        # Link to ILA system
        st.markdown("""
        <div style="text-align: center; margin-top: 1rem;">
            <a href="https://apps.land.gov.il/MichrazimSite/#/search" target="_blank" style="
                display: inline-block;
                padding: 0.75rem 1.5rem;
                background-color: #1e3a8a;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-weight: bold;
                text-align: center;
            ">
                🌐 למערכת המכרזים של רמ״י
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