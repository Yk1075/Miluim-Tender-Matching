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
        return 'נכי צה"ל' in tender_eligibility or 'נכי צהל' in tender_eligibility
    elif profile_category == 'חיילי מילואים':
        return 'חיילי מילואים' in tender_eligibility
    
    return False

def check_housing_match(profile_housing_need, tender_housing_req):
    """Check housing requirement match"""
    # Clean up the tender housing requirement text
    tender_housing_req = str(tender_housing_req).strip()
    
    # If profile needs housing (חסר דיור = כן)
    if profile_housing_need == 'כן':
        # Must require housing shortage
        return 'חסרי דיור' in tender_housing_req or 'מחוסרי דיור' in tender_housing_req or 'חסרי דירה' in tender_housing_req
    else:
        # If profile doesn't need housing, we can ignore tenders that require housing shortage
        # But we can still match with tenders that don't require it
        return 'חסרי דיור' not in tender_housing_req and 'מחוסרי דיור' not in tender_housing_req and 'חסרי דירה' not in tender_housing_req

def create_matching_table():
    """Create matching table based on hard filters"""
    # Load data
    profiles_df = pd.read_csv('data/csv_output/טבלת הפרופילים.csv')
    tenders_df = pd.read_csv('data/csv_output/טבלת מכרזים ניסיון שני_.csv')
    
    # Add profile categories
    profiles_df['קטגוריה'] = profiles_df.apply(get_profile_category, axis=1)
    
    matches = []
    
    for _, profile in profiles_df.iterrows():
        profile_id = profile['מספר_פרופיל']
        profile_area = profile['אזור_מועדף']
        profile_category = profile['קטגוריה']
        profile_housing_need = profile['חסר_דיור']
        
        for _, tender in tenders_df.iterrows():
            tender_id = tender['id']
            tender_area = tender['אזור גיאוגרפי ']
            tender_eligibility = tender['מי רשאי להגיש']
            tender_housing_req = tender['סטטוס דיור נדרש']
            
            # Apply hard filters
            area_match = check_area_match(profile_area, tender_area)
            eligibility_match = check_eligibility_match(profile_category, tender_eligibility)
            housing_match = check_housing_match(profile_housing_need, tender_housing_req)
            
            # Calculate final score (all filters must pass)
            final_score = 1.0 if (area_match and eligibility_match and housing_match) else 0.0
            
            # Only add matches with score > 0 or for comparison purposes
            if final_score > 0 or True:  # Keep all for comparison
                matches.append({
                    'profile_id': profile_id,
                    'tender_id': tender_id,
                    'עובר_אזור': 1.0 if area_match else 0.0,
                    'עובר_זכאות': 1.0 if eligibility_match else 0.0,
                    'עובר_חסר_דיור': 1.0 if housing_match else 0.0,
                    'score_סופי': final_score
                })
    
    return pd.DataFrame(matches)

def compare_with_manual_table(generated_df, manual_df):
    """Compare generated matching table with manual table"""
    # Filter only successful matches (score = 1.0) for comparison
    generated_matches = generated_df[generated_df['score_סופי'] == 1.0].copy()
    manual_matches = manual_df[manual_df['score_סופי'] == 1.0].copy()
    
    # Create comparison sets
    generated_pairs = set(zip(generated_matches['profile_id'], generated_matches['tender_id']))
    manual_pairs = set(zip(manual_matches['profile_id'], manual_matches['tender_id']))
    
    # Calculate metrics
    common_matches = generated_pairs.intersection(manual_pairs)
    only_generated = generated_pairs - manual_pairs
    only_manual = manual_pairs - generated_pairs
    
    precision = len(common_matches) / len(generated_pairs) if len(generated_pairs) > 0 else 0
    recall = len(common_matches) / len(manual_pairs) if len(manual_pairs) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'total_generated_matches': len(generated_pairs),
        'total_manual_matches': len(manual_pairs),
        'common_matches': len(common_matches),
        'only_in_generated': len(only_generated),
        'only_in_manual': len(only_manual),
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'common_pairs': common_matches,
        'only_generated_pairs': only_generated,
        'only_manual_pairs': only_manual
    }

def main():
    print("Creating matching table based on hard filters...")
    
    # Generate matching table
    generated_matches = create_matching_table()
    
    # Save generated matches
    output_path = 'data/csv_output/generated_matches.csv'
    generated_matches.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Generated matching table saved to: {output_path}")
    
    # Load manual matching table
    manual_matches = pd.read_csv('data/csv_output/טבלת התאמות_.csv')
    
    # Compare results
    comparison = compare_with_manual_table(generated_matches, manual_matches)
    
    print("\n=== COMPARISON RESULTS ===")
    print(f"Generated matches: {comparison['total_generated_matches']}")
    print(f"Manual matches: {comparison['total_manual_matches']}")
    print(f"Common matches: {comparison['common_matches']}")
    print(f"Only in generated: {comparison['only_in_generated']}")
    print(f"Only in manual: {comparison['only_in_manual']}")
    print(f"\nPrecision: {comparison['precision']:.3f}")
    print(f"Recall: {comparison['recall']:.3f}")
    print(f"F1-Score: {comparison['f1_score']:.3f}")
    
    if comparison['only_generated_pairs']:
        print(f"\nMatches only in generated algorithm:")
        for profile, tender in comparison['only_generated_pairs']:
            print(f"  {profile} -> {tender}")
    
    if comparison['only_manual_pairs']:
        print(f"\nMatches only in manual table:")
        for profile, tender in comparison['only_manual_pairs']:
            print(f"  {profile} -> {tender}")
    
    # Show sample of successful matches
    successful_matches = generated_matches[generated_matches['score_סופי'] == 1.0]
    print(f"\nSample of successful matches (first 10):")
    print(successful_matches.head(10).to_string(index=False))

if __name__ == "__main__":
    main() 