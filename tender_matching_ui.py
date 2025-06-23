import streamlit as st
import pandas as pd
from create_comprehensive_matches import (
    is_miluim_soldier, 
    get_profile_category, 
    check_area_match, 
    check_eligibility_match, 
    check_housing_match
)

# Set page configuration with RTL support
st.set_page_config(
    page_title="מערכת התאמת מכרזי דיור",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for RTL support and white background with proper text colors
st.markdown("""
<style>
    .main {
        direction: rtl;
        text-align: right;
        background-color: white;
        color: #262626;
    }
    
    .stApp {
        background-color: white;
        color: #262626;
    }
    
    .css-1d391kg {
        background-color: white;
        color: #262626;
    }
    
    /* Ensure all text elements have proper dark color */
    .stApp, .main, div, p, span, label, h1, h2, h3, h4, h5, h6 {
        color: #262626 !important;
    }
    
    /* Form elements styling */
    .stSelectbox > div > div {
        direction: rtl;
        text-align: right;
        color: #262626;
    }
    
    .stSelectbox label {
        color: #262626 !important;
        font-weight: bold;
    }
    
    .stNumberInput > div > div {
        direction: rtl;
        text-align: right;
        color: #262626;
    }
    
    .stNumberInput label {
        color: #262626 !important;
        font-weight: bold;
    }
    
    /* Help text styling */
    .stTooltipIcon {
        color: #666666 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #0066cc;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #0052a3;
    }
    
    /* RTL text styling */
    .rtl-text {
        direction: rtl;
        text-align: right;
        font-family: Arial, sans-serif;
        color: #262626 !important;
    }
    
    .rtl-text h1, .rtl-text h2, .rtl-text h3, .rtl-text h4 {
        color: #1f1f1f !important;
        font-weight: bold;
    }
    
    /* Benefits box styling */
    .benefits-box {
        background-color: #f0f8ff;
        border: 1px solid #b3d9ff;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
        direction: rtl;
        text-align: right;
        color: #262626 !important;
    }
    
    .benefits-box h3 {
        color: #1f1f1f !important;
        font-weight: bold;
        margin-bottom: 15px;
    }
    
    .benefits-box p, .benefits-box li {
        color: #262626 !important;
        line-height: 1.6;
    }
    
    /* Dataframe styling */
    .dataframe {
        direction: rtl;
        color: #262626;
    }
    
    /* Results header styling */
    .results-header {
        background-color: #e6f3ff;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        direction: rtl;
        text-align: right;
        color: #1f1f1f !important;
    }
    
    .results-header h3 {
        color: #1f1f1f !important;
        font-weight: bold;
    }
    
    /* Success/Warning/Error messages */
    .stSuccess, .stWarning, .stError {
        direction: rtl;
        text-align: right;
    }
    
    /* Make sure markdown content is properly colored */
    .markdown-text-container {
        color: #262626 !important;
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
                    'אזור עדיפות': tender.get('אזור עדיפות', 'לא צוין')
                })
        
        return pd.DataFrame(matching_tenders)
        
    except Exception as e:
        st.error(f"אירעה שגיאה בעת חיפוש המכרזים: {str(e)}")
        return pd.DataFrame()

def main():
    # Title with RTL support
    st.markdown('<div class="rtl-text"><h1 style="color: #1f1f1f !important;">מילואים וזוכים - מערכת התאמה למציאת מכרזים</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="rtl-text"><h3 style="color: #1f1f1f !important;">טופס הגשת פרטים</h3></div>', unsafe_allow_html=True)

    # Create two columns for the form
    col1, col2 = st.columns(2)

    with col2:  # Right column in RTL
        st.markdown('<div class="rtl-text"><h4 style="color: #1f1f1f !important;">פרטי שירות ונכות</h4></div>', unsafe_allow_html=True)
        
        days_since_oct = st.number_input(
            "ימי מילואים מ-7.10.23",
            min_value=0,
            value=0,
            help="מספר ימי המילואים שביצעת מתאריך 7.10.23 - יש לצרף אישור על שירות של מעל 45 ימים בזמן מלחמת \"חרבות ברזל\" (טופס 3010, סעיף 1.1)",
            key="days_since_oct"
        )
        
        active_card = st.selectbox(
            "האם יש ברשותך תעודת מילואים פעיל?",
            options=["לא", "כן"],
            help="בחר 'כן' אם יש ברשותך תעודת מילואים פעיל - יש לצרף אישור או למשרת מילואים פעיל שש שנתי (סעיף 1.2) אישור למשרת מילואים פעיל שש שנתי בעבר (סעיף 1.2)",
            key="active_card"
        )
        
        days_in_6_years = st.number_input(
            "ימי מילואים ב-6 שנים האחרונות",
            min_value=0,
            value=0,
            help="סך ימי המילואים שביצעת ב-6 השנים האחרונות - יש לצרף אישור על שירות של 80 ימי מילואים בתקופה של עד 6 שנים (סעיף 1.3)",
            key="days_in_6_years"
        )
        
        disability_status = st.selectbox(
            "סיווג נכות",
            options=["אין", "נכות קשה", "100% ומעלה"],
            help="בחר את סיווג הנכות המתאים",
            key="disability_status"
        )

    with col1:  # Left column in RTL
        st.markdown('<div class="rtl-text"><h4 style="color: #1f1f1f !important;">העדפות דיור ומיקום</h4></div>', unsafe_allow_html=True)
        
        housing_status = st.selectbox(
            "האם הינך חסר/ת דיור?",
            options=["לא", "כן"],
            help="בחר 'כן' אם הינך מוגדר כחסר דיור לפי האתר הבא https://www.gov.il/he/service/certificate-of-homelessness",
            key="housing_status"
        )
        
        preferred_area = st.selectbox(
            "אזור מועדף",
            options=["דרום", "צפון", "ירושלים", "מרכז", "יהודה ושומרון"],
            help="בחר את האזור המועדף עליך למגורים",
            key="preferred_area"
        )
        
        spouse_eligible = st.selectbox(
            "האם בן/בת הזוג זכאי/ת?",
            options=["לא", "כן"],
            help="בחר 'כן' אם בן/בת הזוג זכאי/ת להטבות",
            key="spouse_eligible"
        )

    # Search button
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("חפש מכרזים מתאימים", key="search_button"):
        # Create profile data
        profile_data = {
            'ימי_מילואים_מ-7.10.23': days_since_oct,
            'תעודת_מילואים_פעיל': active_card,
            'ימי_מילואים_ב-6_שנים': days_in_6_years,
            'סיווג_נכות': disability_status if disability_status != "אין" else "",
            'חסר_דיור': housing_status,
            'אזור_מועדף': preferred_area,
            'בן/בת_זוג_זכאי': spouse_eligible
        }
        
        # Find matching tenders
        matches = find_matching_tenders(profile_data)
        
        if not matches.empty:
            st.markdown('<div class="results-header"><h3 style="color: #1f1f1f !important;">מכרזים מתאימים</h3></div>', unsafe_allow_html=True)
            
            # Display results table with RTL support
            st.markdown('<div class="rtl-text">', unsafe_allow_html=True)
            st.dataframe(
                matches,
                use_container_width=True,
                hide_index=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.success(f"נמצאו {len(matches)} מכרזים מתאימים לפרופיל שלך!")
            
        else:
            st.warning("לא נמצאו מכרזים מתאימים לפי הקריטריונים שהוזנו")

    # Benefits section
    st.markdown('<div class="benefits-box">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #1f1f1f !important;">ההטבות</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="color: #262626 !important; direction: rtl; text-align: right;">
    
    <strong>חיילי מילואים שעומדים בתנאים זכאים לשתי הטבות עיקריות:</strong><br><br>

    <strong>2.1 הטבה ראשונה</strong><br>
    הפחתה של 10% בשיעורי התשלום הקבועים באזורי עדיפות לאומית:<br><br>

    <strong>א. חייל מילואים מחוסר דיור:</strong><br>
    - אזור עדיפות לאומית א': ישלם 16% מערך הקרקע<br>
    - אזור עדיפות לאומית ב': ישלם 36% מערך הקרקע<br><br>

    <strong>ב. חייל מילואים שאינו מחוסר דיור:</strong><br>
    - אזור עדיפות לאומית א': ישלם 21% מערך הקרקע<br>
    - אזור עדיפות לאומית ב': ישלם 41% מערך הקרקע<br><br>

    <em>ההנחה מוגבלת למחירי תקרה של הקרקע. בסעיף א' עד 900,000 ₪ ובסעיף ב' עד 500,000 ₪. על הסכום שמעל התקרה שיעור התשלום הוא 91%.</em><br><br>

    <strong>2.2 הטבה שנייה</strong><br>
    חיילי המילואים זכאים להנחה נוספת בהתאם לאזור בארץ בו זכו במגרש (עד 100,000 ₪, לא כולל מע"מ):<br><br>

    - באזור עדיפות לאומית א': הנחה של 35% ממחיר המגרש לאחר חישוב הנחת האזור הראשונית<br>
    - באזור עדיפות לאומית ב': הנחה של 20% ממחיר המגרש לאחר חישוב הנחת האזור הראשונית<br>
    - באזורים שאינם אזורי עדיפות לאומית: הנחה של 10%<br><br>

    <em>בני זוג ששניהם משרתי מילואים זכאים יהנו מהנחה כפולה (70%, 40% ו-20%, בהתאמה) אשר לא תעלה על 200,000 ₪ בסה"כ.</em><br><br>

    <strong>נכי צה"ל שעומדים בתנאי הזכאות זכאים להטבות הבאות:</strong><br>
    - זכאות להשתתף במכרזים ייעודיים לנכי צה"ל<br>
    - קדימות במכרזים הרשמה והגרלה<br>
    - נכה בדרגת נכות 100%+ (מיוחדת), ישלם 31% מערך הקרקע. שיעור התשלום המופחת לערך הקרקע יחול ביחס לערך קרקע, לא כולל הוצאות פיתוח ולא כולל מע"מ, עד 2,000,000 שקלים חדשים<br><br>

    <strong>אנא עקבו אחר העדכונים במערכת לקבלת מידע נוסף</strong>
    
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 