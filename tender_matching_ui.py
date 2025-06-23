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

# Simple and clean CSS
st.markdown("""
<style>
    /* RTL and font setup */
    * {
        direction: rtl;
        text-align: right;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    .main {
        background-color: #ffffff;
        padding: 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .stApp {
        background-color: #f5f5f5;
    }
    
    /* Clean header */
    .header-section {
        background: #1e3a8a;
        color: white;
        padding: 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 12px 12px;
    }
    
    .header-title {
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 1rem;
        margin-bottom: 1.5rem;
        opacity: 0.9;
    }
    
    .info-section {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-top: 1rem;
    }
    
    .info-box {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 8px;
    }
    
    .info-box h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        font-weight: bold;
    }
    
    .info-box p {
        margin: 0;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    /* Form styling */
    .search-container {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .search-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1e3a8a;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.5rem;
    }
    
    /* Results styling */
    .results-container {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        min-height: 400px;
    }
    
    .results-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1e3a8a;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.5rem;
    }
    
    /* Tender cards */
    .tender-card {
        background: #f8f9fa;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        transition: box-shadow 0.2s;
    }
    
    .tender-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .tender-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .tender-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #1e3a8a;
    }
    
    .tender-number {
        background: #1e3a8a;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
    }
    
    .tender-info {
        color: #6b7280;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .tender-stats {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin-bottom: 0.5rem;
    }
    
    .stat {
        background: #e5e7eb;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
    }
    
    .tender-dates {
        font-size: 0.8rem;
        color: #6b7280;
        border-top: 1px solid #e5e7eb;
        padding-top: 0.5rem;
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        color: #6b7280;
    }
    
    .empty-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
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
    
    @media (max-width: 768px) {
        .info-section {
            grid-template-columns: 1fr;
        }
        
        .tender-stats {
            flex-direction: column;
            gap: 0.5rem;
        }
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

def render_tender_card(tender):
    """Render a single tender card"""
    priority_badge = ""
    if "א'" in str(tender.get('אזור עדיפות', '')):
        priority_badge = "🥇 עדיפות א'"
    elif "ב'" in str(tender.get('אזור עדיפות', '')):
        priority_badge = "🥈 עדיפות ב'"
    
    return f"""
    <div class="tender-card">
        <div class="tender-header">
            <div class="tender-title">{tender['עיר']} - {tender['שכונה']}</div>
            <div class="tender-number">#{tender['מספר מכרז']}</div>
        </div>
        
        <div class="tender-info">📍 {tender['אזור גיאוגרפי']}</div>
        
        <div class="tender-stats">
            <div class="stat">🏗️ {tender['מספר מגרשים']} מגרשים</div>
            <div class="stat">🎖️ {tender['מגרשים לחיילי מילואים']} מילואים</div>
            <div class="stat">♿ {tender['מגרשים לנכי צה"ל']} נכי צה"ל</div>
            {f'<div class="stat" style="background: #fef3c7; color: #d97706;">{priority_badge}</div>' if priority_badge else ''}
        </div>
        
        <div class="tender-dates">
            📅 פורסם: {tender['תאריך פרסום חוברת המכרז']} | ⏰ מועד אחרון: {tender['מועד אחרון להגשה']}
        </div>
    </div>
    """

def main():
    # Clean header
    st.markdown("""
    <div class="header-section">
        <div class="header-title">🏠 מילואים וזוכים - מערכת התאמת מכרזים</div>
        <div class="header-subtitle">מצא את המכרז המושלם עבורך בהתאם לפרופיל השירות והעדפותיך</div>
        
        <div class="info-section">
            <div class="info-box">
                <h4>💡 איך זה עובד?</h4>
                <p>המערכת בודקת את הזכאות שלך על בסיס ימי המילואים, נכות וסטטוס דיור, ומציגה רק מכרזים רלוונטיים לפרופיל שלך</p>
            </div>
            
            <div class="info-box">
                <h4>💰 ההטבות העיקריות</h4>
                <p>• הנחות של 10-35% באזורי עדיפות לאומית<br>
                • הנחות נוספות של 10-35% ממחיר המגרש<br>
                • קדימות בהגרלות למילואים ונכי צה"ל</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Layout: Search (30%) + Results (70%)
    search_col, results_col = st.columns([0.3, 0.7], gap="medium")

    # Initialize session state
    if 'search_performed' not in st.session_state:
        st.session_state.search_performed = False
    if 'matches' not in st.session_state:
        st.session_state.matches = pd.DataFrame()

    with search_col:
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        st.markdown('<div class="search-title">📋 פרטים אישיים</div>', unsafe_allow_html=True)
        
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
        
        st.markdown('</div>', unsafe_allow_html=True)

    with results_col:
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        
        if st.session_state.search_performed:
            if not st.session_state.matches.empty:
                st.markdown('<div class="results-title">✅ מכרזים מתאימים לפרופיל שלך</div>', unsafe_allow_html=True)
                
                # Render tender cards
                for _, tender in st.session_state.matches.iterrows():
                    st.markdown(render_tender_card(tender), unsafe_allow_html=True)
                
                st.success(f"נמצאו {len(st.session_state.matches)} מכרזים מתאימים לך!")
                
            else:
                st.markdown("""
                <div class="empty-state">
                    <div class="empty-icon">😔</div>
                    <h3>לא נמצאו מכרזים מתאימים</h3>
                    <p>נסה לשנות את הקריטריונים או לבדוק שוב מאוחר יותר</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">🏠</div>
                <h3>התחל למצוא את המכרז שלך</h3>
                <p>מלא את הפרטים בטופס משמאל לקבלת מכרזים מותאמים אישית</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 