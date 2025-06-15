# IDF Veterans and Reservists Housing Tender Matching System

An automated matching system that connects IDF veterans and reservists with eligible housing tenders based on predefined criteria.

## 🎯 Project Overview

This system automates the process of matching profiles of IDF veterans and reservists with housing tenders they are eligible for. Instead of manually checking each profile against each tender, the system applies three hard filters to find valid matches automatically.

### Key Features
- ✅ Automated matching based on area, eligibility, and housing requirements
- ✅ Processes 20 profiles against 70 tenders (1,400 combinations) in seconds
- ✅ High accuracy with 92.9% recall rate compared to manual matching
- ✅ Comprehensive documentation for technical and non-technical users
- ✅ Excel to CSV conversion utilities

## 📊 Results Summary

- **Generated Matches:** 63 successful matches
- **Manual Matches:** 14 matches (test set)
- **Common Matches:** 13 matches (93% agreement)
- **Precision:** 20.6%
- **Recall:** 92.9%
- **F1-Score:** 33.8%

## 🔧 Setup and Installation

### Prerequisites
- Python 3.8+
- Git

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ZacharAdn/TenderMatching.git
   cd TenderMatching
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv manual_venv
   source manual_venv/bin/activate  # On Windows: manual_venv\Scripts\activate
   ```

3. **Install required packages:**
   ```bash
   pip install pandas openpyxl numpy
   ```

## 📁 Project Structure

```
TenderMatching/
├── data/
│   ├── טבלת הפרופילים.xlsx          # Profiles Excel file
│   ├── טבלת מכרזים ניסיון שני_.xlsx   # Tenders Excel file
│   ├── טבלת התאמות_.xlsx            # Manual matching table (test set)
│   └── csv_output/
│       ├── טבלת הפרופילים.csv
│       ├── טבלת מכרזים ניסיון שני_.csv
│       ├── טבלת התאמות_.csv
│       └── generated_matches.csv    # Algorithm output
├── matching_algorithm.py           # Main matching algorithm
├── manual_venv/                   # Virtual environment
├── Matching_System_Documentation.md # Detailed documentation
└── README.md
```

## 🚀 Usage

### Step 1: Convert Excel Files to CSV
The system automatically converts Excel files to CSV format when running the matching algorithm.

### Step 2: Run the Matching Algorithm
```bash
source manual_venv/bin/activate
python matching_algorithm.py
```

### Step 3: Review Results
- Check console output for statistics and comparison results
- Open `data/csv_output/generated_matches.csv` to see all matches
- Review matches where `score_סופי = 1.0` for valid matches

## 🔍 Matching Criteria (Hard Filters)

### 1. Area Matching Filter 🗺️
- Profile's preferred area must exactly match tender's geographical area
- Areas: צפון (North), מרכז (Center), דרום (South), ירושלים (Jerusalem), יהודה ושומרון (Judea & Samaria)

### 2. Eligibility Filter 👥
**Profile Categories:**
- **IDF Veterans (נכי צהל):** Serious disability or 100%+ disability rating
- **Reservists (חיילי מילואים):** Meet any of:
  - 45+ days since October 7th, OR
  - Active reservist card, OR
  - 80+ days in past 6 years
- **Other (אחר):** Don't qualify for above categories

**Tender Eligibility:**
- נכי צהל וכוחות הביטחון (Veterans only)
- חיילי מילואים (Reservists only)
- נכי צהל וכוחות הביטחון, וחיילי מילואים (Both)
- כולם (Everyone with priority)

### 3. Housing Status Filter 🏠
- If profile needs housing (חסר דיור = כן) → Tender must require housing shortage
- If profile has housing (חסר דיור = לא) → Tender must not require housing shortage

## 📈 Output Format

The generated matching table includes:

| Column | Description |
|--------|-------------|
| profile_id | Person's ID (P001, P002, etc.) |
| tender_id | Tender's ID (m1, m2, etc.) |
| עובר_אזור | 1.0 = area match, 0.0 = no match |
| עובר_זכאות | 1.0 = eligible, 0.0 = not eligible |
| עובר_חסר_דיור | 1.0 = housing match, 0.0 = mismatch |
| score_סופי | 1.0 = valid match, 0.0 = not a match |

## 📚 Documentation

For detailed documentation including technical implementation and non-technical explanations, see:
- [Complete System Documentation](Matching_System_Documentation.md)

## 🛠️ Technical Details

### Built With
- **Python 3.8+**
- **pandas** - Data manipulation and analysis
- **openpyxl** - Excel file handling
- **numpy** - Numerical computations

### Key Functions
- `is_miluim_soldier()` - Determines reservist qualification
- `get_profile_category()` - Categorizes profiles
- `check_area_match()` - Validates area compatibility
- `check_eligibility_match()` - Validates eligibility
- `check_housing_match()` - Validates housing requirements
- `create_matching_table()` - Main matching logic
- `compare_with_manual_table()` - Performance evaluation

## 📊 Performance Metrics

The system demonstrates high recall (92.9%), meaning it successfully identifies almost all manually verified matches while discovering additional valid matches that may have been missed in manual processing.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

For questions or support, please open an issue in this repository.

---

**Note:** This system is designed specifically for matching IDF veterans and reservists with housing tenders according to Israeli housing authority criteria. 