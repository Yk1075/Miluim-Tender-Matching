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

# Simple CSS for RTL and basic styling only
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
    
    /* Custom tender card styling */
    .tender-card-container {
        background: #f0f8ff;
        border: 2px solid #1e3a8a;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(30, 58, 138, 0.1);
    }
    
    .tender-number-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .tender-number {
        font-size: 1.25rem;
        font-weight: bold;
        color: #1e3a8a;
    }
    
    .tender-address {
        font-size: 1rem;
        color: #374151;
    }
    
    .priority-stats-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .priority-badge-a {
        background: #fee2e2;
        color: #dc2626;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.875rem;
    }
    
    .priority-badge-b {
        background: #fef3c7;
        color: #d97706;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.875rem;
    }
    
    .stats-info {
        color: #6b7280;
        font-size: 0.875rem;
    }
    
    .deadline-action-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .deadline-info {
        color: #dc2626;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    .action-button {
        background: #1e3a8a;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.875rem;
        transition: background 0.2s;
    }
    
    .action-button:hover {
        background: #1e40af;
        color: white;
        text-decoration: none;
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

def render_improved_tender_card(tender):
    """Render an improved tender card with the new design"""
    # Determine priority badge
    priority_badge = ""
    priority_class = ""
    if "א'" in str(tender.get('אזור עדיפות', '')):
        priority_badge = "🎯 עדיפות א'"
        priority_class = "priority-badge-a"
    elif "ב'" in str(tender.get('אזור עדיפות', '')):
        priority_badge = "🎯 עדיפות ב'"
        priority_class = "priority-badge-b"
    else:
        priority_badge = "🎯 ללא עדיפות מיוחדת"
        priority_class = "priority-badge-b"
    
    # Stats summary
    stats_text = f"📊 {tender['מספר מגרשים']} מגרשים סה\"כ • {tender['מגרשים לחיילי מילואים']} למילואים • {tender['מגרשים לנכי צה\"ל']} לנכי צה\"ל"
    
    return f"""
    <div class="tender-card-container">
        <!-- שורה 1: מספר מכרז + כתובת מלאה -->
        <div class="tender-number-row">
            <div class="tender-number">🏆 מכרז #{tender['מספר מכרז']}</div>
            <div class="tender-address">📍 {tender['עיר']} • {tender['שכונה']} • {tender['אזור גיאוגרפי']}</div>
        </div>
        
        <!-- שורה 2: אזור עדיפות + סטטיסטיקות -->
        <div class="priority-stats-row">
            <div class="{priority_class}">{priority_badge}</div>
            <div class="stats-info">{stats_text}</div>
        </div>
        
        <!-- שורה 3: מועד הגשה + קישור המשך -->
        <div class="deadline-action-row">
            <div class="deadline-info">⏰ מועד אחרון להגשה: {tender['מועד אחרון להגשה']}</div>
            <a href="https://apps.land.gov.il/MichrazimSite/#/search" target="_blank" class="action-button">
                🔗 להגשת המכרז
            </a>
        </div>
    </div>
    """

def main():
    # Simple header using only Streamlit
    st.markdown("# 🏠 מילואים וזוכים - מערכת התאמת מכרזים")
    st.markdown("### מצא את המכרז המושלם עבורך בהתאם לפרופיל השירות והעדפותיך")
    
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
                help="מספר ימי המילואים שביצעת מתאריך 7.10.23 - יש לצרף אישור על שירות של מעל 45 ימים בזמן מלחמת \"חרבות ברזל\" (טופס 3010, סעיף 1.1)",
                key="days_since_oct"
            )
            
            active_card = st.selectbox(
                "תעודת מילואים פעיל?",
                options=["לא", "כן"],
                help="בחר 'כן' אם יש ברשותך תעודת מילואים פעיל - יש לצרף אישור למשרת מילואים פעיל שש שנתי (סעיף 1.2) או אישור למשרת מילואים פעיל שש שנתי בעבר (סעיף 1.2)",
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
                
                # Render improved tender cards
                for _, tender in st.session_state.matches.iterrows():
                    st.markdown(render_improved_tender_card(tender), unsafe_allow_html=True)
                
                st.success(f"נמצאו {len(st.session_state.matches)} מכרזים מתאימים לך!")
                st.info("🔗 **להמשך הליך ההגשה:** היכנסו לקישור הממשלתי המצורף בכל כרטיסיה ועקבו אחר ההוראות. אנו זמינים לסייע לכם במידה ותרצו!")
                
            else:
                st.warning("😔 לא נמצאו מכרזים מתאימים")
                st.info("נסה לשנות את הקריטריונים או לבדוק שוב מאוחר יותר")
        else:
            st.info("🏠 **התחל למצוא את המכרז שלך**")
            st.write("מלא את הפרטים בטופס משמאל לקבלת מכרזים מותאמים אישית")

if __name__ == "__main__":
    main() 