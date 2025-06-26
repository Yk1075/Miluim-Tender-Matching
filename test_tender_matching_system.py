#!/usr/bin/env python3
"""
טסטים מקיפים עבור מערכת התאמת מכרזי דיור
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import streamlit as st
from create_comprehensive_matches import (
    is_miluim_soldier,
    get_profile_category,
    check_area_match,
    check_eligibility_match,
    check_housing_match
)


class TestMiluimEligibility:
    """טסטים לבדיקת זכאות מילואים"""
    
    def test_45_days_minimum_from_oct_7(self):
        """טסט: מינימום 45 ימי מילואים מ-7.10.23"""
        assert is_miluim_soldier(45, False, 0) == True
        assert is_miluim_soldier(44, False, 0) == False
        assert is_miluim_soldier(0, False, 0) == False
    
    def test_active_miluim_card(self):
        """טסט: תעודת מילואים פעיל"""
        assert is_miluim_soldier(0, True, 0) == True
        assert is_miluim_soldier(44, True, 0) == True  # גם עם פחות מ-45 ימים
        assert is_miluim_soldier(0, False, 0) == False
    
    def test_80_days_in_6_years(self):
        """טסט: 80 ימי מילואים ב-6 שנים"""
        assert is_miluim_soldier(0, False, 80) == True
        assert is_miluim_soldier(0, False, 100) == True
        assert is_miluim_soldier(0, False, 79) == False
    
    def test_multiple_criteria(self):
        """טסט: מספר קריטריונים ביחד"""
        # כל הקריטריונים מתקיימים
        assert is_miluim_soldier(50, True, 100) == True
        # שני קריטריונים מתקיימים
        assert is_miluim_soldier(50, True, 0) == True
        assert is_miluim_soldier(50, False, 100) == True
        assert is_miluim_soldier(0, True, 100) == True
    
    def test_edge_cases(self):
        """טסט: מקרי קצה"""
        # בדיוק על הגבול
        assert is_miluim_soldier(45, False, 0) == True
        assert is_miluim_soldier(0, False, 80) == True
        # מתחת לגבול
        assert is_miluim_soldier(44, False, 79) == False
    
    def test_negative_values(self):
        """טסט: ערכים שליליים"""
        assert is_miluim_soldier(-10, False, 0) == False
        assert is_miluim_soldier(0, False, -5) == False


class TestProfileCategory:
    """טסטים לקביעת קטגוריית פרופיל"""
    
    def test_disabled_veteran_severe(self):
        """טסט: נכי צה"ל - נכות קשה"""
        profile = pd.Series({
            'סיווג_נכות': 'נכות קשה',
            'ימי_מילואים_מ-7.10.23': 0,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 0
        })
        assert get_profile_category(profile) == 'נכי צהל'
    
    def test_disabled_veteran_100_percent(self):
        """טסט: נכי צה"ל - 100% ומעלה"""
        profile = pd.Series({
            'סיווג_נכות': '100% ומעלה',
            'ימי_מילואים_מ-7.10.23': 0,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 0
        })
        assert get_profile_category(profile) == 'נכי צהל'
    
    def test_miluim_soldier_45_days(self):
        """טסט: חייל מילואים - 45 ימים מ-7.10.23"""
        profile = pd.Series({
            'סיווג_נכות': '',
            'ימי_מילואים_מ-7.10.23': 45,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 0
        })
        assert get_profile_category(profile) == 'חיילי מילואים'
    
    def test_miluim_soldier_active_card(self):
        """טסט: חייל מילואים - תעודת מילואים פעיל"""
        profile = pd.Series({
            'סיווג_נכות': '',
            'ימי_מילואים_מ-7.10.23': 0,
            'תעודת_מילואים_פעיל': 'כן',
            'ימי_מילואים_ב-6_שנים': 0
        })
        assert get_profile_category(profile) == 'חיילי מילואים'
    
    def test_miluim_soldier_80_days_6_years(self):
        """טסט: חייל מילואים - 80 ימים ב-6 שנים"""
        profile = pd.Series({
            'סיווג_נכות': '',
            'ימי_מילואים_מ-7.10.23': 0,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 80
        })
        assert get_profile_category(profile) == 'חיילי מילואים'
    
    def test_other_category(self):
        """טסט: קטגוריה 'אחר'"""
        profile = pd.Series({
            'סיווג_נכות': '',
            'ימי_מילואים_מ-7.10.23': 0,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 0
        })
        assert get_profile_category(profile) == 'אחר'
    
    def test_disabled_veteran_priority_over_miluim(self):
        """טסט: נכי צה"ל קודם לחייל מילואים"""
        # גם נכה וגם מילואים - צריך להיות נכי צה"ל
        profile = pd.Series({
            'סיווג_נכות': 'נכות קשה',
            'ימי_מילואים_מ-7.10.23': 60,
            'תעודת_מילואים_פעיל': 'כן',
            'ימי_מילואים_ב-6_שנים': 100
        })
        assert get_profile_category(profile) == 'נכי צהל'


