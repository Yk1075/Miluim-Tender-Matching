import pandas as pd
import numpy as np
from pathlib import Path

def calculate_metrics(test_set_path, generated_matches_path):
    """
    Calculate Precision, Recall, and F1-Score by comparing generated matches with test set
    
    Args:
        test_set_path: Path to the test set CSV file
        generated_matches_path: Path to the generated matches CSV file
    
    Returns:
        dict: Dictionary containing precision, recall, F1-score and detailed statistics
    """
    # Load test set and generated matches
    test_set = pd.read_csv(test_set_path, skiprows=1)  # Skip the first row
    generated_matches = pd.read_csv(generated_matches_path)
    
    # Filter only successful matches (score = 1.0)
    test_set = test_set[test_set['score_סופי'] == 1.0]
    generated_matches = generated_matches[generated_matches['score_סופי'] == 1.0]
    
    # Create sets of profile-tender pairs for comparison
    test_pairs = set(zip(test_set['profile_id'], test_set['tender_id']))
    generated_pairs = set(zip(generated_matches['profile_id'], generated_matches['tender_id']))
    
    # Calculate intersection and differences
    true_positives = test_pairs.intersection(generated_pairs)
    false_positives = generated_pairs - test_pairs
    false_negatives = test_pairs - generated_pairs
    
    # Calculate metrics
    precision = len(true_positives) / len(generated_pairs) if len(generated_pairs) > 0 else 0
    recall = len(true_positives) / len(test_pairs) if len(test_pairs) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    # Prepare detailed results
    results = {
        'metrics': {
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score
        },
        'statistics': {
            'total_test_matches': len(test_pairs),
            'total_generated_matches': len(generated_pairs),
            'true_positives': len(true_positives),
            'false_positives': len(false_positives),
            'false_negatives': len(false_negatives)
        },
        'details': {
            'correct_matches': list(true_positives),
            'extra_matches': list(false_positives),
            'missed_matches': list(false_negatives)
        }
    }
    
    return results

def analyze_mismatches(results, test_set_path, generated_matches_path):
    """
    Analyze why certain matches were missed or incorrectly generated
    
    Args:
        results: Results dictionary from calculate_metrics
        test_set_path: Path to test set CSV
        generated_matches_path: Path to generated matches CSV
    
    Returns:
        dict: Analysis of mismatches
    """
    test_set = pd.read_csv(test_set_path, skiprows=1)  # Skip the first row
    generated_matches = pd.read_csv(generated_matches_path)
    
    # Filter only successful matches
    test_set = test_set[test_set['score_סופי'] == 1.0]
    generated_matches = generated_matches[generated_matches['score_סופי'] == 1.0]
    
    analysis = {
        'missed_matches_analysis': [],
        'extra_matches_analysis': []
    }
    
    # Analyze missed matches
    for profile_id, tender_id in results['details']['missed_matches']:
        test_match = test_set[
            (test_set['profile_id'] == profile_id) & 
            (test_set['tender_id'] == tender_id)
        ].iloc[0]
        
        analysis['missed_matches_analysis'].append({
            'profile_id': profile_id,
            'tender_id': tender_id,
            'area_match': test_match['עובר_אזור'],
            'eligibility_match': test_match['עובר_זכאות'],
            'housing_match': test_match['עובר_חסר_דיור']
        })
    
    # Analyze extra matches
    for profile_id, tender_id in results['details']['extra_matches']:
        generated_match = generated_matches[
            (generated_matches['profile_id'] == profile_id) & 
            (generated_matches['tender_id'] == tender_id)
        ].iloc[0]
        
        analysis['extra_matches_analysis'].append({
            'profile_id': profile_id,
            'tender_id': tender_id,
            'area_match': generated_match['עובר_אזור'],
            'eligibility_match': generated_match['עובר_זכאות'],
            'housing_match': generated_match['עובר_חסר_דיור']
        })
    
    return analysis

def print_results(results, analysis):
    """Print detailed results and analysis"""
    print("\n=== MATCHING METRICS ===")
    print(f"Precision: {results['metrics']['precision']:.3f}")
    print(f"Recall: {results['metrics']['recall']:.3f}")
    print(f"F1-Score: {results['metrics']['f1_score']:.3f}")
    
    print("\n=== STATISTICS ===")
    print(f"Total test set matches: {results['statistics']['total_test_matches']}")
    print(f"Total generated matches: {results['statistics']['total_generated_matches']}")
    print(f"Correct matches: {results['statistics']['true_positives']}")
    print(f"Extra matches: {results['statistics']['false_positives']}")
    print(f"Missed matches: {results['statistics']['false_negatives']}")
    
    if analysis['missed_matches_analysis']:
        print("\n=== MISSED MATCHES ANALYSIS ===")
        for match in analysis['missed_matches_analysis']:
            print(f"\nProfile {match['profile_id']} -> Tender {match['tender_id']}:")
            print(f"  Area Match: {match['area_match']}")
            print(f"  Eligibility Match: {match['eligibility_match']}")
            print(f"  Housing Match: {match['housing_match']}")
    
    if analysis['extra_matches_analysis']:
        print("\n=== EXTRA MATCHES ANALYSIS ===")
        for match in analysis['extra_matches_analysis']:
            print(f"\nProfile {match['profile_id']} -> Tender {match['tender_id']}:")
            print(f"  Area Match: {match['area_match']}")
            print(f"  Eligibility Match: {match['eligibility_match']}")
            print(f"  Housing Match: {match['housing_match']}")

def main():
    # Define paths
    test_set_path = 'data/csv_output/סט בדיקות התאמה 1.csv'
    generated_matches_path = 'data/csv_output/generated_matches.csv'
    
    # Calculate metrics
    results = calculate_metrics(test_set_path, generated_matches_path)
    
    # Analyze mismatches
    analysis = analyze_mismatches(results, test_set_path, generated_matches_path)
    
    # Print results
    print_results(results, analysis)

if __name__ == "__main__":
    main() 