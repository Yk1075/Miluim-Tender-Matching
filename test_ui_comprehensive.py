#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
אסטרטגיית בדיקה מקיפה למערכת התאמת מכרזים
=====================================

קובץ זה מכיל בדיקות מקיפות לכל רכיבי המערכת:
1. בדיקות נתונים וקבצים
2. בדיקות פונקציות התאמה
3. בדיקות תרחישים שונים
4. בדיקות ממשק משתמש
5. בדיקות ביצועים
"""

import pandas as pd
import numpy as np
import os
import time
from pathlib import Path
import sys

# Import our modules
from create_comprehensive_matches import (
    is_miluim_soldier, 
    get_profile_category, 
    check_area_match, 
    check_eligibility_match, 
    check_housing_match,
    create_comprehensive_matching_table
)

class TenderMatchingTestSuite:
    """חבילת בדיקות מקיפה למערכת התאמת מכרזים"""
    
    def __init__(self):
        self.test_results = []
        self.failed_tests = []
        
    def log_test(self, test_name, passed, details=""):
        """רישום תוצאת בדיקה"""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = f"{status} | {test_name}"
        if details:
            result += f" | {details}"
        
        self.test_results.append(result)
        if not passed:
            self.failed_tests.append(test_name)
        
        print(result)
        return passed

    def test_1_data_files_exist(self):
        """בדיקה 1: קיום קבצי נתונים"""
        print("\n🔍 בדיקה 1: קיום קבצי נתונים")
        print("=" * 50)
        
        required_files = [
            'data/טבלת מכרזים יולי 25.xlsx',
            'data/csv_output/טבלת הפרופילים.csv',
            'data/csv_output/טבלת_התאמות_מקיפה.csv'
        ]
        
        all_exist = True
        for file_path in required_files:
            exists = os.path.exists(file_path)
            self.log_test(f"קובץ קיים: {file_path}", exists)
            all_exist &= exists
            
        return self.log_test("כל קבצי הנתונים קיימים", all_exist)

    def test_2_data_loading(self):
        """בדיקה 2: טעינת נתונים"""
        print("\n📊 בדיקה 2: טעינת נתונים")
        print("=" * 50)
        
        try:
            # Load profiles
            profiles_df = pd.read_csv('data/csv_output/טבלת הפרופילים.csv')
            self.log_test("טעינת טבלת פרופילים", True, f"{len(profiles_df)} פרופילים")
            
            # Load tenders
            tenders_df = pd.read_excel('data/טבלת מכרזים יולי 25.xlsx')
            self.log_test("טעינת טבלת מכרזים", True, f"{len(tenders_df)} מכרזים")
            
            # Load matches
            matches_df = pd.read_csv('data/csv_output/טבלת_התאמות_מקיפה.csv')
            self.log_test("טעינת טבלת התאמות", True, f"{len(matches_df)} התאמות")
            
            # Store for later tests
            self.profiles_df = profiles_df
            self.tenders_df = tenders_df
            self.matches_df = matches_df
            
            return True
            
        except Exception as e:
            self.log_test("טעינת נתונים", False, f"שגיאה: {str(e)}")
            return False

    def test_3_data_integrity(self):
        """בדיקה 3: תקינות נתונים"""
        print("\n🔍 בדיקה 3: תקינות נתונים")
        print("=" * 50)
        
        # Check profiles integrity
        required_profile_columns = [
            'מספר_פרופיל', 'ימי_מילואים_מ-7.10.23', 'תעודת_מילואים_פעיל',
            'ימי_מילואים_ב-6_שנים', 'סיווג_נכות', 'חסר_דיור', 'אזור_מועדף'
        ]
        
        all_columns_exist = True
        for col in required_profile_columns:
            exists = col in self.profiles_df.columns
            self.log_test(f"עמודה בפרופילים: {col}", exists)
            all_columns_exist &= exists
        
        # Check tenders integrity
        required_tender_columns = [
            'מספר המכרז', 'עיר', 'אזור גיאוגרפי ', 'מי רשאי להגיש',
            'סטטוס דיור נדרש', 'מספר מגרשים'
        ]
        
        for col in required_tender_columns:
            exists = col in self.tenders_df.columns
            self.log_test(f"עמודה במכרזים: {col}", exists)
            all_columns_exist &= exists
        
        # Check data ranges
        valid_areas = ['דרום', 'צפון', 'ירושלים', 'מרכז', 'יהודה ושומרון']
        profile_areas = self.profiles_df['אזור_מועדף'].unique()
        valid_profile_areas = all(area in valid_areas for area in profile_areas)
        self.log_test("אזורים תקינים בפרופילים", valid_profile_areas)
        
        return self.log_test("תקינות נתונים כללית", all_columns_exist and valid_profile_areas)

    def test_4_matching_functions(self):
        """בדיקה 4: פונקציות התאמה"""
        print("\n⚙️ בדיקה 4: פונקציות התאמה")
        print("=" * 50)
        
        # Test miluim soldier detection
        test_cases = [
            (50, True, 0, True),    # 50 days since Oct
            (0, False, 100, True),  # 100 days in 6 years
            (0, True, 0, True),     # Active card
            (0, False, 0, False),   # None
        ]
        
        all_passed = True
        for days_oct, active_card, days_6y, expected in test_cases:
            result = is_miluim_soldier(days_oct, active_card, days_6y)
            passed = result == expected
            self.log_test(f"זיהוי מילואימניק ({days_oct},{active_card},{days_6y})", passed, f"ציפייה: {expected}, תוצאה: {result}")
            all_passed &= passed
        
        # Test area matching
        area_tests = [
            ('דרום', 'דרום', True),
            ('צפון', 'דרום', False),
            ('מרכז', 'מרכז', True),
        ]
        
        for profile_area, tender_area, expected in area_tests:
            result = check_area_match(profile_area, tender_area)
            passed = result == expected
            self.log_test(f"התאמת אזור ({profile_area}-{tender_area})", passed)
            all_passed &= passed
        
        return self.log_test("פונקציות התאמה", all_passed)

    def test_5_realistic_scenarios(self):
        """בדיקה 5: תרחישים ריאליסטיים"""
        print("\n🎭 בדיקה 5: תרחישים ריאליסטיים")
        print("=" * 50)
        
        # Test scenario 1: Miluim soldier from South needing housing
        profile1 = {
            'ימי_מילואים_מ-7.10.23': 60,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 0,
            'סיווג_נכות': '',
            'חסר_דיור': 'כן',
            'אזור_מועדף': 'דרום',
            'בן/בת_זוג_זכאי': 'לא'
        }
        
        profile_series1 = pd.Series(profile1)
        category1 = get_profile_category(profile_series1)
        scenario1_passed = category1 == 'חיילי מילואים'
        self.log_test("תרחיש 1: מילואימניק דרום חסר דיור", scenario1_passed, f"קטגוריה: {category1}")
        
        # Test scenario 2: Disabled veteran from North
        profile2 = {
            'ימי_מילואים_מ-7.10.23': 0,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 0,
            'סיווג_נכות': 'נכות קשה',
            'חסר_דיור': 'לא',
            'אזור_מועדף': 'צפון',
            'בן/בת_זוג_זכאי': 'לא'
        }
        
        profile_series2 = pd.Series(profile2)
        category2 = get_profile_category(profile_series2)
        scenario2_passed = category2 == 'נכי צהל'
        self.log_test("תרחיש 2: נכה צפון לא חסר דיור", scenario2_passed, f"קטגוריה: {category2}")
        
        return self.log_test("תרחישים ריאליסטיים", scenario1_passed and scenario2_passed)

    def test_6_edge_cases(self):
        """בדיקה 6: מקרי קצה"""
        print("\n🔥 בדיקה 6: מקרי קצה")
        print("=" * 50)
        
        # Test empty/null values
        edge_profile = {
            'ימי_מילואים_מ-7.10.23': 0,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 0,
            'סיווג_נכות': '',
            'חסר_דיור': 'לא',
            'אזור_מועדף': 'מרכז',
            'בן/בת_זוג_זכאי': 'לא'
        }
        
        edge_series = pd.Series(edge_profile)
        edge_category = get_profile_category(edge_series)
        edge_passed = edge_category == 'אחר'
        self.log_test("מקרה קצה: פרופיל ללא זכאות", edge_passed, f"קטגוריה: {edge_category}")
        
        # Test maximum values
        max_profile = {
            'ימי_מילואים_מ-7.10.23': 500,
            'תעודת_מילואים_פעיל': 'כן',
            'ימי_מילואים_ב-6_שנים': 1000,
            'סיווג_נכות': '100% ומעלה',
            'חסר_דיור': 'כן',
            'אזור_מועדף': 'ירושלים',
            'בן/בת_זוג_זכאי': 'כן'
        }
        
        max_series = pd.Series(max_profile)
        max_category = get_profile_category(max_series)
        max_passed = max_category in ['חיילי מילואים', 'נכי צהל']
        self.log_test("מקרה קצה: פרופיל מקסימלי", max_passed, f"קטגוריה: {max_category}")
        
        return self.log_test("מקרי קצה", edge_passed and max_passed)

    def test_7_performance(self):
        """בדיקה 7: ביצועים"""
        print("\n⚡ בדיקה 7: ביצועים")
        print("=" * 50)
        
        # Test matching table creation performance
        start_time = time.time()
        try:
            test_matches = create_comprehensive_matching_table()
            creation_time = time.time() - start_time
            
            performance_passed = creation_time < 10.0  # Less than 10 seconds
            self.log_test("יצירת טבלת התאמות", performance_passed, f"זמן: {creation_time:.2f} שניות")
            
            # Test data size
            expected_matches = len(self.matches_df)
            actual_matches = len(test_matches)
            matches_consistent = abs(expected_matches - actual_matches) <= 5  # Allow small variance
            self.log_test("עקביות מספר התאמות", matches_consistent, f"צפוי: {expected_matches}, בפועל: {actual_matches}")
            
            return self.log_test("ביצועים כלליים", performance_passed and matches_consistent)
            
        except Exception as e:
            self.log_test("בדיקת ביצועים", False, f"שגיאה: {str(e)}")
            return False

    def test_8_ui_data_consistency(self):
        """בדיקה 8: עקביות נתוני UI"""
        print("\n🖥️ בדיקה 8: עקביות נתוני UI")
        print("=" * 50)
        
        try:
            # Test that UI can load the same data
            from tender_ui_streamlit import find_matching_tenders
            
            # Test with a known good profile
            test_profile = {
                'ימי_מילואים_מ-7.10.23': 60,
                'תעודת_מילואים_פעיל': 'לא',
                'ימי_מילואים_ב-6_שנים': 0,
                'סיווג_נכות': '',
                'חסר_דיור': 'כן',
                'אזור_מועדף': 'דרום',
                'בן/בת_זוג_זכאי': 'לא'
            }
            
            matches, errors = find_matching_tenders(test_profile)
            
            ui_load_passed = len(errors) == 0
            self.log_test("טעינת נתונים ב-UI", ui_load_passed, f"שגיאות: {len(errors)}")
            
            ui_matches_passed = len(matches) > 0
            self.log_test("קבלת התאמות ב-UI", ui_matches_passed, f"התאמות: {len(matches)}")
            
            return self.log_test("עקביות נתוני UI", ui_load_passed and ui_matches_passed)
            
        except Exception as e:
            self.log_test("בדיקת UI", False, f"שגיאה: {str(e)}")
            return False

    def test_9_data_statistics(self):
        """בדיקה 9: סטטיסטיקות נתונים"""
        print("\n📈 בדיקה 9: סטטיסטיקות נתונים")
        print("=" * 50)
        
        # Check expected statistics from our recent run
        expected_stats = {
            'total_matches': 71,
            'unique_profiles': 13,
            'unique_tenders': 44
        }
        
        actual_total = len(self.matches_df)
        actual_profiles = self.matches_df['מספר_פרופיל'].nunique()
        actual_tenders = self.matches_df['מספר_מכרז'].nunique()
        
        stats_passed = True
        
        total_passed = abs(actual_total - expected_stats['total_matches']) <= 5
        self.log_test("סה״כ התאמות", total_passed, f"צפוי: {expected_stats['total_matches']}, בפועל: {actual_total}")
        stats_passed &= total_passed
        
        profiles_passed = abs(actual_profiles - expected_stats['unique_profiles']) <= 3
        self.log_test("פרופילים ייחודיים", profiles_passed, f"צפוי: {expected_stats['unique_profiles']}, בפועל: {actual_profiles}")
        stats_passed &= profiles_passed
        
        tenders_passed = abs(actual_tenders - expected_stats['unique_tenders']) <= 5
        self.log_test("מכרזים ייחודיים", tenders_passed, f"צפוי: {expected_stats['unique_tenders']}, בפועל: {actual_tenders}")
        stats_passed &= tenders_passed
        
        return self.log_test("סטטיסטיקות נתונים", stats_passed)

    def run_all_tests(self):
        """הרצת כל הבדיקות"""
        print("🧪 מתחיל אסטרטגיית בדיקה מקיפה למערכת התאמת מכרזים")
        print("=" * 80)
        
        test_methods = [
            self.test_1_data_files_exist,
            self.test_2_data_loading,
            self.test_3_data_integrity,
            self.test_4_matching_functions,
            self.test_5_realistic_scenarios,
            self.test_6_edge_cases,
            self.test_7_performance,
            self.test_8_ui_data_consistency,
            self.test_9_data_statistics
        ]
        
        passed_tests = 0
        total_tests = len(test_methods)
        
        for test_method in test_methods:
            try:
                if test_method():
                    passed_tests += 1
            except Exception as e:
                self.log_test(f"שגיאה ב-{test_method.__name__}", False, str(e))
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 סיכום תוצאות הבדיקה")
        print("=" * 80)
        
        success_rate = (passed_tests / total_tests) * 100
        print(f"✅ בדיקות שעברו: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        
        if self.failed_tests:
            print(f"❌ בדיקות שנכשלו: {len(self.failed_tests)}")
            for failed_test in self.failed_tests:
                print(f"   - {failed_test}")
        
        if success_rate >= 90:
            print("\n🎉 המערכת במצב מצוין! ראויה לייצור")
        elif success_rate >= 75:
            print("\n⚠️ המערכת במצב טוב, אך דורשת תיקונים קלים")
        else:
            print("\n🚨 המערכת דורשת תיקונים משמעותיים לפני ייצור")
        
        print("\n📋 יומן מפורט:")
        for result in self.test_results:
            print(f"  {result}")
        
        return success_rate >= 90

def main():
    """הרצת חבילת הבדיקות"""
    test_suite = TenderMatchingTestSuite()
    return test_suite.run_all_tests()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 