class TestAreaMatching:
    """טסטים להתאמת אזורים גיאוגרפיים"""
    
    def test_exact_match(self):
        """טסט: התאמה מדויקת"""
        assert check_area_match('דרום', 'דרום') == True
        assert check_area_match('צפון', 'צפון') == True
        assert check_area_match('מרכז', 'מרכז') == True
        assert check_area_match('ירושלים', 'ירושלים') == True
        assert check_area_match('יהודה ושומרון', 'יהודה ושומרון') == True
    
    def test_no_match(self):
        """טסט: אי התאמה"""
        assert check_area_match('דרום', 'צפון') == False
        assert check_area_match('מרכז', 'דרום') == False
        assert check_area_match('ירושלים', 'מרכז') == False
    
    def test_case_sensitivity(self):
        """טסט: רגישות לרישיות"""
        # בהנחה שהפונקציה רגישה לרישיות
        assert check_area_match('דרום', 'דרום') == True
        # אם יש בעיה עם רווחים או רישיות - הטסט יגלה זאת
    
    def test_empty_values(self):
        """טסט: ערכים ריקים"""
        assert check_area_match('', '') == True
        assert check_area_match('דרום', '') == False
        assert check_area_match('', 'דרום') == False
    
    def test_none_values(self):
        """טסט: ערכי None"""
        assert check_area_match(None, None) == True
        assert check_area_match('דרום', None) == False
        assert check_area_match(None, 'דרום') == False


class TestEligibilityMatching:
    """טסטים לבדיקת זכאות למכרז"""
    
    def test_everyone_eligible(self):
        """טסט: כולם זכאים"""
        assert check_eligibility_match('נכי צהל', 'כולם') == True
        assert check_eligibility_match('חיילי מילואים', 'כולם') == True
        assert check_eligibility_match('אחר', 'כולם') == True
    
    def test_disabled_veterans_eligibility(self):
        """טסט: זכאות נכי צה"ל"""
        assert check_eligibility_match('נכי צהל', 'נכי צה"ל') == True
        assert check_eligibility_match('נכי צהל', 'נכי צהל') == True
        assert check_eligibility_match('חיילי מילואים', 'נכי צה"ל') == False
        assert check_eligibility_match('אחר', 'נכי צה"ל') == False
    
    def test_miluim_soldiers_eligibility(self):
        """טסט: זכאות חיילי מילואים"""
        assert check_eligibility_match('חיילי מילואים', 'חיילי מילואים') == True
        assert check_eligibility_match('נכי צהל', 'חיילי מילואים') == False
        assert check_eligibility_match('אחר', 'חיילי מילואים') == False
    
    def test_mixed_eligibility(self):
        """טסט: זכאות מעורבת"""
        # טסט עם טקסט שמכיל מספר קטגוריות
        mixed_text = 'נכי צה"ל וחיילי מילואים'
        assert check_eligibility_match('נכי צהל', mixed_text) == True
        assert check_eligibility_match('חיילי מילואים', mixed_text) == True
        assert check_eligibility_match('אחר', mixed_text) == False
    
    def test_empty_eligibility(self):
        """טסט: זכאות ריקה"""
        assert check_eligibility_match('נכי צהל', '') == False
        assert check_eligibility_match('חיילי מילואים', '') == False
        assert check_eligibility_match('אחר', '') == False
    
    def test_case_variations(self):
        """טסט: וריאציות בכתיבה"""
        # בדיקה שהפונקציה מטפלת בווריאציות שונות
        assert check_eligibility_match('נכי צהל', 'נכי צהל') == True
        assert check_eligibility_match('נכי צהל', 'נכי צה"ל') == True


