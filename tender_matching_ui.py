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

# Clean, minimal CSS design
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset and base styles */
    * {
        direction: rtl;
        text-align: right;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    .main {
        background-color: #f8fafc;
        padding: 0;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Header */
    .header {
        background: #1e40af;
        color: white;
        padding: 1.5rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
    }
    
    .header h1 {
        font-size: 1.75rem;
        font-weight: 600;
        margin: 0;
        color: white !important;
    }
    
    .header p {
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        color: white !important;
    }
    
    /* Search panel */
    .search-panel {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border: 1px solid #e5e7eb;
    }
    
    .search-panel h3 {
        font-size: 1.125rem;
        font-weight: 600;
        color: #111827 !important;
        margin: 0 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    /* Form sections */
    .form-group {
        margin-bottom: 1rem;
    }
    
    .form-group:last-child {
        margin-bottom: 0;
    }
    
    /* Labels */
    .stSelectbox label, .stNumberInput label {
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        color: #374151 !important;
        margin-bottom: 0.25rem;
    }
    
    /* Form inputs */
    .stSelectbox > div > div, .stNumberInput > div > div > div > input {
        border: 1px solid #d1d5db !important;
        border-radius: 6px !important;
        font-size: 0.875rem !important;
        padding: 0.5rem !important;
        background: white !important;
    }
    
    .stSelectbox > div > div:focus-within, .stNumberInput > div > div:focus-within {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 1px #3b82f6 !important;
    }
    
    /* Button */
    .stButton > button {
        background: #1e40af !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        width: 100% !important;
        transition: background-color 0.2s !important;
    }
    
    .stButton > button:hover {
        background: #1d4ed8 !important;
    }
    
    /* Results area */
    .results-area {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
        min-height: 500px;
    }
    
    .results-header {
        font-size: 1.125rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    /* Tender cards - Wolt style */
    .tender-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .tender-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-color: #3b82f6;
        transform: translateY(-1px);
    }
    
    .tender-card-header {
        display: flex;
        justify-content: space-between;
        align-items: start;
        margin-bottom: 0.75rem;
    }
    
    .tender-title {
        font-size: 1rem;
        font-weight: 600;
        color: #111827;
        margin: 0;
    }
    
    .tender-number {
        font-size: 0.75rem;
        color: #6b7280;
        background: #f3f4f6;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-weight: 500;
    }
    
    .tender-location {
        font-size: 0.875rem;
        color: #374151;
        margin-bottom: 0.5rem;
    }
    
    .tender-stats {
        display: flex;
        gap: 1rem;
        margin-bottom: 0.75rem;
    }
    
    .stat-item {
        font-size: 0.75rem;
        color: #6b7280;
    }
    
    .stat-number {
        font-weight: 600;
        color: #1e40af;
    }
    
    .tender-dates {
        font-size: 0.75rem;
        color: #6b7280;
        border-top: 1px solid #f3f4f6;
        padding-top: 0.75rem;
    }
    
    .priority-badge {
        display: inline-block;
        font-size: 0.75rem;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    .priority-a {
        background: #dbeafe;
        color: #1e40af;
    }
    
    .priority-b {
        background: #fef3c7;
        color: #d97706;
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        color: #6b7280;
    }
    
    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }
    
    .empty-state h3 {
        font-size: 1.125rem;
        font-weight: 600;
        color: #374151 !important;
        margin-bottom: 0.5rem;
    }
    
    .empty-state p {
        font-size: 0.875rem;
        color: #6b7280 !important;
    }
    
    /* Success message */
    .stSuccess {
        background: #dcfce7 !important;
        color: #166534 !important;
        border: 1px solid #bbf7d0 !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }
    
    /* Warning message */
    .stWarning {
        background: #fef3c7 !important;
        color: #d97706 !important;
        border: 1px solid #fde68a !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }
    
    /* Benefits section */
    .benefits-section {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
    }
    
    .benefits-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .benefits-content {
        font-size: 0.875rem;
        line-height: 1.6;
        color: #374151;
    }
    
    .benefits-content strong {
        font-weight: 600;
        color: #111827;
    }
    
    .benefits-content em {
        font-style: italic;
        color: #6b7280;
    }
    
    /* Hide Streamlit elements */
    .stDeployButton {
        display: none;
    }
    
    .stDecoration {
        display: none;
    }
    
    #MainMenu {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
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
        priority_text = "אזור עדיפות א'"
    elif "ב'" in str(tender.get('אזור עדיפות', '')):
        priority_class = "priority-b"
        priority_text = "אזור עדיפות ב'"
    
    return f"""
    <div class="tender-card">
        <div class="tender-card-header">
            <div class="tender-title">{tender['עיר']} - {tender['שכונה']}</div>
            <div class="tender-number">מכרז {tender['מספר מכרז']}</div>
        </div>
        
        <div class="tender-location">
            📍 {tender['אזור גיאוגרפי']}
        </div>
        
        <div class="tender-stats">
            <div class="stat-item">
                <span class="stat-number">{tender['מספר מגרשים']}</span> מגרשים סה"כ
            </div>
            <div class="stat-item">
                <span class="stat-number">{tender['מגרשים לחיילי מילואים']}</span> למילואים
            </div>
            <div class="stat-item">
                <span class="stat-number">{tender['מגרשים לנכי צה"ל']}</span> לנכי צה"ל
            </div>
        </div>
        
        <div class="tender-dates">
            📅 פרסום: {tender['תאריך פרסום חוברת המכרז']} | 
            ⏰ מועד אחרון: {tender['מועד אחרון להגשה']}
        </div>
        
        {f'<div class="priority-badge {priority_class}">{priority_text}</div>' if priority_text else ''}
    </div>
    """

def main():
    # Header
    st.markdown("""
    <div class="header">
        <h1>🏠 מילואים וזוכים - מערכת התאמת מכרזים</h1>
        <p>מצא את המכרז המושלם עבורך בקלות ובמהירות</p>
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
        st.markdown('<h3>🔍 טופס חיפוש</h3>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        days_since_oct = st.number_input(
            "ימי מילואים מ-7.10.23",
            min_value=0,
            value=0,
            help="מספר ימי המילואים שביצעת מתאריך 7.10.23",
            key="days_since_oct"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        active_card = st.selectbox(
            "תעודת מילואים פעיל?",
            options=["לא", "כן"],
            help="האם יש ברשותך תעודת מילואים פעיל",
            key="active_card"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        days_in_6_years = st.number_input(
            "ימי מילואים ב-6 שנים",
            min_value=0,
            value=0,
            help="סך ימי המילואים ב-6 השנים האחרונות",
            key="days_in_6_years"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        disability_status = st.selectbox(
            "סיווג נכות",
            options=["אין", "נכות קשה", "100% ומעלה"],
            help="בחר את סיווג הנכות המתאים",
            key="disability_status"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        housing_status = st.selectbox(
            "חסר/ת דיור?",
            options=["לא", "כן"],
            help="האם הינך מוגדר כחסר דיור",
            key="housing_status"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        preferred_area = st.selectbox(
            "אזור מועדף",
            options=["דרום", "צפון", "ירושלים", "מרכז", "יהודה ושומרון"],
            help="בחר את האזור המועדף עליך למגורים",
            key="preferred_area"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        spouse_eligible = st.selectbox(
            "בן/בת זוג זכאי/ת?",
            options=["לא", "כן"],
            help="האם בן/בת הזוג זכאי/ת להטבות",
            key="spouse_eligible"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Search button
        if st.button("🔎 חפש מכרזים מתאימים", key="search_button"):
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
                st.markdown('<div class="results-header">✅ נמצאו מכרזים מתאימים</div>', unsafe_allow_html=True)
                
                # Render tender cards
                for _, tender in st.session_state.matches.iterrows():
                    st.markdown(render_tender_card(tender), unsafe_allow_html=True)
                
                st.success(f"נמצאו {len(st.session_state.matches)} מכרזים מתאימים לפרופיל שלך")
                
            else:
                st.markdown("""
                <div class="empty-state">
                    <div class="empty-state-icon">😔</div>
                    <h3>לא נמצאו מכרזים מתאימים</h3>
                    <p>נסה לשנות את הקריטריונים ולחפש שוב</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🏠</div>
                <h3>ברוכים הבאים למערכת התאמת המכרזים</h3>
                <p>מלא את הפרטים בטופס והקלק על "חפש מכרזים מתאימים"</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Benefits section
    st.markdown('<div class="benefits-section">', unsafe_allow_html=True)
    st.markdown('<div class="benefits-title">💰 מידע על ההטבות</div>', unsafe_allow_html=True)
    
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

    <em>ההנחה מוגבלת למחירי תקרה של הקרקע. בסעיף א' עד 900,000 ₪ ובסעיף ב' עד 500,000 ₪.</em><br><br>

    <strong>💎 הטבה שנייה</strong><br>
    חיילי המילואים זכאים להנחה נוספת בהתאם לאזור (עד 100,000 ₪, לא כולל מע"מ):<br><br>

    • באזור עדיפות לאומית א': הנחה של 35%<br>
    • באזור עדיפות לאומית ב': הנחה של 20%<br>
    • באזורים שאינם אזורי עדיפות לאומית: הנחה של 10%<br><br>

    <strong>🎖️ נכי צה"ל:</strong><br>
    • זכאות להשתתף במכרזים ייעודיים<br>
    • קדימות במכרזי הרשמה והגרלה<br>
    • נכה בדרגת נכות 100%+ ישלם 31% מערך הקרקע (עד 2,000,000 ש"ח)<br><br>

    <strong>📢 עקבו אחר העדכונים במערכת לקבלת מידע נוסף</strong>
    
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 