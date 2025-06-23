import streamlit as st
import pandas as pd
from create_comprehensive_matches import create_comprehensive_matching_table, get_profile_category

def main():
    st.title("מערכת התאמת מכרזי דיור")
    st.markdown("### טופס הגשת פרטים")

    # Create two columns for form layout
    col1, col2 = st.columns(2)

    with col1:
        # Military service and disability section
        st.subheader("פרטי שירות ונכות")
        
        days_since_oct = st.number_input(
            "ימי מילואים מ-7.10.23",
            min_value=0,
            help="מספר ימי המילואים שביצעת מתאריך 7.10.23"
        )
        
        active_card = st.selectbox(
            "האם יש ברשותך תעודת מילואים פעיל?",
            options=["כן", "לא"],
            help="בחר 'כן' אם יש ברשותך תעודת מילואים פעיל"
        )
        
        days_in_6_years = st.number_input(
            "ימי מילואים ב-6 שנים האחרונות",
            min_value=0,
            help="סך ימי המילואים שביצעת ב-6 השנים האחרונות"
        )
        
        disability_status = st.selectbox(
            "סיווג נכות",
            options=["אין", "נכות קשה", "100% ומעלה"],
            help="בחר את סיווג הנכות המתאים"
        )

    with col2:
        # Housing and location preferences
        st.subheader("העדפות דיור ומיקום")
        
        housing_status = st.selectbox(
            "האם הינך חסר/ת דיור?",
            options=["כן", "לא"],
            help="בחר 'כן' אם אין בבעלותך דירה"
        )
        
        preferred_area = st.selectbox(
            "אזור מועדף",
            options=["דרום", "צפון", "ירושלים", "מרכז", "יהודה ושומרון"],
            help="בחר את האזור המועדף עליך למגורים"
        )
        
        spouse_eligible = st.selectbox(
            "האם בן/בת הזוג זכאי/ת?",
            options=["כן", "לא"],
            help="בחר 'כן' אם בן/בת הזוג זכאי/ת להטבות"
        )

    # Search button
    if st.button("חפש מכרזים מתאימים"):
        # Create a profile dictionary
        profile = {
            'ימי_מילואים_מ-7.10.23': days_since_oct,
            'תעודת_מילואים_פעיל': active_card,
            'ימי_מילואים_ב-6_שנים': days_in_6_years,
            'סיווג_נכות': disability_status if disability_status != "אין" else "",
            'חסר_דיור': housing_status,
            'אזור_מועדף': preferred_area,
            'בן/בת_זוג_זכאי': spouse_eligible,
            'מספר_פרופיל': 'TEMP_ID'  # Temporary ID for matching
        }
        
        # Convert profile to DataFrame
        profile_df = pd.DataFrame([profile])
        
        try:
            # Load existing data
            tenders_df = pd.read_csv('data/csv_output/טבלת מכרזים ניסיון שני_.csv')
            
            # Add category to profile
            profile_df['קטגוריה'] = profile_df.apply(get_profile_category, axis=1)
            
            # Display matches
            st.subheader("מכרזים מתאימים")
            
            # Get matches using the existing algorithm
            matches = create_comprehensive_matching_table()
            
            if not matches.empty:
                # Display relevant columns
                display_columns = [
                    'מספר_מכרז', 'עיר', 'שכונה', 'אזור_גיאוגרפי',
                    'מספר_מגרשים', 'מגרשים_לנכי_צהל', 'מגרשים_לחיילי_מילואים',
                    'תאריך_פרסום', 'מועד_אחרון_להגשה'
                ]
                
                st.dataframe(matches[display_columns])
                
                # Display benefits information
                st.markdown("""
                ### מידע על הטבות נוספות
                בקרוב יתווספו למערכת פרטים על הטבות נוספות הכוללות:
                * מענקים כספיים
                * הלוואות בתנאים מועדפים
                * הנחות במיסוי
                * סיוע בתהליך הרכישה
                
                אנא עקבו אחר העדכונים במערכת לקבלת מידע נוסף.
                """)
            else:
                st.warning("לא נמצאו מכרזים מתאימים לפי הקריטריונים שהוזנו")
                
        except Exception as e:
            st.error(f"אירעה שגיאה בעת חיפוש המכרזים: {str(e)}")

if __name__ == "__main__":
    # Set page configuration
    st.set_page_config(
        page_title="מערכת התאמת מכרזי דיור",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main() 