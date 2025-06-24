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
    
    /* Input container fixes */
    .stSelectbox > div[data-baseweb="select"] > div,
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        color: #2d3748 !important;
        font-weight: 500 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        transition: all 0.2s ease !important;
    }
    
    /* Selectbox specific styling */
    .stSelectbox > div[data-baseweb="select"] > div {
        min-height: 48px !important;
        background-color: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
    }
    
    /* Dropdown styling */
    .stSelectbox > div[data-baseweb="select"] > div > div {
        color: #2d3748 !important;
        font-weight: 500 !important;
        padding: 8px 12px !important;
    }
    
    /* Number input specific */
    .stNumberInput > div > div > input {
        background-color: #ffffff !important;
        color: #2d3748 !important;
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
    
    /* Expander styling */
    .stExpander {
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        margin: 1rem 0 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    
    .stExpander details summary {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%) !important;
        padding: 1rem !important;
        font-weight: 600 !important;
        color: #2d3748 !important;
        border-radius: 12px !important;
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
                "🗓️ ימי מילואים מ-7.10.23",
                min_value=0,
                value=0,
                help="❓ מספר ימי המילואים שביצעת מתאריך 7.10.23. זהו תנאי מרכזי להטבות! \n\n🔍 פרטי ההטבה:\n• מעל 45 ימים = הנחה של 10-35% ממחיר המגרש\n• נדרש אישור רשמי על השירות במלחמת 'חרבות ברזל'\n• ככל שיותר ימים, כך ההנחה גדולה יותר",
                key="days_since_oct"
            )
            
            active_card = st.selectbox(
                "🪖 תעודת מילואים פעיל?",
                options=["לא", "כן"],
                help="❓ האם יש ברשותך תעודת מילואים פעיל? \n\n🔍 מה זה נותן:\n• זכאות מיוחדת למכרזים ייעודיים\n• עדיפות בהגרלות\n• הנחות נוספות במחיר המגרש\n\n📄 אישורים נדרשים:\n• אישור למשרת מילואים פעיל (6 שנים)\n• או אישור למשרת מילואים פעיל בעבר",
                key="active_card"
            )
            
            days_in_6_years = st.number_input(
                "📊 ימי מילואים ב-6 שנים",
                min_value=0,
                value=0,
                help="❓ סך כל ימי המילואים שביצעת במצטבר בפרק זמן של עד 6 שנים קלנדריות (מאז 2000). \n\n🔍 הסבר על ההטבות:\n• 50+ ימים = זכאות להנחות מיוחדות\n• 100+ ימים = הנחות משמעותיות במחיר המגרש\n• נחשב הפרק הטוב ביותר של 6 שנים רצופות\n\n💡 דוגמה: שירתת ב-2018, 2019, 2020, 2021, 2022, 2023",
                key="days_in_6_years"
            )
            
            disability_status = st.selectbox(
                "🎖️ סיווג נכות",
                options=["אין", "נכות קשה", "100% ומעלה"],
                help="❓ סיווג הנכות שלך לפי משרד הביטחון. זהו תנאי מרכזי להטבות נכי צה״ל! \n\n🔍 הטבות לפי סיווג:\n• נכות קשה = מגרשים ייעודיים + הנחות של 35%\n• 100% ומעלה = הטבות מקסימליות + עדיפות עליונה\n• מגרשים מיוחדים רק לנכי צה״ל\n\n📄 נדרש: אישור נכות מהמוסד לביטוח לאומי",
                key="disability_status"
            )
            
            housing_status = st.selectbox(
                "🏠 חסר/ת דיור?",
                options=["לא", "כן"],
                help="❓ האם אתה מוגדר רשמית כחסר דיור? זה מעניק הטבות נוספות משמעותיות! \n\n🔍 מה זה נותן:\n• הנחות נוספות של 10-20% במחיר המגרש\n• עדיפות בהגרלות מיוחדות\n• זכאות למכרזים ייעודיים לחסרי דיור\n\n📄 איך לבדוק:\n• כנס לאתר הממשלתי: gov.il\n• חפש 'אישור חוסר דיור'\n• הגש בקשה אם עדיין לא עשית זאת",
                key="housing_status"
            )
            
            preferred_area = st.selectbox(
                "🗺️ אזור מועדף",
                options=["דרום", "צפון", "ירושלים", "מרכז", "יהודה ושומרון"],
                help="❓ באיזה אזור בארץ תרצה לגור? המערכת תמצא מכרזים רק באזור שבחרת. \n\n🔍 מידע על האזורים:\n• דרום = באר שבע, אשקלון, נתיבות וסביבה\n• צפון = חיפה, נהריה, כרמיאל וסביבה\n• מרכז = תל אביב, פתח תקווה, ראשון לציון\n• ירושלים = ירושלים ויישובי הסביבה\n• יהודה ושומרון = יישובים מעבר לקו הירוק\n\n💡 טיפ: אזורי עדיפות לאומית (א', ב') מציעים הנחות גדולות יותר!",
                key="preferred_area"
            )
            
            spouse_eligible = st.selectbox(
                "💑 בן/בת זוג זכאי/ת?",
                options=["לא", "כן"],
                help="❓ האם בן/בת הזוג שלך גם זכאי/ת להטבות? זה יכול להכפיל את ההטבות! \n\n🔍 מתי בן/בת זוג זכאי/ת:\n• שירת/ה גם כן במילואים (45+ ימים)\n• נכה/נכת צה״ל\n• בעל/ת תעודת מילואים פעיל\n• חסר/ת דיור\n\n💰 הטבות כפולות:\n• הנחות מצטברות (עד 70% במקרים מיוחדים!)\n• עדיפות גבוהה יותר בהגרלות\n• זכאות למכרזים מיוחדים לזוגות זכאים\n\n📄 נדרש: אישורים עבור שני בני הזוג",
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