class TestHousingMatching:
    """טסטים לבדיקת התאמת סטטוס דיור"""
    
    def test_housing_shortage_required_match(self):
        """טסט: התאמה למכרז הדורש חסרי דיור"""
        # חסר דיור יכול להגיש למכרז הדורש חסרי דיור
        assert check_housing_match('כן', 'חסרי דיור') == True
        assert check_housing_match('כן', 'מחוסרי דיור') == True
        assert check_housing_match('כן', 'חסרי דירה') == True
        
        # לא חסר דיור לא יכול להגיש למכרז הדורש חסרי דיור
        assert check_housing_match('לא', 'חסרי דיור') == False
        assert check_housing_match('לא', 'מחוסרי דיור') == False
        assert check_housing_match('לא', 'חסרי דירה') == False
    
    def test_no_housing_requirement(self):
        """טסט: מכרז ללא דרישת דיור"""
        # כולם יכולים להגיש למכרז ללא דרישת דיור מיוחדת
        assert check_housing_match('כן', 'לא צוין') == True
        assert check_housing_match('לא', 'לא צוין') == True
        assert check_housing_match('כן', '') == True
        assert check_housing_match('לא', '') == True
        assert check_housing_match('כן', 'nan') == True
        assert check_housing_match('לא', 'nan') == True
    
    def test_other_housing_requirements(self):
        """טסט: דרישות דיור אחרות"""
        # אם יש דרישה אחרת (לא חסרי דיור), לא חסר דיור יכול להגיש
        assert check_housing_match('לא', 'משפחות צעירות') == True
        assert check_housing_match('לא', 'זוגות נשואים') == True
        
        # חסר דיור גם יכול להגיש (אלא אם המכרז דורש במפורש שלא להיות חסר דיור)
        assert check_housing_match('כן', 'משפחות צעירות') == True
    
    def test_edge_cases(self):
        """טסט: מקרי קצה"""
        # ערכי None
        assert check_housing_match('כן', None) == True
        assert check_housing_match('לא', None) == True
        
        # ערכים ריקים
        assert check_housing_match('', 'חסרי דיור') == False
        assert check_housing_match(None, 'חסרי דיור') == False


class TestIntegration:
    """טסטי אינטגרציה לבדיקת הפעולה המשולבת"""
    
    def test_complete_profile_matching_miluim(self):
        """טסט: התאמה מלאה לחייל מילואים"""
        # פרופיל חייל מילואים טיפוסי
        profile_data = {
            'ימי_מילואים_מ-7.10.23': 60,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 0,
            'סיווג_נכות': '',
            'חסר_דיור': 'לא',
            'אזור_מועדף': 'דרום'
        }
        
        profile = pd.Series(profile_data)
        category = get_profile_category(profile)
        
        assert category == 'חיילי מילואים'
        
        # בדיקת התאמה למכרז מתאים
        assert check_area_match('דרום', 'דרום') == True
        assert check_eligibility_match(category, 'חיילי מילואים') == True
        assert check_housing_match('לא', 'לא צוין') == True
    
    def test_complete_profile_matching_disabled_veteran(self):
        """טסט: התאמה מלאה לנכה צה"ל"""
        profile_data = {
            'ימי_מילואים_מ-7.10.23': 0,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 0,
            'סיווג_נכות': 'נכות קשה',
            'חסר_דיור': 'כן',
            'אזור_מועדף': 'מרכז'
        }
        
        profile = pd.Series(profile_data)
        category = get_profile_category(profile)
        
        assert category == 'נכי צהל'
        
        # בדיקת התאמה למכרז מתאים
        assert check_area_match('מרכז', 'מרכז') == True
        assert check_eligibility_match(category, 'נכי צה"ל') == True
        assert check_housing_match('כן', 'חסרי דיור') == True
    
    def test_profile_no_eligibility(self):
        """טסט: פרופיל ללא זכאות"""
        profile_data = {
            'ימי_מילואים_מ-7.10.23': 0,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 0,
            'סיווג_נכות': '',
            'חסר_דיור': 'לא',
            'אזור_מועדף': 'צפון'
        }
        
        profile = pd.Series(profile_data)
        category = get_profile_category(profile)
        
        assert category == 'אחר'
        
        # לא יעבור בדיקת זכאות למכרזים ייעודיים
        assert check_eligibility_match(category, 'חיילי מילואים') == False
        assert check_eligibility_match(category, 'נכי צה"ל') == False
        
        # רק למכרזים פתוחים לכולם
        assert check_eligibility_match(category, 'כולם') == True


