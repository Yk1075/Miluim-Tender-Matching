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
try:
    st.image("apm_logo.png", width=90)
except:
    # אם אין לוגו, הצג כותרת
    st.markdown("### APM משרד עורכי דין")

# Simple CSS for RTL and blue theme
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        color: #262626 !important;
    }
    
    .main {
        background-color: #ffffff;
        padding: 1rem;
    }
    
    .stApp {
        background-color: #f5f5f5;
    }
    
    /* Force dark text color for all elements */
    .stMarkdown, .stMarkdown p, .stMarkdown div, .stInfo, .stInfo p, .stInfo div {
        color: #262626 !important;
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
        background: #3b82f6 !important;
        color: white !important;
        border: 2px solid #1d4ed8 !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: bold !important;
        font-size: 16px !important;
        width: 100% !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background: #2563eb !important;
        border-color: #1e40af !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15) !important;
        transform: translateY(-1px) !important;
    }
    
    .stButton > button:active {
        background: #1d4ed8 !important;
        transform: translateY(0) !important;
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
    
    /* Success message styling */
    .stSuccess {
        background-color: #dcfce7 !important;
        border: 1px solid #16a34a !important;
    }
    
    /* Warning message styling */
    .stWarning {
        background-color: #fef3c7 !important;
        border: 1px solid #d97706 !important;
    }
    
    /* Error message styling */
    .stError {
        background-color: #fee2e2 !important;
        border: 1px solid #dc2626 !important;
    }
</style>
""", unsafe_allow_html=True)

def validate_profile_data(profile_data):
    """Validate profile data and return error messages if any"""
    errors = []
    
    # Check required fields
    if not profile_data.get('אזור_מועדף'):
        errors.append("יש לבחור אזור מועדף")
    
    # Check logical consistency
    if (profile_data.get('ימי_מילואים_מ-7.10.23', 0) == 0 and 
        profile_data.get('תעודת_מילואים_פעיל') == 'לא' and 
        profile_data.get('ימי_מילואים_ב-6_שנים', 0) == 0 and
        profile_data.get('סיווג_נכות') == 'אין'):
        errors.append("על פי הנתונים שהזנת, אינך זכאי להטבות מכרזי דיור מיוחדים")
    
    return errors

def find_matching_tenders(profile_data):
    """Find tenders that match the user profile"""
    try:
        # Validate profile data
        validation_errors = validate_profile_data(profile_data)
        if validation_errors:
            return pd.DataFrame(), validation_errors
        
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
                    'אזור עדיפות': tender['אזור עדיפות'],
                    'מי רשאי להגיש': tender['מי רשאי להגיש'],
                    'סטטוס דיור נדרש': tender['סטטוס דיור נדרש']
                })
        
        return pd.DataFrame(matching_tenders), []
        
    except FileNotFoundError as e:
        return pd.DataFrame(), [f"קובץ הנתונים לא נמצא: {str(e)}"]
    except Exception as e:
        return pd.DataFrame(), [f"אירעה שגיאה בעת חיפוש המכרזים: {str(e)}"]

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
            st.markdown(f"🏠 **מספר מגרשים:** {tender['מספר מגרשים']}")
        
        with col_right:
            # Priority on the RIGHT - normal size
            priority_status = str(tender.get('אזור עדיפות', ''))
            if priority_status == "A":
                st.error("🔥 עדיפות א'")
            elif priority_status == "B":
                st.warning("⚡ עדיפות ב'")
            else:
                st.info("📋 ללא עדיפות לאומית")
        
        # Row 2: Special plots info
        special_col_left, special_col_right = st.columns([1, 1])
        
        with special_col_left:
            miluim_plots = tender.get('מגרשים לחיילי מילואים', 0)
            if miluim_plots and str(miluim_plots) != 'nan' and str(miluim_plots) != '0':
                st.success(f"🎖️ מגרשים למילואים: {miluim_plots}")
        
        with special_col_right:
            disability_plots = tender.get('מגרשים לנכי צה"ל', 0)
            if disability_plots and str(disability_plots) != 'nan' and str(disability_plots) != '0':
                st.success(f"🎖️ מגרשים לנכי צה\"ל: {disability_plots}")
        
        # Row 3: Dates - same size as plot count and priority
        date_col_left, date_col_right = st.columns([1, 1])
        
        with date_col_left:
            publish_date = tender.get('תאריך פרסום חוברת המכרז', 'לא צוין')
            st.markdown(f"📅 **תאריך פרסום חוברת:** {publish_date}")
        
        with date_col_right:
            deadline = tender.get('מועד אחרון להגשה', 'לא צוין')
            st.markdown(f"⏰ **מועד אחרון:** {deadline}")
        
        # Row 4: Eligibility and housing requirements
        req_col_left, req_col_right = st.columns([1, 1])
        
        with req_col_left:
            eligibility = tender.get('מי רשאי להגיש', 'לא צוין')
            st.markdown(f"👥 **זכאות:** {eligibility}")
        
        with req_col_right:
            housing_req = tender.get('סטטוס דיור נדרש', 'לא צוין')
            if housing_req and str(housing_req) != 'nan':
                st.markdown(f"🏠 **דרישת דיור:** {housing_req}")
        
        # Row 5: Button on the left side
        button_col_left, button_col_right = st.columns([1, 1])
        
        with button_col_left:
            # Direct link button - opens immediately without additional clicks
            st.markdown(f"""
            <a href="https://apps.land.gov.il/MichrazimSite/#/search" target="_blank" style="
                display: inline-block;
                padding: 0.75rem 1rem;
                background-color: #059669;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                border: 2px solid #047857;
                font-weight: bold;
                font-size: 14px;
                text-align: center;
                cursor: pointer;
                width: 100%;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                transition: all 0.2s ease;
            " onmouseover="this.style.backgroundColor='#047857'; this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 8px rgba(0, 0, 0, 0.15)';" 
              onmouseout="this.style.backgroundColor='#059669'; this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(0, 0, 0, 0.1)';">
                🌐 למערכת המכרזים של רמ״י
            </a>
            """, unsafe_allow_html=True)

def show_profile_summary(profile_data):
    """Show a summary of the user's profile"""
    st.markdown("### 📋 סיכום הפרופיל שלך")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**פרטי שירות:**")
        st.write(f"• ימי מילואים מ-7.10.23: {profile_data.get('ימי_מילואים_מ-7.10.23', 0)}")
        st.write(f"• תעודת מילואים פעיל: {profile_data.get('תעודת_מילואים_פעיל', 'לא')}")
        st.write(f"• ימי מילואים ב-6 שנים: {profile_data.get('ימי_מילואים_ב-6_שנים', 0)}")
        st.write(f"• סיווג נכות: {profile_data.get('סיווג_נכות', 'אין')}")
    
    with col2:
        st.markdown("**העדפות אישיות:**")
        st.write(f"• אזור מועדף: {profile_data.get('אזור_מועדף', 'לא נבחר')}")
        st.write(f"• חסר/ת דיור: {profile_data.get('חסר_דיור', 'לא')}")
        st.write(f"• בן/בת זוג זכאי/ת: {profile_data.get('בן/בת_זוג_זכאי', 'לא')}")
    
    # Determine profile category
    profile_series = pd.Series(profile_data)
    category = get_profile_category(profile_series)
    
    if category == 'נכי צהל':
        st.success(f"✅ **קטגוריה:** {category} - זכאי להטבות מיוחדות!")
    elif category == 'חיילי מילואים':
        st.success(f"✅ **קטגוריה:** {category} - זכאי להטבות מילואים!")
    else:
        st.warning(f"⚠️ **קטגוריה:** {category} - ייתכן ולא תהיה זכאי להטבות מיוחדות")

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
**איך זה עובד?**

על בסיס תנאי הזכאות והמכרזים שפורסמו על ידי רשות מקרקעי ישראל המערכת יודעת להתאים לך את המכרזים הייעודיים עם התאמה מקסימלית. 

פשוט עונים על השאלות מטה והמכרזים הרלוונטים כבר יעלו לפניכם כך שתוכלו להתקדם מבלי לבזבז זמן חשוב על נבירה באתר של רמ״י.

**שימו לב:** במרבית המכרזים הפרטים המלאים יופיעו בחוברת המכרז - כך ששווה במציאת המכרזים הרלוונטים לשים לכם תזכורת לתאריך פרסום החוברת ותאריך ההגשה האחרון שלא תפספסו!

**השימוש במידע המופיע באתר אינו מהווה תחליף לקבלת ייעוץ או טיפול משפטי, מקצועי או אחר והסתמכות על האמור בו היא באחריות המשתמש בלבד.**
""")
    
    with col2:
        st.info("""
**💰 ההטבות העיקריות**

• הנחות של 10-35% באזורי עדיפות לאומית

• הנחות נוספות של 10-35% ממחיר המגרש

• קדימות בהגרלות למילואים ונכי צה"ל

• אפשרות לרכישת מגרשים בתנאים מועדפים

**כלל ההטבות מפורטות בקישור הבא:**  
[פירוט מלא של ההטבות לחיילי מילואים](https://www.gov.il/he/pages/pr-miluaim-29042025)

לכל תקלה באתר או בחיפוש עדכנו אותנו ב- yuvalk@apm.law
""")

    st.markdown("---")

    # Layout: Search (30%) + Results (70%)
    search_col, results_col = st.columns([0.3, 0.7], gap="medium")

    # Initialize session state
    if 'search_performed' not in st.session_state:
        st.session_state.search_performed = False
    if 'matches' not in st.session_state:
        st.session_state.matches = pd.DataFrame()
    if 'profile_data' not in st.session_state:
        st.session_state.profile_data = {}
    if 'validation_errors' not in st.session_state:
        st.session_state.validation_errors = []

    with search_col:
        with st.container():
            st.markdown("### 📋 פרטים אישיים")
            
            # Service details section
            st.markdown("#### 🎖️ פרטי שירות")
            
            days_since_oct = st.number_input(
                "ימי מילואים מ-7.10.23",
                min_value=0,
                value=st.session_state.profile_data.get('ימי_מילואים_מ-7.10.23', 0),
                help="מספר ימי המילואים שביצעת מתאריך 7.10.23. נדרשים לפחות 45 ימים לזכאות.",
                key="days_since_oct"
            )
            
            active_card = st.selectbox(
                "תעודת מילואים פעיל?",
                options=["לא", "כן"],
                index=0 if st.session_state.profile_data.get('תעודת_מילואים_פעיל', 'לא') == 'לא' else 1,
                help="בחר 'כן' אם יש ברשותך תעודת מילואים פעיל תקפה.",
                key="active_card"
            )
            
            days_in_6_years = st.number_input(
                "ימי מילואים ב-6 שנים",
                min_value=0,
                value=st.session_state.profile_data.get('ימי_מילואים_ב-6_שנים', 0),
                help="סך ימי המילואים שביצעת במצטבר בפרק זמן של עד 6 שנים קלנדריות. נדרשים לפחות 80 ימים לזכאות.",
                key="days_in_6_years"
            )
            
            # Safe index for disability status
            disability_options = ["אין", "נכות קשה", "100% ומעלה"]
            disability_value = st.session_state.profile_data.get('סיווג_נכות', 'אין')
            disability_index = disability_options.index(disability_value) if disability_value in disability_options else 0
            
            disability_status = st.selectbox(
                "סיווג נכות",
                options=disability_options,
                index=disability_index,
                help="בחר את סיווג הנכות המתאים לך - זה משפיע על הזכאות למכרזים מיוחדים.",
                key="disability_status"
            )
            
            st.markdown("#### 🏠 העדפות דיור")
            
            housing_status = st.selectbox(
                "חסר/ת דיור?",
                options=["לא", "כן"],
                index=0 if st.session_state.profile_data.get('חסר_דיור', 'לא') == 'לא' else 1,
                help="בחר 'כן' אם הינך מוגדר כחסר דיור לפי הגדרות רמ״י.",
                key="housing_status"
            )
            
            # Safe index for preferred area
            area_options = ["דרום", "צפון", "ירושלים", "מרכז", "יהודה ושומרון"]
            area_value = st.session_state.profile_data.get('אזור_מועדף', 'דרום')
            area_index = area_options.index(area_value) if area_value in area_options else 0
            
            preferred_area = st.selectbox(
                "אזור מועדף",
                options=area_options,
                index=area_index,
                help="בחר את האזור המועדף עליך למגורים.",
                key="preferred_area"
            )
            
            spouse_eligible = st.selectbox(
                "בן/בת זוג זכאי/ת?",
                options=["לא", "כן"],
                index=0 if st.session_state.profile_data.get('בן/בת_זוג_זכאי', 'לא') == 'לא' else 1,
                help="בחר 'כן' אם בן/בת הזוג גם זכאי/ת להטבות.",
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
                
                matches, validation_errors = find_matching_tenders(profile_data)
                st.session_state.matches = matches
                st.session_state.profile_data = profile_data
                st.session_state.validation_errors = validation_errors
                st.session_state.search_performed = True
                st.rerun()

    with results_col:
        if st.session_state.search_performed:
            # Show validation errors if any
            if st.session_state.validation_errors:
                for error in st.session_state.validation_errors:
                    st.error(f"❌ {error}")
                st.markdown("---")
            
            # Show profile summary
            if st.session_state.profile_data:
                show_profile_summary(st.session_state.profile_data)
                st.markdown("---")
            
            if not st.session_state.matches.empty:
                st.markdown("### ✅ מכרזים מתאימים לפרופיל שלך")
                
                # Show messages BEFORE the tender cards
                st.success(f"נמצאו {len(st.session_state.matches)} מכרזים מתאימים לך!")
                
                # Government website link - show prominently at the top
                st.info("""
🔗 **על מנת להתקדם להגשה יש להכנס למערכת המכרזים של רמ״י ולפתוח את המכרז שבחרתם לפי מספר המכרז שהוצג למטה.**

**לסיוע בתהליך המלא אנו מזמינים אתכם ליצור קשר עם הצוות שלנו בכתובת:** yuvalk@apm.law
""")
                
                st.markdown("---")
                
                # Render tender cards using expander
                for _, tender in st.session_state.matches.iterrows():
                    render_tender_with_streamlit(tender)
                    st.markdown("---")
                
            else:
                if not st.session_state.validation_errors:  # Only show if no validation errors
                    st.warning("😔 לא נמצאו מכרזים מתאימים לפרופיל שלך")
                    st.info("""
**מה אפשר לעשות?**
• נסה לשנות את האזור המועדף
• בדוק שוב מאוחר יותר - מכרזים חדשים מתפרסמים באופן קבוע
• צור קשר עם הצוות שלנו לבדיקה ידנית של האפשרויות
""")
        else:
            st.info("🏠 **התחל למצוא את המכרז שלך**")
            st.write("מלא את הפרטים בטופס משמאל לקבלת מכרזים מותאמים אישית")

if __name__ == "__main__":
    main() 