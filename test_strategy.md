# אסטרטגיית טסטים עבור מערכת התאמת מכרזי דיור

## מבוא
מסמך זה מתאר את אסטרטגיית הטסטים המקיפה עבור מערכת התאמת מכרזי דיור למילואימניקים ונכי צה"ל. המערכת כוללת ממשק UI ב-Streamlit ואלגוריתם התאמה מתקדם.

## 1. סקירה כללית של המערכת

### רכיבי המערכת:
1. **ממשק משתמש (UI)** - `tender_ui_streamlit.py`
2. **אלגוריתם התאמה** - `create_comprehensive_matches.py` & `matching_algorithm.py`
3. **קבצי נתונים** - טבלאות במבנה CSV
4. **לוגיקת אימות** - פונקציות validation

### פונקציונליות עיקרית:
- קלט נתוני פרופיל משתמש
- בדיקת זכאות על פי קריטריונים שונים
- התאמת מכרזים על פי חוקי עסק
- הצגת תוצאות בממשק ידידותי

## 2. רמות הטסטים

### 2.1 Unit Tests (טסטי יחידה)
טסטים על פונקציות בודדות וקטנות.

#### פונקציות לטסט:
1. `is_miluim_soldier()` - בדיקת זכאות מילואים
2. `get_profile_category()` - קביעת קטגוריית פרופיל
3. `check_area_match()` - התאמת אזור גיאוגרפי
4. `check_eligibility_match()` - בדיקת זכאות למכרז
5. `check_housing_match()` - בדיקת התאמת סטטוס דיור
6. `validate_profile_data()` - אימות נתוני קלט

#### מקרי טסט עיקריים:
- ערכי קלט תקינים
- ערכי קלט לא תקינים
- ערכי גבול (boundary values)
- ערכי null/None
- מחרוזות ריקות

### 2.2 Integration Tests (טסטי אינטגרציה)
טסטים על אינטראקציה בין רכיבי המערכת.

#### תרחישי אינטגרציה:
1. **קריאת נתונים מקבצי CSV**
   - טעינת קבצי מכרזים
   - טעינת קבצי פרופילים
   - טיפול בשגיאות קבצים

2. **זרימת נתונים בין פונקציות**
   - פרופיל → קטגוריה → התאמה
   - אימות קלט → חיפוש → הצגת תוצאות

3. **ממשק Streamlit**
   - session state management
   - עדכון UI לאחר חיפוש
   - טיפול בשגיאות ב-UI

### 2.3 End-to-End Tests (טסטי קצה לקצה)
טסטים על תרחישי שימוש מלאים.

#### תרחישי משתמש עיקריים:

1. **תרחיש 1: חייל מילואים עם זכאות מלאה**
   - קלט: 60 ימי מילואים מ-7.10.23, אזור דרום
   - צפוי: מכרזים מתאימים באזור דרום
   - אימות: הצגת מכרזים עם עדיפות למילואים

2. **תרחיש 2: נכה צה"ל**
   - קלט: נכות 100%, אזור מרכז
   - צפוי: מכרזים עם עדיפות לנכי צה"ל
   - אימות: קדימות בהגרלה

3. **תרחיש 3: חסר דיור**
   - קלט: סטטוס חסר דיור, אזור צפון
   - צפוי: מכרזים המיועדים לחסרי דיור
   - אימות: סינון נכון של מכרזים

4. **תרחיש 4: לא זכאי**
   - קלט: 0 ימי מילואים, ללא נכות
   - צפוי: הודעת שגיאה מתאימה
   - אימות: אי הצגת מכרזים

### 2.4 Performance Tests (טסטי ביצועים)
טסטים על זמני תגובה וטעינת המערכת.

#### מדדי ביצועים:
1. **זמן חיפוש מכרזים** - מתחת ל-2 שניות
2. **זמן טעינת דף** - מתחת לשנייה
3. **זיכרון שגוי** - מתחת ל-100MB
4. **טעינת קבצי נתונים** - מתחת ל-500ms

### 2.5 Security Tests (טסטי אבטחה)
בדיקת אבטחת המערכת.

#### תחומי אבטחה:
1. **אימות קלט** - XSS, SQL injection
2. **גישה לקבצים** - path traversal
3. **הגנה על נתונים אישיים**
4. **session management**

## 3. טסטים ספציפיים לחוקי עסק

### 3.1 חוקי זכאות מילואים
```python
# טסט: 45 ימי מילואים מ-7.10.23
assert is_miluim_soldier(45, False, 0) == True
assert is_miluim_soldier(44, False, 0) == False

# טסט: תעודת מילואים פעיל
assert is_miluim_soldier(0, True, 0) == True

# טסט: 80 ימי מילואים ב-6 שנים
assert is_miluim_soldier(0, False, 80) == True
assert is_miluim_soldier(0, False, 79) == False
```

### 3.2 חוקי זכאות נכי צה"ל
```python
# טסט: נכות קשה
profile = {'סיווג_נכות': 'נכות קשה'}
assert get_profile_category(pd.Series(profile)) == 'נכי צהל'

# טסט: נכות 100%
profile = {'סיווג_נכות': '100% ומעלה'}
assert get_profile_category(pd.Series(profile)) == 'נכי צהל'
```

### 3.3 חוקי התאמת אזורים
```python
# טסט: התאמת אזור מדויקת
assert check_area_match('דרום', 'דרום') == True
assert check_area_match('דרום', 'צפון') == False
```

### 3.4 חוקי חסרי דיור
```python
# טסט: חסר דיור יכול להגיש למכרזי חסרי דיור
assert check_housing_match('כן', 'חסרי דיור') == True

# טסט: לא חסר דיור לא יכול להגיש למכרזי חסרי דיור
assert check_housing_match('לא', 'חסרי דיור') == False
```