class TestDataValidation:
    """טסטים לאימות נתונים"""
    
    def test_validate_profile_data_valid(self):
        """טסט: אימות נתונים תקינים"""
        from tender_ui_streamlit import validate_profile_data
        
        valid_profile = {
            'ימי_מילואים_מ-7.10.23': 45,
            'תעודת_מילואים_פעיל': 'כן',
            'ימי_מילואים_ב-6_שנים': 100,
            'סיווג_נכות': 'נכות קשה',
            'חסר_דיור': 'כן',
            'אזור_מועדף': 'דרום',
            'בן/בת_זוג_זכאי': 'כן'
        }
        
        errors = validate_profile_data(valid_profile)
        assert len(errors) == 0
    
    def test_validate_profile_data_missing_area(self):
        """טסט: אימות נתונים - אזור חסר"""
        from tender_ui_streamlit import validate_profile_data
        
        invalid_profile = {
            'ימי_מילואים_מ-7.10.23': 45,
            'תעודת_מילואים_פעיל': 'כן',
            'ימי_מילואים_ב-6_שנים': 100,
            'סיווג_נכות': 'נכות קשה',
            'חסר_דיור': 'כן',
            'אזור_מועדף': '',  # אזור חסר
            'בן/בת_זוג_זכאי': 'כן'
        }
        
        errors = validate_profile_data(invalid_profile)
        assert len(errors) > 0
        assert any('אזור מועדף' in error for error in errors)
    
    def test_validate_profile_data_no_eligibility(self):
        """טסט: אימות נתונים - אין זכאות"""
        from tender_ui_streamlit import validate_profile_data
        
        non_eligible_profile = {
            'ימי_מילואים_מ-7.10.23': 0,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 0,
            'סיווג_נכות': 'אין',
            'חסר_דיור': 'לא',
            'אזור_מועדף': 'דרום',
            'בן/בת_זוג_זכאי': 'לא'
        }
        
        errors = validate_profile_data(non_eligible_profile)
        assert len(errors) > 0
        assert any('אינך זכאי' in error for error in errors)


class TestUIComponents:
    """טסטים לרכיבי ממשק המשתמש"""
    
    @patch('streamlit.session_state', {})
    @patch('pandas.read_csv')
    def test_find_matching_tenders_success(self, mock_read_csv):
        """טסט: חיפוש מכרזים מתאים - הצלחה"""
        from tender_ui_streamlit import find_matching_tenders
        
        # הכנת נתוני טסט
        mock_tenders_df = pd.DataFrame([
            {
                'מספר המכרז': 'T001',
                'עיר': 'תל אביב',
                'שכונה': 'רמת אביב',
                'אזור גיאוגרפי ': 'מרכז',
                'מספר מגרשים': 10,
                'כמה מגרשים בעדיפות בהגרלה לנכי צה"ל': 2,
                'כמה מגרשים בעדיפות בהגרלה לחיילי מילואים': 3,
                'תאריך פרסום חוברת': '2024-01-01',
                'מועד אחרון להגשת הצעות': '2024-02-01',
                'אזור עדיפות': 'A',
                'מי רשאי להגיש': 'חיילי מילואים',
                'סטטוס דיור נדרש': 'לא צוין'
            }
        ])
        
        mock_read_csv.return_value = mock_tenders_df
        
        profile_data = {
            'ימי_מילואים_מ-7.10.23': 60,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 0,
            'סיווג_נכות': '',
            'חסר_דיור': 'לא',
            'אזור_מועדף': 'מרכז',
            'בן/בת_זוג_זכאי': 'לא'
        }
        
        matches, errors = find_matching_tenders(profile_data)
        
        assert len(errors) == 0
        assert len(matches) == 1
        assert matches.iloc[0]['מספר מכרז'] == 'T001'
    
    @patch('pandas.read_csv')
    def test_find_matching_tenders_file_not_found(self, mock_read_csv):
        """טסט: חיפוש מכרזים - קובץ לא נמצא"""
        from tender_ui_streamlit import find_matching_tenders
        
        mock_read_csv.side_effect = FileNotFoundError("File not found")
        
        profile_data = {
            'ימי_מילואים_מ-7.10.23': 60,
            'אזור_מועדף': 'מרכז'
        }
        
        matches, errors = find_matching_tenders(profile_data)
        
        assert len(matches) == 0
        assert len(errors) > 0
        assert any('קובץ הנתונים לא נמצא' in error for error in errors)


class TestPerformance:
    """טסטי ביצועים בסיסיים"""
    
    def test_large_dataset_performance(self):
        """טסט: ביצועים עם מערך נתונים גדול"""
        import time
        
        # יצירת מערך נתונים גדול
        large_profile_data = []
        for i in range(1000):
            profile = pd.Series({
                'ימי_מילואים_מ-7.10.23': i % 100,
                'תעודת_מילואים_פעיל': 'כן' if i % 2 == 0 else 'לא',
                'ימי_מילואים_ב-6_שנים': (i % 200),
                'סיווג_נכות': 'נכות קשה' if i % 10 == 0 else ''
            })
            large_profile_data.append(profile)
        
        # מדידת זמן ביצוע
        start_time = time.time()
        
        for profile in large_profile_data:
            category = get_profile_category(profile)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # ביצועים צריכים להיות מתחת לשנייה
        assert execution_time < 1.0, f"Execution time too slow: {execution_time:.2f}s"


# הרצת הטסטים
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"]) 