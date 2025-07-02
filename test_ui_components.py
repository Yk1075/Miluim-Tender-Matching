"""
בדיקה מקיפה של רכיבי הממשק המעודכן
"""
import pandas as pd
from create_comprehensive_matches import (
    is_miluim_soldier, 
    get_profile_category, 
    check_area_match, 
    check_eligibility_match, 
    check_housing_match
)

def test_data_loading():
    """בדיקת טעינת נתונים"""
    print("🔍 בדיקת טעינת נתונים...")
    try:
        # בדיקת טעינת פרופילים
        profiles_df = pd.read_csv('data/csv_output/טבלת הפרופילים.csv')
        print(f"✅ פרופילים נטענו: {len(profiles_df)} פרופילים")
        
        # בדיקת טעינת מכרזים
        tenders_df = pd.read_excel('data/טבלת מכרזים מתוקנת .xlsx')
        print(f"✅ מכרזים נטענו: {len(tenders_df)} מכרזים")
        
        return True, profiles_df, tenders_df
        
    except Exception as e:
        print(f"❌ שגיאה בטעינת נתונים: {e}")
        return False, None, None

def test_matching_functions():
    """בדיקת פונקציות ההתאמה"""
    print("\n🔍 בדיקת פונקציות ההתאמה...")
    
    # פרופיל בדיקה
    test_profile = {
        'ימי_מילואים_מ-7.10.23': 50,
        'תעודת_מילואים_פעיל': 'כן',
        'ימי_מילואים_ב-6_שנים': 90,
        'סיווג_נכות': '',
        'חסר_דיור': 'כן',
        'אזור_מועדף': 'דרום',
        'בן/בת_זוג_זכאי': 'כן'
    }
    
    try:
        # בדיקת קטגוריה
        profile_series = pd.Series(test_profile)
        category = get_profile_category(profile_series)
        print(f"✅ קטגוריית פרופיל: {category}")
        
        # בדיקת התאמות
        area_match = check_area_match('דרום', 'דרום')
        eligibility_match = check_eligibility_match(category, 'חיילי מילואים')
        housing_match = check_housing_match('כן', 'חסרי דיור')
        
        print(f"✅ התאמת אזור: {area_match}")
        print(f"✅ התאמת זכאות: {eligibility_match}")
        print(f"✅ התאמת דיור: {housing_match}")
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה בפונקציות התאמה: {e}")
        return False

def test_end_to_end_matching():
    """בדיקת תהליך התאמה מלא"""
    print("\n🔍 בדיקת תהליך התאמה מלא...")
    
    success, profiles_df, tenders_df = test_data_loading()
    if not success:
        return False
    
    try:
        # פרופיל בדיקה
        test_profile = {
            'ימי_מילואים_מ-7.10.23': 50,
            'תעודת_מילואים_פעיל': 'כן',
            'ימי_מילואים_ב-6_שנים': 90,
            'סיווג_נכות': '',
            'חסר_דיור': 'כן',
            'אזור_מועדף': 'דרום',
            'בן/בת_זוג_זכאי': 'כן'
        }
        
        profile_series = pd.Series(test_profile)
        profile_category = get_profile_category(profile_series)
        
        matching_count = 0
        for _, tender in tenders_df.iterrows():
            area_match = check_area_match(test_profile['אזור_מועדף'], tender['אזור גיאוגרפי '])
            eligibility_match = check_eligibility_match(profile_category, tender['מי רשאי להגיש'])
            housing_match = check_housing_match(test_profile['חסר_דיור'], tender['סטטוס דיור נדרש'])
            
            if area_match and eligibility_match and housing_match:
                matching_count += 1
        
        print(f"✅ נמצאו {matching_count} התאמות מוצלחות")
        return True
        
    except Exception as e:
        print(f"❌ שגיאה בתהליך התאמה: {e}")
        return False

def test_streamlit_imports():
    """בדיקת imports של Streamlit"""
    print("\n🔍 בדיקת imports...")
    try:
        import streamlit as st
        print("✅ Streamlit נטען בהצלחה")
        
        # בדיקת pandas
        import pandas as pd
        print("✅ Pandas נטען בהצלחה")
        
        # בדיקת openpyxl
        import openpyxl
        print("✅ OpenPyXL נטען בהצלחה")
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה ב-imports: {e}")
        return False

def main():
    """הרצת כל הבדיקות"""
    print("🚀 התחלת בדיקות מערכת ההתאמות\n")
    
    tests = [
        ("בדיקת imports", test_streamlit_imports),
        ("בדיקת טעינת נתונים", lambda: test_data_loading()[0]),
        ("בדיקת פונקציות התאמה", test_matching_functions),
        ("בדיקת תהליך מלא", test_end_to_end_matching)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ שגיאה ב{test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "="*50)
    print("📊 סיכום תוצאות הבדיקות:")
    print("="*50)
    
    for test_name, result in results:
        status = "✅ עבר" if result else "❌ נכשל"
        print(f"{test_name}: {status}")
    
    success_count = sum(1 for _, result in results if result)
    total_count = len(results)
    
    print(f"\nסיכום: {success_count}/{total_count} בדיקות עברו בהצלחה")
    
    if success_count == total_count:
        print("🎉 כל הבדיקות עברו! המערכת מוכנה לשימוש")
    else:
        print("⚠️ יש בדיקות שנכשלו - יש לבדוק ולתקן")

if __name__ == "__main__":
    main() 