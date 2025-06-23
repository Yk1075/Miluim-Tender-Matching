# אסטרטגיית בדיקות - מערכת התאמת מכרזי דיור

## 1. מטרות הבדיקות
- וידוא דיוק בתהליך ההתאמה בין פרופילים למכרזים
- בדיקת תקינות הממשק והחוויה למשתמש
- אימות חישובי ההטבות והזכאויות
- וידוא תאימות עם דפדפנים ומכשירים שונים

## 2. סוגי בדיקות

### 2.1 בדיקות יחידה (Unit Tests)
#### בדיקת פונקציות ההתאמה
```python
def test_is_miluim_soldier():
    # בדיקת תנאי מילואים חרבות ברזל
    assert is_miluim_soldier(days_since_oct=45, has_active_card=False, days_in_6_years=0) == True
    assert is_miluim_soldier(days_since_oct=44, has_active_card=False, days_in_6_years=0) == False
    
    # בדיקת תנאי תעודת מילואים פעיל
    assert is_miluim_soldier(days_since_oct=0, has_active_card=True, days_in_6_years=0) == True
    
    # בדיקת תנאי 80 ימי מילואים ב-6 שנים
    assert is_miluim_soldier(days_since_oct=0, has_active_card=False, days_in_6_years=80) == True
    assert is_miluim_soldier(days_since_oct=0, has_active_card=False, days_in_6_years=79) == False

def test_get_profile_category():
    # בדיקת קטגוריית נכי צה"ל
    profile_disabled = {
        'סיווג_נכות': 'נכות קשה',
        'ימי_מילואים_מ-7.10.23': 0,
        'תעודת_מילואים_פעיל': 'לא',
        'ימי_מילואים_ב-6_שנים': 0
    }
    assert get_profile_category(profile_disabled) == 'נכי צהל'
    
    # בדיקת קטגוריית חיילי מילואים
    profile_miluim = {
        'סיווג_נכות': '',
        'ימי_מילואים_מ-7.10.23': 45,
        'תעודת_מילואים_פעיל': 'לא',
        'ימי_מילואים_ב-6_שנים': 0
    }
    assert get_profile_category(profile_miluim) == 'חיילי מילואים'

def test_check_area_match():
    assert check_area_match('דרום', 'דרום') == True
    assert check_area_match('דרום', 'צפון') == False

def test_check_eligibility_match():
    # בדיקת התאמה לכולם
    assert check_eligibility_match('חיילי מילואים', 'כולם') == True
    assert check_eligibility_match('נכי צהל', 'כולם') == True
    
    # בדיקת התאמה ספציפית
    assert check_eligibility_match('נכי צהל', 'נכי צה"ל') == True
    assert check_eligibility_match('חיילי מילואים', 'חיילי מילואים') == True
    
    # בדיקת אי-התאמה
    assert check_eligibility_match('חיילי מילואים', 'נכי צה"ל') == False

def test_check_housing_match():
    # בדיקת התאמה לחסרי דיור
    assert check_housing_match('כן', 'חסרי דיור') == True
    assert check_housing_match('לא', 'חסרי דיור') == False
    
    # בדיקת מקרים ללא דרישת דיור
    assert check_housing_match('כן', '') == True
    assert check_housing_match('לא', '') == True
```

### 2.2 בדיקות אינטגרציה
```python
def test_comprehensive_matching():
    # יצירת נתוני בדיקה
    test_profiles = pd.DataFrame([
        {
            'מספר_פרופיל': '001',
            'ימי_מילואים_מ-7.10.23': 45,
            'תעודת_מילואים_פעיל': 'לא',
            'ימי_מילואים_ב-6_שנים': 0,
            'סיווג_נכות': '',
            'חסר_דיור': 'כן',
            'אזור_מועדף': 'דרום',
            'בן/בת_זוג_זכאי': 'לא'
        }
    ])
    
    test_tenders = pd.DataFrame([
        {
            'id': '001',
            'מספר המכרז': 'T001',
            'עיר': 'באר שבע',
            'אזור גיאוגרפי ': 'דרום',
            'מי רשאי להגיש': 'חיילי מילואים',
            'סטטוס דיור נדרש': 'חסרי דיור'
        }
    ])
    
    # בדיקת תוצאות ההתאמה
    matches = create_comprehensive_matching_table(test_profiles, test_tenders)
    assert len(matches) == 1
    assert matches.iloc[0]['מספר_מכרז'] == 'T001'
```

