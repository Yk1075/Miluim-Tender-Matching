import pandas as pd
import numpy as np
from pathlib import Path

def is_miluim_soldier(days_since_oct, has_active_card, days_in_6_years):
    """Check if profile qualifies as miluim soldier"""
    return days_since_oct >= 45 or has_active_card or days_in_6_years >= 80

def get_profile_category(row):
    """Determine profile category based on disability and miluim status"""
    disability = row['סיווג_נכות']
    
    # Check for disability categories
    if disability in ['נכות קשה', '100% ומעלה']:
        return 'נכי צהל'
    
    # Check for miluim soldier status
    days_since_oct = row['ימי_מילואים_מ-7.10.23']
    has_active_card = row['תעודת_מילואים_פעיל'] == 'כן'
    days_in_6_years = row['ימי_מילואים_ב-6_שנים']
    
    if is_miluim_soldier(days_since_oct, has_active_card, days_in_6_years):
        return 'חיילי מילואים'
    
    return 'אחר'

def check_area_match(profile_area, tender_area):
    """Check if profile preferred area matches tender geographical area"""
    return profile_area == tender_area

def check_eligibility_match(profile_category, tender_eligibility):
    """Check if profile category is eligible for tender"""
    # Clean up the tender eligibility text
    tender_eligibility = str(tender_eligibility).strip()
    
    # Check for "כולם" (everyone)
    if 'כולם' in tender_eligibility:
        return True
    
    # Check specific categories
    if profile_category == 'נכי צהל':
        return ('נכי צה"ל' in tender_eligibility or 
                'נכי צהל' in tender_eligibility or
                'נכי צה״ל' in tender_eligibility)  # Hebrew quotation mark
    elif profile_category == 'חיילי מילואים':
        return 'חיילי מילואים' in tender_eligibility
    
    return False

def check_housing_match(profile_housing_need, tender_housing_req):
    """Check housing requirement match"""
    # Clean up the tender housing requirement text
    tender_housing_req = str(tender_housing_req).strip()
    
    # If profile needs housing (חסר דיור = כן)
    if profile_housing_need == 'כן':
        # Must require housing shortage OR not specify housing requirement
        return ('חסרי דיור' in tender_housing_req or 
                'מחוסרי דיור' in tender_housing_req or 
                'חסרי דירה' in tender_housing_req or
                'לא צוין' in tender_housing_req or
                tender_housing_req == '' or
                tender_housing_req == 'nan')
    else:
        # If profile doesn't need housing, we can ignore tenders that require housing shortage
        # But we can still match with tenders that don't require it
        return ('חסרי דיור' not in tender_housing_req and 
                'מחוסרי דיור' not in tender_housing_req and 
                'חסרי דירה' not in tender_housing_req)

