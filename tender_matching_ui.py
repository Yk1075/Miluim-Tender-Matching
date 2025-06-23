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

# Wolt-style CSS design
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Reset and base styles */
    * {
        direction: rtl;
        text-align: right;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    .main {
        background-color: #f8f9fa;
        padding: 0;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Header Banner - Wolt style */
    .wolt-header {
        background: linear-gradient(135deg, #009de0 0%, #0066cc 100%);
        color: white;
        padding: 1.5rem 2rem;
        margin: -1rem -1rem 1.5rem -1rem;
        border-radius: 0 0 16px 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        color: white !important;
    }
    
    .header-subtitle {
        font-size: 0.95rem;
        margin: 0 0 1rem 0;
        opacity: 0.9;
        color: white !important;
    }
    
    .info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .info-card {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 8px;
        backdrop-filter: blur(10px);
    }
    
    .info-card h4 {
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
        color: white !important;
    }
    
    .info-card p {
        font-size: 0.8rem;
        margin: 0;
        opacity: 0.9;
        color: white !important;
        line-height: 1.4;
    }
    
    /* Search panel - Wolt style */
    .search-panel {
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
    }
    
    .search-panel h3 {
        font-size: 1rem;
        font-weight: 600;
        color: #212529 !important;
        margin: 0 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e9ecef;
    }
    
    /* Form groups - compact spacing */
    .form-group {
        margin-bottom: 0.75rem;
    }
    
    .form-group:last-child {
        margin-bottom: 0;
    }
    
    /* Labels - Wolt style */
    .stSelectbox label, .stNumberInput label {
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: #495057 !important;
        margin-bottom: 0.25rem !important;
    }
    
    /* Form inputs - Wolt style */
    .stSelectbox > div > div, .stNumberInput > div > div > div > input {
        border: 1px solid #ced4da !important;
        border-radius: 8px !important;
        font-size: 0.85rem !important;
        padding: 0.5rem 0.75rem !important;
        background: white !important;
        transition: border-color 0.2s ease !important;
    }
    
    .stSelectbox > div > div:focus-within, .stNumberInput > div > div:focus-within {
        border-color: #009de0 !important;
        box-shadow: 0 0 0 2px rgba(0, 157, 224, 0.1) !important;
    }
    
    /* Help text styling */
    .stTooltipIcon {
        color: #6c757d !important;
        font-size: 0.75rem !important;
    }
    
    /* Button - Wolt style */
    .stButton > button {
        background: #009de0 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(0, 157, 224, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: #0088cc !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0, 157, 224, 0.4) !important;
    }
    
    /* Results area - Wolt style */
    .results-area {
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e9ecef;
        min-height: 450px;
    }
    
    .results-header {
        font-size: 1rem;
        font-weight: 600;
        color: #212529;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e9ecef;
    }
    
    /* Tender cards - Pure Wolt style */
    .tender-card {
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
        cursor: pointer;
        position: relative;
    }
    
    .tender-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        border-color: #009de0;
        transform: translateY(-2px);
    }
    
    .tender-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 0.5rem;
    }
    
    .tender-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #212529;
        margin: 0;
        line-height: 1.3;
    }
    
    .tender-number {
        font-size: 0.7rem;
        color: #6c757d;
        background: #f8f9fa;
        padding: 0.2rem 0.5rem;
        border-radius: 6px;
        font-weight: 500;
        white-space: nowrap;
    }
    
    .tender-location {
        font-size: 0.8rem;
        color: #6c757d;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .tender-stats {
        display: flex;
        gap: 0.75rem;
        margin-bottom: 0.5rem;
        flex-wrap: wrap;
    }
    
    .stat-item {
        font-size: 0.75rem;
        color: #6c757d;
        background: #f8f9fa;
        padding: 0.25rem 0.5rem;
        border-radius: 6px;
    }
    
    .stat-number {
        font-weight: 600;
        color: #009de0;
    }
    
    .tender-dates {
        font-size: 0.7rem;
        color: #6c757d;
        border-top: 1px solid #f1f3f4;
        padding-top: 0.5rem;
        line-height: 1.3;
    }
    
    .priority-badge {
        position: absolute;
        top: 0.75rem;
        left: 0.75rem;
        font-size: 0.7rem;
        padding: 0.2rem 0.5rem;
        border-radius: 6px;
        font-weight: 500;
    }
    
    .priority-a {
        background: #e3f2fd;
        color: #1976d2;
    }
    
    .priority-b {
        background: #fff3e0;
        color: #f57c00;
    }
    
    /* Empty state - Wolt style */
    .empty-state {
        text-align: center;
        padding: 2rem 1rem;
        color: #6c757d;
    }
    
    .empty-state-icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
        opacity: 0.6;
    }
    
    .empty-state h3 {
        font-size: 1rem;
        font-weight: 600;
        color: #495057 !important;
        margin-bottom: 0.5rem;
    }
    
    .empty-state p {
        font-size: 0.85rem;
        color: #6c757d !important;
        margin: 0;
    }
    
    /* Success/Warning messages - Wolt style */
    .stSuccess {
        background: #d4edda !important;
        color: #155724 !important;
        border: 1px solid #c3e6cb !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    
    .stWarning {
        background: #fff3cd !important;
        color: #856404 !important;
        border: 1px solid #ffeaa7 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    
    /* Hide Streamlit elements */
    .stDeployButton, .stDecoration, #MainMenu, footer {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .info-grid {
            grid-template-columns: 1fr;
        }
        
        .tender-stats {
            flex-direction: column;
            gap: 0.25rem;
        }
        
        .priority-badge {
            position: static;
            margin-top: 0.5rem;
            display: inline-block;
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
    """Render a single tender as a Wolt-style card"""
    priority_class = ""
    priority_text = ""
    
    if "א'" in str(tender.get('אזור עדיפות', '')):
        priority_class = "priority-a"
        priority_text = "עדיפות א'"
    elif "ב'" in str(tender.get('אזור עדיפות', '')):
        priority_class = "priority-b"
        priority_text = "עדיפות ב'"
    
    return f"""
    <div class="tender-card">
        {f'<div class="priority-badge {priority_class}">{priority_text}</div>' if priority_text else ''}
        
        <div class="tender-card-header">
            <div class="tender-title">{tender['עיר']} • {tender['שכונה']}</div>
            <div class="tender-number">#{tender['מספר מכרז']}</div>
        </div>
        
        <div class="tender-location">
            📍 {tender['אזור גיאוגרפי']}
        </div>
        
        <div class="tender-stats">
            <div class="stat-item">
                <span class="stat-number">{tender['מספר מגרשים']}</span> מגרשים
            </div>
            <div class="stat-item">
                <span class="stat-number">{tender['מגרשים לחיילי מילואים']}</span> מילואים
            </div>
            <div class="stat-item">
                <span class="stat-number">{tender['מגרשים לנכי צה"ל']}</span> נכי צה"ל
            </div>
        </div>
        
        <div class="tender-dates">
            📅 פורסם: {tender['תאריך פרסום חוברת המכרז']}<br>
            ⏰ מועד אחרון: {tender['מועד אחרון להגשה']}
        </div>
    </div>
    """

def main():
    # Wolt-style Header with system info and benefits
    st.markdown("""
    <div class="wolt-header">
        <div class="header-title">🏠 מילואים וזוכים - מערכת התאמת מכרזים</div>
        <div class="header-subtitle">מצא את המכרז המושלם עבורך בהתאם לפרופיל השירות והעדפותיך</div>
        
        <div class="info-grid">
            <div class="info-card">
                <h4>💡 איך זה עובד?</h4>
                <p>המערכת בודקת את הזכאות שלך על בסיס ימי המילואים, נכות וסטטוס דיור, ומציגה רק מכרזים רלוונטיים לפרופיל שלך</p>
            </div>
            
            <div class="info-card">
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
        st.markdown('<div class="search-panel">', unsafe_allow_html=True)
        st.markdown('<h3>📋 פרטים אישיים</h3>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        days_since_oct = st.number_input(
            "ימי מילואים מ-7.10.23",
            min_value=0,
            value=0,
            help="מספר ימי המילואים שביצעת מתאריך 7.10.23 - יש לצרף אישור על שירות של מעל 45 ימים בזמן מלחמת \"חרבות ברזל\" (טופס 3010, סעיף 1.1)",
            key="days_since_oct"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        active_card = st.selectbox(
            "תעודת מילואים פעיל?",
            options=["לא", "כן"],
            help="בחר 'כן' אם יש ברשותך תעודת מילואים פעיל - יש לצרף אישור למשרת מילואים פעיל שש שנתי (סעיף 1.2) או אישור למשרת מילואים פעיל שש שנתי בעבר (סעיף 1.2)",
            key="active_card"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        days_in_6_years = st.number_input(
            "ימי מילואים ב-6 שנים",
            min_value=0,
            value=0,
            help="סך ימי המילואים שביצעת ב-6 השנים האחרונות - יש לצרף אישור על שירות של 80 ימי מילואים בתקופה של עד 6 שנים (סעיף 1.3)",
            key="days_in_6_years"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        disability_status = st.selectbox(
            "סיווג נכות",
            options=["אין", "נכות קשה", "100% ומעלה"],
            help="בחר את סיווג הנכות המתאים לך - זה משפיע על הזכאות למכרזים מיוחדים ועל היקף ההטבות",
            key="disability_status"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        housing_status = st.selectbox(
            "חסר/ת דיור?",
            options=["לא", "כן"],
            help="בחר 'כן' אם הינך מוגדר כחסר דיור לפי האתר הממשלתי: https://www.gov.il/he/service/certificate-of-homelessness - זה משפיע על היקף ההטבות שלך",
            key="housing_status"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        preferred_area = st.selectbox(
            "אזור מועדף",
            options=["דרום", "צפון", "ירושלים", "מרכז", "יהודה ושומרון"],
            help="בחר את האזור המועדף עליך למגורים - המערכת תציג רק מכרזים באזור הנבחר",
            key="preferred_area"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        spouse_eligible = st.selectbox(
            "בן/בת זוג זכאי/ת?",
            options=["לא", "כן"],
            help="בחר 'כן' אם בן/בת הזוג זכאי/ת להטבות (גם הוא/היא מילואים או נכה) - זה יכול להכפיל את ההטבות שלכם",
            key="spouse_eligible"
        )
        st.markdown('</div>', unsafe_allow_html=True)

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
        st.markdown('<div class="results-area">', unsafe_allow_html=True)
        
        if st.session_state.search_performed:
            if not st.session_state.matches.empty:
                st.markdown('<div class="results-header">✅ מכרזים מתאימים לפרופיל שלך</div>', unsafe_allow_html=True)
                
                # Render tender cards
                for _, tender in st.session_state.matches.iterrows():
                    st.markdown(render_tender_card(tender), unsafe_allow_html=True)
                
                st.success(f"נמצאו {len(st.session_state.matches)} מכרזים מתאימים לך!")
                
            else:
                st.markdown("""
                <div class="empty-state">
                    <div class="empty-state-icon">😔</div>
                    <h3>לא נמצאו מכרזים מתאימים</h3>
                    <p>נסה לשנות את הקריטריונים או לבדוק שוב מאוחר יותר</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🏠</div>
                <h3>התחל למצוא את המכרז שלך</h3>
                <p>מלא את הפרטים בטופס משמאל לקבלת מכרזים מותאמים אישית</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 