## 4. מתודולוגיית הטסטים

### 4.1 Test-Driven Development (TDD)
1. כתיבת טסט כושל
2. כתיבת קוד מינימלי שעובר
3. רפקטורינג
4. חזרה על התהליך

### 4.2 Behavior-Driven Development (BDD)
שימוש בתחביר Given-When-Then:

```gherkin
Given a user with 60 miluim days from 7.10.23
When searching for tenders in South area
Then show relevant tenders with miluim priority
```

### 4.3 כלים ופריימוורקים

#### כלי טסטים:
- **pytest** - טסטי Python
- **unittest** - טסטי יחידה
- **selenium** - טסטי UI אוטומטיים
- **locust** - טסטי עומס

#### כלי בדיקת קוד:
- **black** - פורמט קוד
- **flake8** - בדיקת סגנון
- **mypy** - בדיקת סוגים
- **coverage** - כיסוי טסטים

## 5. תכנון ביצוע הטסטים

### 5.1 סביבות טסט
1. **Development** - טסטים מקומיים
2. **Staging** - טסטים מלאים
3. **Production** - smoke tests

### 5.2 לוח זמנים
- **שבוע 1**: הכנת infrastructure טסטים
- **שבוע 2**: כתיבת Unit Tests
- **שבוע 3**: Integration Tests
- **שבוע 4**: E2E Tests
- **שבוע 5**: Performance & Security Tests

### 5.3 קריטריוני הצלחה
- **כיסוי קוד**: מעל 90%
- **זמן ביצוע**: מתחת ל-5 דקות
- **יציבות**: 0% failure rate
- **תחזוקה**: תיעוד מלא

## 6. ניטור ודיווח

### 6.1 מדדי איכות
1. **Bug Detection Rate** - מספר באגים שנתגלו
2. **Test Coverage** - אחוז כיסוי הקוד
3. **Mean Time to Detect** - זמן ממוצע לגילוי בעיה
4. **Mean Time to Repair** - זמן ממוצע לתיקון

### 6.2 דוחות טסטים
- דוח יומי - תוצאות טסטים אוטומטיים
- דוח שבועי - סיכום מדדי איכות
- דוח חודשי - ניתוח מגמות

## 7. סיכונים ואסטרטגיות מיטיגציה

### 7.1 סיכונים טכניים
1. **שינויים בקבצי נתונים** - טסטים עם mock data
2. **עדכונים ב-Streamlit** - version pinning
3. **שינויים בחוקי עסק** - טסטים מודולריים

### 7.2 סיכונים עסקיים
1. **שינויים בחקיקה** - גמישות בקונפיגורציה
2. **נתונים לא מעודכנים** - אלרטים אוטומטיים
3. **עומס משתמשים** - טסטי stress

## 8. תחזוקה ועדכון

### 8.1 תחזוקה שוטפת
- הרצת טסטים יומית
- עדכון טסטים עם שינויי קוד
- ניקוי טסטים מיושנים

### 8.2 שיפורים עתידיים
- אוטומציה מלאה של CI/CD
- טסטי A/B למשוב משתמשים
- ניטור performance בזמן אמת

---

## נספחים

### נספח א': דוגמאות קוד טסט

```python
# test_matching_algorithm.py
import pytest
import pandas as pd
from create_comprehensive_matches import *

class TestMiluimEligibility:
    def test_45_days_minimum(self):
        assert is_miluim_soldier(45, False, 0) == True
        assert is_miluim_soldier(44, False, 0) == False
    
    def test_active_card(self):
        assert is_miluim_soldier(0, True, 0) == True
    
    def test_6_years_accumulation(self):
        assert is_miluim_soldier(0, False, 80) == True
        assert is_miluim_soldier(0, False, 79) == False

class TestProfileCategory:
    def test_disabled_veteran(self):
        profile = pd.Series({'סיווג_נכות': 'נכות קשה'})
        assert get_profile_category(profile) == 'נכי צהל'
    
    def test_miluim_soldier(self):
        profile = pd.Series({
            'ימי_מילואים_מ-7.10.23': 50,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 0,
            'סיווג_נכות': ''
        })
        assert get_profile_category(profile) == 'חיילי מילואים'

class TestAreaMatching:
    def test_exact_match(self):
        assert check_area_match('דרום', 'דרום') == True
    
    def test_no_match(self):
        assert check_area_match('דרום', 'צפון') == False

class TestEligibilityMatching:
    def test_everyone_eligible(self):
        assert check_eligibility_match('אחר', 'כולם') == True
    
    def test_miluim_specific(self):
        assert check_eligibility_match('חיילי מילואים', 'חיילי מילואים') == True
        assert check_eligibility_match('אחר', 'חיילי מילואים') == False

class TestHousingMatching:
    def test_housing_shortage_required(self):
        assert check_housing_match('כן', 'חסרי דיור') == True
        assert check_housing_match('לא', 'חסרי דיור') == False
    
    def test_no_housing_requirement(self):
        assert check_housing_match('לא', 'לא צוין') == True
        assert check_housing_match('כן', 'לא צוין') == True
```

### נספח ב': תצורת CI/CD

```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest coverage
    
    - name: Run tests
      run: |
        coverage run -m pytest
        coverage report
        coverage html
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v1
```

### נספח ג': רשימת בדיקה לפני production

- [ ] כל הטסטים עוברים
- [ ] כיסוי קוד מעל 90%
- [ ] ביצועים תקינים
- [ ] בדיקות אבטחה עברו
- [ ] תיעוד מעודכן
- [ ] backup נתונים
- [ ] תכנית rollback 