def create_comprehensive_matching_table():
    """Create comprehensive matching table with detailed information"""
    # Load data
    profiles_df = pd.read_csv('data/csv_output/טבלת הפרופילים.csv')
    tenders_df = pd.read_excel('data/טבלת מכרזים יולי 25.xlsx')
    
    # Add profile categories
    profiles_df['קטגוריה'] = profiles_df.apply(get_profile_category, axis=1)
    
    successful_matches = []
    
    for _, profile in profiles_df.iterrows():
        profile_id = profile['מספר_פרופיל']
        profile_area = profile['אזור_מועדף']
        profile_category = profile['קטגוריה']
        profile_housing_need = profile['חסר_דיור']
        profile_disability = profile['סיווג_נכות']
        profile_miluim_days = profile['ימי_מילואים_מ-7.10.23']
        profile_active_card = profile['תעודת_מילואים_פעיל']
        profile_6_years_days = profile['ימי_מילואים_ב-6_שנים']
        profile_spouse_eligible = profile['בן/בת_זוג_זכאי']
        
        for _, tender in tenders_df.iterrows():
            tender_id = tender['id']
            tender_number = tender['מספר המכרז']
            tender_city = tender['עיר']
            tender_neighborhood = tender['שכונה']
            tender_area = tender['אזור גיאוגרפי ']
            tender_priority_area = tender['אזור עדיפות']
            tender_eligibility = tender['מי רשאי להגיש']
            tender_housing_req = tender['סטטוס דיור נדרש']
            tender_plots = tender['מספר מגרשים']
            tender_disability_plots = tender['כמה מגרשים בעדיפות בהגרלה לנכי צה"ל']
            tender_miluim_plots = tender['כמה מגרשים בעדיפות בהגרלה לחיילי מילואים']
            tender_publish_date = tender['תאריך פרסום חוברת']
            tender_deadline = tender['מועד אחרון להגשת הצעות']
            
            # Apply hard filters
            area_match = check_area_match(profile_area, tender_area)
            eligibility_match = check_eligibility_match(profile_category, tender_eligibility)
            housing_match = check_housing_match(profile_housing_need, tender_housing_req)
            
            # Calculate final score (all filters must pass)
            final_score = 1.0 if (area_match and eligibility_match and housing_match) else 0.0
            
            # Only add successful matches
            if final_score == 1.0:
                successful_matches.append({
                    'מספר_פרופיל': profile_id,
                    'מספר_מכרז': tender_number,
                    'עיר': tender_city,
                    'שכונה': tender_neighborhood,
                    'אזור_גיאוגרפי': tender_area,
                    'אזור_עדיפות': tender_priority_area,
                    'קטגוריית_פרופיל': profile_category,
                    'חסר_דיור': profile_housing_need,
                    'סיווג_נכות': profile_disability,
                    'ימי_מילואים_מ-7.10.23': profile_miluim_days,
                    'תעודת_מילואים_פעיל': profile_active_card,
                    'ימי_מילואים_ב-6_שנים': profile_6_years_days,
                    'בן/בת_זוג_זכאי': profile_spouse_eligible,
                    'מי_רשאי_להגיש': tender_eligibility,
                    'סטטוס_דיור_נדרש': tender_housing_req,
                    'מספר_מגרשים': tender_plots,
                    'מגרשים_לנכי_צהל': tender_disability_plots,
                    'מגרשים_לחיילי_מילואים': tender_miluim_plots,
                    'תאריך_פרסום': tender_publish_date,
                    'מועד_אחרון_להגשה': tender_deadline,
                    'עובר_אזור': 1.0 if area_match else 0.0,
                    'עובר_זכאות': 1.0 if eligibility_match else 0.0,
                    'עובר_חסר_דיור': 1.0 if housing_match else 0.0,
                    'ציון_סופי': final_score
                })
    
    return pd.DataFrame(successful_matches)

def main():
    print("Creating comprehensive matching table...")
    
    # Generate comprehensive matching table
    comprehensive_matches = create_comprehensive_matching_table()
    
    # Sort by profile ID and tender number for better organization
    comprehensive_matches = comprehensive_matches.sort_values(['מספר_פרופיל', 'מספר_מכרז'])
    
    # Save comprehensive matches
    output_path = 'data/csv_output/טבלת_התאמות_מקיפה.csv'
    comprehensive_matches.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Comprehensive matching table saved to: {output_path}")
    
    # Print summary statistics
    print(f"\n=== SUMMARY STATISTICS ===")
    print(f"Total successful matches: {len(comprehensive_matches)}")
    print(f"Unique profiles matched: {comprehensive_matches['מספר_פרופיל'].nunique()}")
    print(f"Unique tenders matched: {comprehensive_matches['מספר_מכרז'].nunique()}")
    
    # Print matches by profile
    print(f"\n=== MATCHES BY PROFILE ===")
    profile_counts = comprehensive_matches['מספר_פרופיל'].value_counts().sort_index()
    for profile, count in profile_counts.items():
        print(f"{profile}: {count} matches")
    
    # Print matches by area
    print(f"\n=== MATCHES BY AREA ===")
    area_counts = comprehensive_matches['אזור_גיאוגרפי'].value_counts()
    for area, count in area_counts.items():
        print(f"{area}: {count} matches")
    
    # Print sample of matches
    print(f"\n=== SAMPLE OF MATCHES (first 10) ===")
    print(comprehensive_matches[['מספר_פרופיל', 'מספר_מכרז', 'עיר', 'קטגוריית_פרופיל', 'חסר_דיור']].head(10).to_string(index=False))

if __name__ == "__main__":
    main() 