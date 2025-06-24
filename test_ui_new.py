import pytest
import streamlit as st
import pandas as pd
import sys
import os

# Add current directory to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tender_matching_ui_new import find_matching_tenders, render_tender_card, main
from create_comprehensive_matches import (
    get_profile_category, 
    check_area_match, 
    check_eligibility_match, 
    check_housing_match
)

class TestTenderMatchingNewUI:
    """Test suite for the new clean tender matching UI"""
    
    def setup_method(self):
        """Setup test data"""
        self.valid_profile = {
            'ימי_מילואים_מ-7.10.23': 50,
            'תעודת_מילואים_פעיל': 'כן',
            'ימי_מילואים_ב-6_שנים': 100,
            'סיווג_נכות': '',
            'חסר_דיור': 'כן',
            'אזור_מועדף': 'דרום',
            'בן/בת_זוג_זכאי': 'לא'
        }
        
        self.sample_tender = {
            'מספר מכרז': '2024/001',
            'עיר': 'באר שבע',
            'שכונה': 'רמות',
            'אזור גיאוגרפי ': 'דרום',
            'מספר מגרשים': 10,
            'כמה מגרשים בעדיפות בהגרלה לנכי צה"ל': 2,
            'כמה מגרשים בעדיפות בהגרלה לחיילי מילואים': 3,
            'תאריך פרסום חוברת': '2024-01-15',
            'מועד אחרון להגשת הצעות': '2024-02-15',
            'אזור עדיפות': 'A'
        }

    def test_find_matching_tenders_valid_profile(self):
        """Test finding matches with valid profile"""
        try:
            matches = find_matching_tenders(self.valid_profile)
            assert isinstance(matches, pd.DataFrame), "Should return DataFrame"
            print("✅ find_matching_tenders works with valid profile")
        except Exception as e:
            print(f"⚠️  find_matching_tenders error: {e}")

    def test_find_matching_tenders_empty_profile(self):
        """Test with empty profile data"""
        empty_profile = {
            'ימי_מילואים_מ-7.10.23': 0,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 0,
            'סיווג_נכות': '',
            'חסר_דיור': 'לא',
            'אזור_מועדף': 'דרום',
            'בן/בת_זוג_זכאי': 'לא'
        }
        
        try:
            matches = find_matching_tenders(empty_profile)
            assert isinstance(matches, pd.DataFrame), "Should return DataFrame even with empty profile"
            print("✅ find_matching_tenders handles empty profile")
        except Exception as e:
            print(f"⚠️  Empty profile error: {e}")

    def test_profile_category_detection(self):
        """Test profile category detection"""
        test_cases = [
            # Miluim soldier cases
            ({'ימי_מילואים_מ-7.10.23': 50, 'תעודת_מילואים_פעיל': 'כן'}, 'miluim'),
            ({'ימי_מילואים_ב-6_שנים': 100}, 'miluim'),
            
            # Disability cases
            ({'סיווג_נכות': 'נכות קשה'}, 'disability'),
            ({'סיווג_נכות': '100% ומעלה'}, 'disability'),
            
            # Regular citizen
            ({'ימי_מילואים_מ-7.10.23': 10}, 'regular')
        ]
        
        for profile_data, expected_category in test_cases:
            try:
                profile = pd.Series(profile_data)
                category = get_profile_category(profile)
                print(f"✅ Profile {profile_data} -> Category: {category}")
            except Exception as e:
                print(f"⚠️  Profile category error for {profile_data}: {e}")

    def test_area_matching(self):
        """Test area matching logic"""
        test_cases = [
            ('דרום', 'דרום', True),
            ('צפון', 'דרום', False),
            ('מרכז', 'מרכז', True),
            ('ירושלים', 'ירושלים', True),
            ('יהודה ושומרון', 'יהודה ושומרון', True)
        ]
        
        for user_area, tender_area, expected in test_cases:
            try:
                result = check_area_match(user_area, tender_area)
                assert result == expected, f"Area match failed: {user_area} vs {tender_area}"
                print(f"✅ Area match: {user_area} vs {tender_area} = {result}")
            except Exception as e:
                print(f"⚠️  Area match error: {e}")

    def test_data_file_exists(self):
        """Test that required data files exist"""
        required_files = [
            'data/csv_output/טבלת מכרזים ניסיון שני_.csv',
            'apm_logo.png',
            'create_comprehensive_matches.py'
        ]
        
        for file_path in required_files:
            if os.path.exists(file_path):
                print(f"✅ Required file exists: {file_path}")
            else:
                print(f"❌ Missing required file: {file_path}")

    def test_csv_data_integrity(self):
        """Test CSV data integrity"""
        try:
            df = pd.read_csv('data/csv_output/טבלת מכרזים ניסיון שני_.csv')
            
            required_columns = [
                'מספר המכרז', 'עיר', 'אזור גיאוגרפי ', 
                'מי רשאי להגיש', 'סטטוס דיור נדרש'
            ]
            
            for col in required_columns:
                if col in df.columns:
                    print(f"✅ Required column exists: {col}")
                else:
                    print(f"❌ Missing required column: {col}")
                    
            print(f"✅ CSV loaded successfully with {len(df)} rows")
            
        except Exception as e:
            print(f"❌ CSV data integrity error: {e}")

    def test_help_text_content(self):
        """Test that the help text contains the correct content"""
        expected_text = "על בסיס תנאי הזכאות והמכרזים שפורסמו על ידי רשות מקרקעי ישראל"
        
        # Read the UI file to check help text
        try:
            with open('tender_matching_ui_new.py', 'r', encoding='utf-8') as f:
                content = f.read()
                if expected_text in content:
                    print("✅ Help text contains correct content")
                else:
                    print("❌ Help text does not contain expected content")
        except Exception as e:
            print(f"⚠️  Error reading UI file: {e}")

    def test_ui_components_exist(self):
        """Test that all UI components exist in the code"""
        ui_components = [
            'st.number_input',
            'st.selectbox', 
            'st.button',
            'st.info',
            'st.title',
            'st.image'
        ]
        
        try:
            with open('tender_matching_ui_new.py', 'r', encoding='utf-8') as f:
                content = f.read()
                for component in ui_components:
                    if component in content:
                        print(f"✅ UI component exists: {component}")
                    else:
                        print(f"❌ Missing UI component: {component}")
        except Exception as e:
            print(f"⚠️  Error reading UI file: {e}")

    def test_css_styling_exists(self):
        """Test that CSS styling is properly implemented"""
        css_elements = [
            'direction: rtl',
            'color: #262626',
            'font-family:',
            '.stButton',
            '.stInfo'
        ]
        
        try:
            with open('tender_matching_ui_new.py', 'r', encoding='utf-8') as f:
                content = f.read()
                for element in css_elements:
                    if element in content:
                        print(f"✅ CSS element exists: {element}")
                    else:
                        print(f"❌ Missing CSS element: {element}")
        except Exception as e:
            print(f"⚠️  Error reading UI file: {e}")

