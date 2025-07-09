import streamlit as st
import pandas as pd
from create_comprehensive_matches import (
    is_miluim_soldier, 
    get_profile_category, 
    check_area_match, 
    check_eligibility_match, 
    check_housing_match
)
from datetime import datetime, timedelta

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

def format_israeli_date(date_input):
    """Convert date from any format to Israeli format DD.M.YYYY בשעה HH:MM"""
    if not date_input or str(date_input) == 'nan' or str(date_input) == 'לא צוין':
        return 'לא צוין'
    
    try:
        # Handle pandas timestamp or datetime objects directly
        if hasattr(date_input, 'day') and hasattr(date_input, 'month'):
            dt = date_input
        else:
            # Convert to string and try to parse
            date_str = str(date_input).strip()
            
            # Try different date formats
            if 'T' in date_str:
                # ISO format with T
                dt = datetime.fromisoformat(date_str.replace('T', ' ').split('.')[0])
            elif len(date_str) == 10:
                # YYYY-MM-DD format
                dt = datetime.strptime(date_str, '%Y-%m-%d')
            else:
                # YYYY-MM-DD HH:MM:SS format
                dt = datetime.strptime(date_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
        
        # Format to Israeli style: DD.M.YYYY בשעה HH:MM
        day = dt.day
        month = dt.month
        year = dt.year
        hour = dt.hour if hasattr(dt, 'hour') else 0
        minute = dt.minute if hasattr(dt, 'minute') else 0
        
        return f"{day}.{month}.{year} בשעה {hour:02d}:{minute:02d}"
        
    except (ValueError, TypeError, AttributeError) as e:
        # If parsing fails, return original string
        return str(date_input)

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
                st.success(f"🏅 מגרשים לנכי צה\"ל: {disability_plots}")
        
        # Row 3: Dates - same size as plot count and priority
        date_col_left, date_col_right = st.columns([1, 1])
        
        with date_col_left:
            publish_date = tender.get('תאריך פרסום חוברת המכרז', 'לא צוין')
            formatted_publish_date = format_israeli_date(publish_date)
            st.markdown(f"📅 **תאריך פרסום חוברת:** {formatted_publish_date}")
        
        with date_col_right:
            deadline = tender.get('מועד אחרון להגשה', 'לא צוין')
            formatted_deadline = format_israeli_date(deadline)
            st.markdown(f"⏰ **מועד אחרון:** {formatted_deadline}")
        
        # Row 4: Eligibility and housing requirements
        req_col_left, req_col_right = st.columns([1, 1])
        
        with req_col_left:
            eligibility = tender.get('מי רשאי להגיש', 'לא צוין')
            st.markdown(f"👥 **זכאות:** {eligibility}")
        
        with req_col_right:
            housing_req = tender.get('סטטוס דיור נדרש', 'לא צוין')
            if housing_req and str(housing_req) != 'nan':
                # Show "עדיפות לחסרי דיור" instead of "לא צוין"
                if housing_req == 'לא צוין':
                    housing_req = 'עדיפות לחסרי דיור'
                st.markdown(f"🏠 **דרישת דיור:** {housing_req}")
        
        # Row 5: Button on the left side
        button_col_left, button_col_right = st.columns([1, 1])
        
        with button_col_left:
            # Direct link button - opens immediately without additional clicks
            st.markdown(f"""
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
                width: 100%;
            ">
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
רשות מקרקעי ישראל (רמ"י) פרסמה בחודשים האחרונים מכרזים מיוחדים המעניקים הטבות למשרתי ומשרתות המילואים ברכישת מגרשים לבנייה. כדי לסייע לכם למצוא בקלות את המכרזים הרלוונטיים עבורכם, יצרנו מערכת חכמה המתאימה את המכרזים הרלוונטיים על פי תשובותיכם לשאלות מטה. אנו מקווים שתמצאו במערכת כלי שימושי ונשמח ללוות אתכם בתהליך לבניית בית חלומותיכם.

**שימו לב:** הפרטים המלאים והמדויקים נמצאים בדרך כלל בחוברת המכרז עצמה. מומלץ לסמן לעצמכם תזכורת לתאריך פרסום החוברת ולמועד האחרון להגשת ההצעות.

**המידע באתר מוצג כפי שהוא (as is) ומבוסס על פרסומי רשות מקרקעי ישראל (רמ"י). אין לראות במידע זה תחליף לייעוץ משפטי, מקצועי או אחר, והשימוש בו והסתמכות על האמור בו נעשה על אחריות המשתמש בלבד. האתר אינו קשור באופן רשמי לרשות מקרקעי ישראל.**
""")
    
    with col2:
        st.info("""
**🪖 ההטבות העיקריות לחיילי מילואים:**
הטבה של 10% נוספים בשיעורי התשלום על הקרקע, מעבר להטבות החלות על אזורי עדיפות לאומית (בכפוף לתקרות).
הטבה נוספת של 10%-35% על מחיר המגרש, בהתאם לאזור העדיפות הלאומית (עד 100,000 ₪ לזכאי יחיד, או עד 200,000 ₪ לזוג ששני בני הזוג זכאים).

**🎖️ הטבות עיקריות לנכי צה״ל:**
אפשרות להשתתפות במכרזים ייעודיים לנכי צה״ל.
קדימות אפשרית בהרשמה ובהגרלה.
נכים בדרגת נכות 100%+ (מיוחדת) עשויים להיות זכאים לתשלום מופחת של כ־31% מערך הקרקע, בכפוף לתנאים ולתקרות (לרוב עד 2,000,000 ₪, לא כולל מע״מ והוצאות פיתוח).

**📞 צריכים עזרה?**

צוות המשרד זמין לליווי בכל התהליך - yuvalk@apm.law

[למדיניות הפרטיות](https://drive.google.com/uc?export=download&id=1CUQc8SVnwxVdZe0-eHwQQfKg2hjEL6qG)     [לתקנון](https://drive.google.com/uc?export=download&id=15Ui-erPaWxitHOdQR7vouyZkSXfpoTcn)
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
            
            disability_status = st.selectbox(
                "סיווג נכות",
                options=["אין", "נכות קשה", "100% ומעלה"],
                index=["אין", "נכות קשה", "100% ומעלה"].index(st.session_state.profile_data.get('סיווג_נכות', 'אין')),
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
            
            preferred_area = st.selectbox(
                "אזור מועדף",
                options=["דרום", "צפון", "ירושלים", "מרכז", "יהודה ושומרון"],
                index=["דרום", "צפון", "ירושלים", "מרכז", "יהודה ושומרון"].index(st.session_state.profile_data.get('אזור_מועדף', 'דרום')),
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
                
                # Government website link
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