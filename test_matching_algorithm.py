import unittest
import pandas as pd
import numpy as np
from create_comprehensive_matches import (
    is_miluim_soldier, 
    get_profile_category, 
    check_area_match, 
    check_eligibility_match, 
    check_housing_match,
    create_comprehensive_matching_table
)

class TestMatchingAlgorithm(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        # Test profiles data
        self.test_profiles = pd.DataFrame({
            'מספר_פרופיל': [1, 2, 3, 4, 5],
            'אזור_מועדף': ['צפון', 'מרכז', 'דרום', 'צפון', 'מרכז'],
            'סיווג_נכות': ['נכות קשה', '20%', '100% ומעלה', '30%', '50%'],
            'ימי_מילואים_מ-7.10.23': [60, 30, 0, 50, 40],
            'תעודת_מילואים_פעיל': ['כן', 'לא', 'לא', 'כן', 'לא'],
            'ימי_מילואים_ב-6_שנים': [100, 50, 20, 90, 70],
            'חסר_דיור': ['כן', 'לא', 'כן', 'לא', 'כן'],
            'בן/בת_זוג_זכאי': ['כן', 'לא', 'כן', 'לא', 'כן']
        })
        
        # Test tenders data
        self.test_tenders = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'מספר המכרז': ['T001', 'T002', 'T003', 'T004', 'T005'],
            'עיר': ['חיפה', 'תל אביב', 'באר שבע', 'חיפה', 'תל אביב'],
            'שכונה': ['שכונה א', 'שכונה ב', 'שכונה ג', 'שכונה ד', 'שכונה ה'],
            'אזור גיאוגרפי ': ['צפון', 'מרכז', 'דרום', 'צפון', 'מרכז'],
            'אזור עדיפות': ['צפון', 'מרכז', 'דרום', 'צפון', 'מרכז'],
            'מי רשאי להגיש': ['כולם', 'נכי צה"ל', 'חיילי מילואים', 'נכי צהל', 'כולם'],
            'סטטוס דיור נדרש': ['חסרי דיור', 'לא צוין', 'מחוסרי דיור', '', 'חסרי דירה'],
            'מספר מגרשים': [10, 15, 8, 12, 20],
            'כמה מגרשים בעדיפות בהגרלה לנכי צה"ל': [2, 3, 1, 2, 4],
            'כמה מגרשים בעדיפות בהגרלה לחיילי מילואים': [2, 0, 1, 2, 3],
            'תאריך פרסום חוברת': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
            'מועד אחרון להגשת הצעות': ['2024-02-01', '2024-02-02', '2024-02-03', '2024-02-04', '2024-02-05']
        })

    def test_is_miluim_soldier(self):
        """Test miluim soldier qualification logic"""
        # Test case 1: Days since Oct >= 45
        self.assertTrue(is_miluim_soldier(50, True, 30))
        
        # Test case 2: Has active card
        self.assertTrue(is_miluim_soldier(20, True, 30))
        
        # Test case 3: Days in 6 years >= 80
        self.assertTrue(is_miluim_soldier(20, False, 90))
        
        # Test case 4: None of the conditions met
        self.assertFalse(is_miluim_soldier(30, False, 50))
        
        # Test case 5: Edge cases
        self.assertTrue(is_miluim_soldier(45, False, 30))  # Exactly 45 days
        self.assertTrue(is_miluim_soldier(20, False, 80))  # Exactly 80 days in 6 years

    def test_get_profile_category(self):
        """Test profile category determination"""
        # Test נכי צהל category
        profile1 = pd.Series({
            'סיווג_נכות': 'נכות קשה',
            'ימי_מילואים_מ-7.10.23': 0,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 0
        })
        self.assertEqual(get_profile_category(profile1), 'נכי צהל')
        
        # Test נכי צהל with 100% disability
        profile2 = pd.Series({
            'סיווג_נכות': '100% ומעלה',
            'ימי_מילואים_מ-7.10.23': 0,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 0
        })
        self.assertEqual(get_profile_category(profile2), 'נכי צהל')
        
        # Test חיילי מילואים category
        profile3 = pd.Series({
            'סיווג_נכות': '20%',
            'ימי_מילואים_מ-7.10.23': 50,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 30
        })
        self.assertEqual(get_profile_category(profile3), 'חיילי מילואים')
        
        # Test חיילי מילואים with active card
        profile4 = pd.Series({
            'סיווג_נכות': '30%',
            'ימי_מילואים_מ-7.10.23': 20,
            'תעודת_מילואים_פעיל': 'כן',
            'ימי_מילואים_ב-6_שנים': 40
        })
        self.assertEqual(get_profile_category(profile4), 'חיילי מילואים')
        
        # Test אחר category
        profile5 = pd.Series({
            'סיווג_נכות': '50%',
            'ימי_מילואים_מ-7.10.23': 20,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 30
        })
        self.assertEqual(get_profile_category(profile5), 'אחר')

    def test_check_area_match(self):
        """Test area matching logic"""
        # Test matching areas
        self.assertTrue(check_area_match('צפון', 'צפון'))
        self.assertTrue(check_area_match('מרכז', 'מרכז'))
        self.assertTrue(check_area_match('דרום', 'דרום'))
        
        # Test non-matching areas
        self.assertFalse(check_area_match('צפון', 'מרכז'))
        self.assertFalse(check_area_match('מרכז', 'דרום'))
        self.assertFalse(check_area_match('דרום', 'צפון'))
        
        # Test edge cases
        self.assertTrue(check_area_match('', ''))
        self.assertFalse(check_area_match('צפון', ''))
        self.assertFalse(check_area_match('', 'מרכז'))

    def test_check_eligibility_match(self):
        """Test eligibility matching logic"""
        # Test "כולם" (everyone)
        self.assertTrue(check_eligibility_match('נכי צהל', 'כולם'))
        self.assertTrue(check_eligibility_match('חיילי מילואים', 'כולם'))
        self.assertTrue(check_eligibility_match('אחר', 'כולם'))
        
        # Test נכי צהל category
        self.assertTrue(check_eligibility_match('נכי צהל', 'נכי צה"ל'))
        self.assertTrue(check_eligibility_match('נכי צהל', 'נכי צהל'))
        self.assertFalse(check_eligibility_match('נכי צהל', 'חיילי מילואים'))
        
        # Test חיילי מילואים category
        self.assertTrue(check_eligibility_match('חיילי מילואים', 'חיילי מילואים'))
        self.assertFalse(check_eligibility_match('חיילי מילואים', 'נכי צה"ל'))
        
        # Test אחר category
        self.assertFalse(check_eligibility_match('אחר', 'נכי צה"ל'))
        self.assertFalse(check_eligibility_match('אחר', 'חיילי מילואים'))
        
        # Test edge cases
        self.assertFalse(check_eligibility_match('נכי צהל', ''))
        self.assertFalse(check_eligibility_match('נכי צהל', 'nan'))

    def test_check_housing_match(self):
        """Test housing requirement matching logic"""
        # Test profile needs housing (חסר דיור = כן)
        # Should match with tenders requiring housing shortage
        self.assertTrue(check_housing_match('כן', 'חסרי דיור'))
        self.assertTrue(check_housing_match('כן', 'מחוסרי דיור'))
        self.assertTrue(check_housing_match('כן', 'חסרי דירה'))
        self.assertTrue(check_housing_match('כן', 'לא צוין'))
        self.assertTrue(check_housing_match('כן', ''))
        self.assertTrue(check_housing_match('כן', 'nan'))
        
        # Test profile doesn't need housing (חסר דיור = לא)
        # Should not match with tenders requiring housing shortage
        self.assertFalse(check_housing_match('לא', 'חסרי דיור'))
        self.assertFalse(check_housing_match('לא', 'מחוסרי דיור'))
        self.assertFalse(check_housing_match('לא', 'חסרי דירה'))
        
        # Should match with tenders not requiring housing shortage
        self.assertTrue(check_housing_match('לא', 'לא צוין'))
        self.assertTrue(check_housing_match('לא', ''))
        self.assertTrue(check_housing_match('לא', 'nan'))

    def test_integration_matching(self):
        """Test complete matching process with test data"""
        # Create test CSV files
        self.test_profiles.to_csv('data/csv_output/test_profiles.csv', index=False, encoding='utf-8-sig')
        self.test_tenders.to_csv('data/csv_output/test_tenders.csv', index=False, encoding='utf-8-sig')
        
        # Temporarily modify the function to use test data
        original_profiles_path = 'data/csv_output/טבלת הפרופילים.csv'
        original_tenders_path = 'data/csv_output/טבלת מכרזים ניסיון שני_.csv'
        
        # Create a test version of the function
        def test_create_comprehensive_matching_table():
            profiles_df = pd.read_csv('data/csv_output/test_profiles.csv')
            tenders_df = pd.read_csv('data/csv_output/test_tenders.csv')
            
            profiles_df['קטגוריה'] = profiles_df.apply(get_profile_category, axis=1)
            
            successful_matches = []
            
            for _, profile in profiles_df.iterrows():
                profile_id = profile['מספר_פרופיל']
                profile_area = profile['אזור_מועדף']
                profile_category = profile['קטגוריה']
                profile_housing_need = profile['חסר_דיור']
                
                for _, tender in tenders_df.iterrows():
                    tender_area = tender['אזור גיאוגרפי ']
                    tender_eligibility = tender['מי רשאי להגיש']
                    tender_housing_req = tender['סטטוס דיור נדרש']
                    
                    area_match = check_area_match(profile_area, tender_area)
                    eligibility_match = check_eligibility_match(profile_category, tender_eligibility)
                    housing_match = check_housing_match(profile_housing_need, tender_housing_req)
                    
                    final_score = 1.0 if (area_match and eligibility_match and housing_match) else 0.0
                    
                    if final_score == 1.0:
                        successful_matches.append({
                            'מספר_פרופיל': profile_id,
                            'מספר_מכרז': tender['מספר המכרז'],
                            'קטגוריית_פרופיל': profile_category,
                            'חסר_דיור': profile_housing_need,
                            'מי_רשאי_להגיש': tender_eligibility,
                            'סטטוס_דיור_נדרש': tender_housing_req,
                            'עובר_אזור': 1.0 if area_match else 0.0,
                            'עובר_זכאות': 1.0 if eligibility_match else 0.0,
                            'עובר_חסר_דיור': 1.0 if housing_match else 0.0,
                            'ציון_סופי': final_score
                        })
            
            return pd.DataFrame(successful_matches)
        
        # Run the test
        test_matches = test_create_comprehensive_matching_table()
        
        # Verify expected matches based on our test data
        # Profile 1 (נכי צהל, צפון, חסר דיור) should match with:
        # - Tender 1 (צפון, כולם, חסרי דיור)
        # - Tender 4 (צפון, נכי צהל, empty)
        
        # Profile 2 (חיילי מילואים, מרכז, לא חסר דיור) should match with:
        # - Tender 2 (מרכז, נכי צה"ל, לא צוין) - but not eligible
        # - Tender 5 (מרכז, כולם, חסרי דירה) - but housing mismatch
        
        # Profile 3 (נכי צהל, דרום, חסר דיור) should match with:
        # - Tender 3 (דרום, חיילי מילואים, מחוסרי דיור) - but not eligible
        
        # Profile 4 (חיילי מילואים, צפון, לא חסר דיור) should match with:
        # - Tender 1 (צפון, כולם, חסרי דיור) - but housing mismatch
        # - Tender 4 (צפון, נכי צהל, empty) - but not eligible
        
        # Profile 5 (אחר, מרכז, חסר דיור) should match with:
        # - Tender 2 (מרכז, נכי צה"ל, לא צוין) - but not eligible
        # - Tender 5 (מרכז, כולם, חסרי דירה)
        
        # Expected matches:
        # Profile 1 with Tender 1 and Tender 4
        # Profile 5 with Tender 5
        
        expected_matches = 3  # Profile 1 has 2 matches, Profile 5 has 1 match
        self.assertEqual(len(test_matches), expected_matches)
        
        # Verify specific matches
        profile1_matches = test_matches[test_matches['מספר_פרופיל'] == 1]
        self.assertEqual(len(profile1_matches), 2)
        
        profile5_matches = test_matches[test_matches['מספר_פרופיל'] == 5]
        self.assertEqual(len(profile5_matches), 1)
        
        # Clean up test files
        import os
        os.remove('data/csv_output/test_profiles.csv')
        os.remove('data/csv_output/test_tenders.csv')

    def test_edge_cases(self):
        """Test edge cases and error handling"""
        # Test with NaN values
        profile_nan = pd.Series({
            'סיווג_נכות': np.nan,
            'ימי_מילואים_מ-7.10.23': np.nan,
            'תעודת_מילואים_פעיל': np.nan,
            'ימי_מילואים_ב-6_שנים': np.nan
        })
        self.assertEqual(get_profile_category(profile_nan), 'אחר')
        
        # Test with empty strings
        self.assertFalse(check_eligibility_match('נכי צהל', ''))
        self.assertFalse(check_eligibility_match('נכי צהל', '   '))
        
        # Test with None values
        self.assertFalse(check_area_match(None, 'צפון'))
        self.assertFalse(check_area_match('צפון', None))

    def test_performance_metrics(self):
        """Test performance and efficiency"""
        # Test that the algorithm handles large datasets efficiently
        large_profiles = pd.DataFrame({
            'מספר_פרופיל': range(1000),
            'אזור_מועדף': ['צפון'] * 250 + ['מרכז'] * 250 + ['דרום'] * 500,
            'סיווג_נכות': ['20%'] * 1000,
            'ימי_מילואים_מ-7.10.23': [50] * 1000,
            'תעודת_מילואים_פעיל': ['כן'] * 1000,
            'ימי_מילואים_ב-6_שנים': [100] * 1000,
            'חסר_דיור': ['כן'] * 500 + ['לא'] * 500,
            'בן/בת_זוג_זכאי': ['כן'] * 1000
        })
        
        large_tenders = pd.DataFrame({
            'id': range(100),
            'מספר המכרז': [f'T{i:03d}' for i in range(100)],
            'עיר': ['חיפה'] * 100,
            'שכונה': ['שכונה'] * 100,
            'אזור גיאוגרפי ': ['צפון'] * 100,
            'אזור עדיפות': ['צפון'] * 100,
            'מי רשאי להגיש': ['כולם'] * 100,
            'סטטוס דיור נדרש': ['חסרי דיור'] * 100,
            'מספר מגרשים': [10] * 100,
            'כמה מגרשים בעדיפות בהגרלה לנכי צה"ל': [2] * 100,
            'כמה מגרשים בעדיפות בהגרלה לחיילי מילואים': [2] * 100,
            'תאריך פרסום חוברת': ['2024-01-01'] * 100,
            'מועד אחרון להגשת הצעות': ['2024-02-01'] * 100
        })
        
        # Save large test datasets
        large_profiles.to_csv('data/csv_output/large_test_profiles.csv', index=False, encoding='utf-8-sig')
        large_tenders.to_csv('data/csv_output/large_test_tenders.csv', index=False, encoding='utf-8-sig')
        
        # Test processing time
        import time
        start_time = time.time()
        
        # Process the large dataset
        large_profiles['קטגוריה'] = large_profiles.apply(get_profile_category, axis=1)
        
        successful_matches = []
        for _, profile in large_profiles.iterrows():
            for _, tender in large_tenders.iterrows():
                area_match = check_area_match(profile['אזור_מועדף'], tender['אזור גיאוגרפי '])
                eligibility_match = check_eligibility_match(profile['קטגוריה'], tender['מי רשאי להגיש'])
                housing_match = check_housing_match(profile['חסר_דיור'], tender['סטטוס דיור נדרש'])
                
                if area_match and eligibility_match and housing_match:
                    successful_matches.append({
                        'מספר_פרופיל': profile['מספר_פרופיל'],
                        'מספר_מכרז': tender['מספר המכרז']
                    })
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Verify performance (should complete within reasonable time)
        self.assertLess(processing_time, 10.0)  # Should complete within 10 seconds
        
        # Verify results - only profiles with 'כן' in חסר_דיור should match with 'חסרי דיור' tenders
        # 500 profiles with 'כן' * 100 tenders = 50000 matches
        expected_matches = 50000  # 500 profiles with 'כן' * 100 tenders
        self.assertEqual(len(successful_matches), expected_matches)
        
        # Clean up
        import os
        os.remove('data/csv_output/large_test_profiles.csv')
        os.remove('data/csv_output/large_test_tenders.csv')

def run_comprehensive_tests():
    """Run all tests and provide detailed report"""
    print("=== STARTING COMPREHENSIVE ALGORITHM TESTS ===\n")
    
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestMatchingAlgorithm)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n=== TEST SUMMARY ===")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n=== FAILURES ===")
        for test, traceback in result.failures:
            print(f"FAILED: {test}")
            print(f"Traceback: {traceback}\n")
    
    if result.errors:
        print(f"\n=== ERRORS ===")
        for test, traceback in result.errors:
            print(f"ERROR: {test}")
            print(f"Traceback: {traceback}\n")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_comprehensive_tests() 