### 2.3 בדיקות ממשק משתמש (UI Tests)
```python
def test_ui_components():
    # בדיקת טעינת הדף
    assert st.title.text == "מילואים וזוכים - מערכת התאמה למציאת מכרזים"
    
    # בדיקת שדות הקלט
    assert st.number_input["ימי_מילואים_מ-7.10.23"].min_value == 0
    assert st.selectbox["תעודת_מילואים_פעיל"].options == ["כן", "לא"]
    assert st.selectbox["אזור_מועדף"].options == ["דרום", "צפון", "ירושלים", "מרכז", "יהודה ושומרון"]
    
    # בדיקת טקסט עזרה
    assert "טופס 3010" in st.number_input["ימי_מילואים_מ-7.10.23"].help
```

### 2.4 בדיקות קצה (Edge Cases)
```python
def test_edge_cases():
    # בדיקת ערכים גבוליים
    assert is_miluim_soldier(days_since_oct=44, has_active_card=False, days_in_6_years=79) == False
    assert is_miluim_soldier(days_since_oct=45, has_active_card=False, days_in_6_years=79) == True
    
    # בדיקת ערכים חסרים
    assert check_housing_match('כן', None) == True
    assert check_area_match(None, 'דרום') == False
    
    # בדיקת מקרי קצה בהטבות
    test_profile = {
        'בן/בת_זוג_זכאי': 'כן',
        'חסר_דיור': 'כן',
        'אזור_עדיפות': 'א'
    }
    benefits = calculate_benefits(test_profile)
    assert benefits['max_discount'] <= 200000  # בדיקת תקרת הטבה לבני זוג
```

## 3. תרחישי בדיקה עיקריים

### 3.1 תרחישי חיילי מילואים
1. חייל מילואים עם 45+ ימי שירות מ-7.10.23
2. חייל מילואים עם תעודת מילואים פעיל
3. חייל מילואים עם 80+ ימי שירות ב-6 שנים
4. חייל מילואים שאינו עומד באף קריטריון

### 3.2 תרחישי נכי צה"ל
1. נכה צה"ל עם נכות קשה
2. נכה צה"ל עם 100% ומעלה
3. נכה צה"ל שגם משרת במילואים

### 3.3 תרחישי דיור והתאמה
1. חסר דיור באזור עדיפות א'
2. חסר דיור באזור עדיפות ב'
3. לא חסר דיור באזור ללא עדיפות
4. בני זוג ששניהם משרתי מילואים

## 4. כלי בדיקות
- pytest לבדיקות יחידה ואינטגרציה
- Streamlit Testing Tools לבדיקות ממשק
- Coverage.py למדידת כיסוי הבדיקות

## 5. תהליך הבדיקות
1. הרצת בדיקות יחידה בכל commit
2. בדיקות אינטגרציה לפני כל merge
3. בדיקות UI ידניות בכל גרסה חדשה
4. בדיקות רגרסיה מלאות לפני כל release

## 6. מדדי הצלחה
- כיסוי בדיקות של לפחות 90%
- זמן ריצת כל הבדיקות פחות מ-5 דקות
- אפס באגים קריטיים בייצור
- דיוק של 100% בחישובי זכאות והטבות

## 7. תיעוד בדיקות
- תיעוד מלא של כל מקרי הבדיקה
- דוחות כיסוי אוטומטיים
- תיעוד באגים ופתרונם
- מעקב אחר שיפורים בתהליך הבדיקות 