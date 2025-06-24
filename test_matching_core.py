#!/usr/bin/env python3
"""
טסטים עיקריים עבור מערכת התאמת מכרזי דיור
"""

import pytest
import pandas as pd
from create_comprehensive_matches import (
    is_miluim_soldier,
    get_profile_category,
    check_area_match,
    check_eligibility_match,
    check_housing_match
)


class TestMiluimEligibility:
    """טסטים לבדיקת זכאות מילואים"""
    
    def test_45_days_minimum(self):
        """מינימום 45 ימי מילואים מ-7.10.23"""
        assert is_miluim_soldier(45, False, 0) == True
        assert is_miluim_soldier(44, False, 0) == False
    
    def test_active_card(self):
        """תעודת מילואים פעיל"""
        assert is_miluim_soldier(0, True, 0) == True
        assert is_miluim_soldier(0, False, 0) == False
    
    def test_80_days_in_6_years(self):
        """80 ימי מילואים ב-6 שנים"""
        assert is_miluim_soldier(0, False, 80) == True
        assert is_miluim_soldier(0, False, 79) == False


class TestProfileCategory:
    """טסטים לקביעת קטגוריית פרופיל"""
    
    def test_disabled_veteran(self):
        """נכי צה"ל"""
        profile = pd.Series({'סיווג_נכות': 'נכות קשה'})
        assert get_profile_category(profile) == 'נכי צהל'
    
    def test_miluim_soldier(self):
        """חייל מילואים"""
        profile = pd.Series({
            'ימי_מילואים_מ-7.10.23': 50,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 0,
            'סיווג_נכות': ''
        })
        assert get_profile_category(profile) == 'חיילי מילואים'


class TestAreaMatching:
    """טסטים להתאמת אזורים"""
    
    def test_exact_match(self):
        """התאמה מדויקת"""
        assert check_area_match('דרום', 'דרום') == True
        assert check_area_match('דרום', 'צפון') == False


class TestEligibilityMatching:
    """טסטים לבדיקת זכאות"""
    
    def test_everyone_eligible(self):
        """כולם זכאים"""
        assert check_eligibility_match('אחר', 'כולם') == True
    
    def test_miluim_specific(self):
        """זכאות ספציפית למילואים"""
        assert check_eligibility_match('חיילי מילואים', 'חיילי מילואים') == True
        assert check_eligibility_match('אחר', 'חיילי מילואים') == False


class TestHousingMatching:
    """טסטים לבדיקת התאמת דיור"""
    
    def test_housing_shortage(self):
        """חסרי דיור"""
        assert check_housing_match('כן', 'חסרי דיור') == True
        assert check_housing_match('לא', 'חסרי דיור') == False
    
    def test_no_requirement(self):
        """ללא דרישת דיור"""
        assert check_housing_match('לא', 'לא צוין') == True
        assert check_housing_match('כן', 'לא צוין') == True


# הרצת הטסטים
if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 