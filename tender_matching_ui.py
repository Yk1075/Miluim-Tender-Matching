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

# Modern CSS with professional UX/UI design
st.markdown("""
<style>
    /* Base styling */
    .main {
        direction: rtl;
        text-align: right;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
        padding: 0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 2rem 1rem;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header .subtitle {
        color: #e8f0fe !important;
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    
    /* Search panel styling */
    .search-panel {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid #e0e7ff;
        margin-bottom: 2rem;
        position: sticky;
        top: 2rem;
    }
    
    .search-panel h3 {
        color: #1e40af !important;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        text-align: center;
        border-bottom: 2px solid #e0e7ff;
        padding-bottom: 1rem;
    }
    
    .form-section {
        background: #f8fafc;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #3b82f6;
    }
    
    .form-section h4 {
        color: #1e40af !important;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Form elements styling */
    .stSelectbox label, .stNumberInput label {
        color: #374151 !important;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    .stSelectbox > div > div, .stNumberInput > div > div {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within, .stNumberInput > div > div:focus-within {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Search button styling */
    .search-button {
        margin-top: 2rem;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #3b82f6, #1d4ed8);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 700;
        font-size: 1.1rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #1d4ed8, #1e40af);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }
    
    /* Results panel styling */
    .results-panel {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid #e0e7ff;
        margin-bottom: 2rem;
        min-height: 400px;
    }
    
    .results-header {
        background: linear-gradient(45deg, #10b981, #059669);
        color: white;
        padding: 1.5rem;
        margin: -2rem -2rem 2rem -2rem;
        border-radius: 15px 15px 0 0;
        text-align: center;
    }
    
    .results-header h3 {
        color: white !important;
        font-size: 1.4rem;
        font-weight: 600;
        margin: 0;
    }
    
    .no-results {
        text-align: center;
        padding: 3rem 2rem;
        color: #6b7280;
    }
    
    .no-results .icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }
    
    .waiting-state {
        text-align: center;
        padding: 4rem 2rem;
        color: #6b7280;
    }
    
    .waiting-state .icon {
        font-size: 5rem;
        margin-bottom: 1rem;
        opacity: 0.3;
    }
    
    /* Table styling */
    .dataframe {
        direction: rtl;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Success/Warning messages */
    .stSuccess {
        background: linear-gradient(45deg, #10b981, #059669);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        font-weight: 600;
    }
    
    .stWarning {
        background: linear-gradient(45deg, #f59e0b, #d97706);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        font-weight: 600;
    }
    
    /* Benefits section styling */
    .benefits-section {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin-top: 3rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid #e0e7ff;
    }
    
    .benefits-header {
        background: linear-gradient(45deg, #8b5cf6, #7c3aed);
        color: white;
        padding: 1.5rem;
        margin: -2rem -2rem 2rem -2rem;
        border-radius: 15px 15px 0 0;
        text-align: center;
    }
    
    .benefits-header h3 {
        color: white !important;
        font-size: 1.4rem;
        font-weight: 600;
        margin: 0;
    }
    
    .benefits-content {
        color: #374151 !important;
        line-height: 1.8;
        font-size: 0.95rem;
    }
    
    .benefits-content strong {
        color: #1e40af !important;
        font-weight: 700;
    }
    
    .benefits-content em {
        color: #6b7280 !important;
        font-style: italic;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .search-panel, .results-panel, .benefits-section {
            margin: 1rem 0;
            padding: 1.5rem;
        }
    }
    
    /* RTL support */
    * {
        direction: rtl;
        text-align: right;
    }
    
    .stSelectbox, .stNumberInput {
        direction: rtl;
        text-align: right;
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
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🏠 מילואים וזוכים - מערכת התאמת מכרזים</h1>
        <div class="subtitle">מצא את המכרז המושלם עבורך בקלות ובמהירות</div>
    </div>
    """, unsafe_allow_html=True)

    # Create layout: Search panel (30%) + Results panel (70%)
    search_col, results_col = st.columns([0.3, 0.7], gap="large")

    # Initialize session state for search results
    if 'search_performed' not in st.session_state:
        st.session_state.search_performed = False
    if 'matches' not in st.session_state:
        st.session_state.matches = pd.DataFrame()

    with search_col:
        st.markdown('<div class="search-panel">', unsafe_allow_html=True)
        st.markdown('<h3>🔍 טופס חיפוש</h3>', unsafe_allow_html=True)
        
        # Service and disability section
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<h4>👨‍💼 פרטי שירות ונכות</h4>', unsafe_allow_html=True)
        
        days_since_oct = st.number_input(
            "ימי מילואים מ-7.10.23",
            min_value=0,
            value=0,
            help="מספר ימי המילואים שביצעת מתאריך 7.10.23 - יש לצרף אישור על שירות של מעל 45 ימים בזמן מלחמת \"חרבות ברזל\" (טופס 3010, סעיף 1.1)",
            key="days_since_oct"
        )
        
        active_card = st.selectbox(
            "תעודת מילואים פעיל?",
            options=["לא", "כן"],
            help="בחר 'כן' אם יש ברשותך תעודת מילואים פעיל - יש לצרף אישור או למשרת מילואים פעיל שש שנתי (סעיף 1.2) אישור למשרת מילואים פעיל שש שנתי בעבר (סעיף 1.2)",
            key="active_card"
        )
        
        days_in_6_years = st.number_input(
            "ימי מילואים ב-6 שנים",
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
        st.markdown('</div>', unsafe_allow_html=True)

        # Housing and location section
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<h4>🏡 העדפות דיור ומיקום</h4>', unsafe_allow_html=True)
        
        housing_status = st.selectbox(
            "חסר/ת דיור?",
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
            "בן/בת זוג זכאי/ת?",
            options=["לא", "כן"],
            help="בחר 'כן' אם בן/בת הזוג זכאי/ת להטבות",
            key="spouse_eligible"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Search button
        st.markdown('<div class="search-button">', unsafe_allow_html=True)
        if st.button("🔎 חפש מכרזים מתאימים", key="search_button"):
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
            
            # Find matching tenders and store in session state
            st.session_state.matches = find_matching_tenders(profile_data)
            st.session_state.search_performed = True
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with results_col:
        st.markdown('<div class="results-panel">', unsafe_allow_html=True)
        
        if st.session_state.search_performed:
            if not st.session_state.matches.empty:
                st.markdown("""
                <div class="results-header">
                    <h3>✅ מכרזים מתאימים נמצאו!</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Display results table
                st.dataframe(
                    st.session_state.matches,
                    use_container_width=True,
                    hide_index=True
                )
                
                st.success(f"🎯 נמצאו {len(st.session_state.matches)} מכרזים מתאימים לפרופיל שלך!")
                
            else:
                st.markdown("""
                <div class="no-results">
                    <div class="icon">😔</div>
                    <h3>לא נמצאו מכרזים מתאימים</h3>
                    <p>נסה לשנות את הקריטריונים ולחפש שוב</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="waiting-state">
                <div class="icon">🏠</div>
                <h3>ברוכים הבאים למערכת התאמת המכרזים</h3>
                <p>מלא את הפרטים בטופס מימין והקלק על "חפש מכרזים מתאימים"</p>
                <p>המערכת תציג כאן את כל המכרזים הרלוונטיים עבורך</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Benefits section at the bottom
    st.markdown('<div class="benefits-section">', unsafe_allow_html=True)
    st.markdown("""
    <div class="benefits-header">
        <h3>💰 מידע על ההטבות</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="benefits-content">
    
    <strong>חיילי מילואים שעומדים בתנאים זכאים לשתי הטבות עיקריות:</strong><br><br>

    <strong>🎯 הטבה ראשונה</strong><br>
    הפחתה של 10% בשיעורי התשלום הקבועים באזורי עדיפות לאומית:<br><br>

    <strong>א. חייל מילואים מחוסר דיור:</strong><br>
    • אזור עדיפות לאומית א': ישלם 16% מערך הקרקע<br>
    • אזור עדיפות לאומית ב': ישלם 36% מערך הקרקע<br><br>

    <strong>ב. חייל מילואים שאינו מחוסר דיור:</strong><br>
    • אזור עדיפות לאומית א': ישלם 21% מערך הקרקע<br>
    • אזור עדיפות לאומית ב': ישלם 41% מערך הקרקע<br><br>

    <em>ההנחה מוגבלת למחירי תקרה של הקרקע. בסעיף א' עד 900,000 ₪ ובסעיף ב' עד 500,000 ₪. על הסכום שמעל התקרה שיעור התשלום הוא 91%.</em><br><br>

    <strong>💎 הטבה שנייה</strong><br>
    חיילי המילואים זכאים להנחה נוספת בהתאם לאזור בארץ בו זכו במגרש (עד 100,000 ₪, לא כולל מע"מ):<br><br>

    • באזור עדיפות לאומית א': הנחה של 35% ממחיר המגרש לאחר חישוב הנחת האזור הראשונית<br>
    • באזור עדיפות לאומית ב': הנחה של 20% ממחיר המגרש לאחר חישוב הנחת האזור הראשונית<br>
    • באזורים שאינם אזורי עדיפות לאומית: הנחה של 10%<br><br>

    <em>בני זוג ששניהם משרתי מילואים זכאים יהנו מהנחה כפולה (70%, 40% ו-20%, בהתאמה) אשר לא תעלה על 200,000 ₪ בסה"כ.</em><br><br>

    <strong>🎖️ נכי צה"ל שעומדים בתנאי הזכאות זכאים להטבות הבאות:</strong><br>
    • זכאות להשתתף במכרזים ייעודיים לנכי צה"ל<br>
    • קדימות במכרזים הרשמה והגרלה<br>
    • נכה בדרגת נכות 100%+ (מיוחדת), ישלם 31% מערך הקרקע. שיעור התשלום המופחת לערך הקרקע יחול ביחס לערך קרקע, לא כולל הוצאות פיתוח ולא כולל מע"מ, עד 2,000,000 שקלים חדשים<br><br>

    <strong>📢 אנא עקבו אחר העדכונים במערכת לקבלת מידע נוסף</strong>
    
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 