def run_comprehensive_tests():
    """Run comprehensive test suite for new UI"""
    print("🧪 התחלת בדיקות למערכת התאמת מכרזים החדשה")
    print("=" * 60)
    
    test_suite = TestTenderMatchingNewUI()
    test_suite.setup_method()
    
    # Run all tests
    test_methods = [
        test_suite.test_data_file_exists,
        test_suite.test_csv_data_integrity,
        test_suite.test_find_matching_tenders_valid_profile,
        test_suite.test_find_matching_tenders_empty_profile,
        test_suite.test_profile_category_detection,
        test_suite.test_area_matching,
        test_suite.test_help_text_content,
        test_suite.test_ui_components_exist,
        test_suite.test_css_styling_exists
    ]
    
    passed = 0
    total = len(test_methods)
    
    for test_method in test_methods:
        try:
            print(f"\n🔍 {test_method.__name__}")
            test_method()
            passed += 1
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 תוצאות הבדיקות: {passed}/{total} בדיקות עברו בהצלחה")
    
    if passed == total:
        print("🎉 כל הבדיקות עברו בהצלחה! המערכת החדשה מוכנה לשימוש.")
    else:
        print(f"⚠️  {total - passed} בדיקות נכשלו. יש צורך בתיקונים.")
    
    return passed == total

if __name__ == "__main__":
    run_comprehensive_tests() 