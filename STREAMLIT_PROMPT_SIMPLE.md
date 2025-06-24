# איך ליצור ממשק Streamlit מושלם

היי! אני צריך/ה ממשק Streamlit בעברית שיהיה:
1. קל לקריאה
2. נוח לשימוש
3. יפה ומקצועי

## מה חשוב לי במיוחד:
- שכל הטקסט יהיה בעברית מימין לשמאל
- שהכל יהיה קריא בקלות (שחור על לבן, גופן גדול וברור)
- שיהיה ברור מה כל כפתור ושדה עושה בלי להתאמץ

## מבנה הדף:
1. לוגו קטן למעלה
2. כותרת ראשית גדולה
3. שני קטעי מידע קצרים להסבר
4. טופס בצד ימין (30% מהרוחב)
5. תוצאות בצד שמאל (70% מהרוחב)

## לכל שדה בטופס צריך:
1. כותרת ברורה עם אייקון
2. שדה קלט גדול עם מסגרת כחולה
3. הסבר קצר וברור מתחת לשדה

## עיצוב:
- גופן: Heebo מ-Google Fonts
- צבעים: כחול-לבן עם הדגשות כחולות (#4a90e2)
- כפתורים: גדולים עם צבע בולט
- מסגרות: עבות (3 פיקסלים) בצבע כחול
- רווחים: נדיבים בין כל האלמנטים

## דוגמה לשדה:
```python
# כותרת השדה
st.markdown("#### 🗓️ ימי מילואים")

# השדה עצמו
days = st.number_input("הכנס מספר ימים:", min_value=0)

# הסבר
st.info("💡 מעל 45 ימים = הנחה של 35%")
```

## CSS הכרחי:
```css
<style>
/* עברית מימין לשמאל */
* {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Heebo', sans-serif !important;
}

/* שדות קלט */
.stSelectbox > div, .stNumberInput > div {
    background: white !important;
    border: 3px solid #4a90e2 !important;
    border-radius: 12px !important;
}

/* כותרות כרטיסיות */
.stExpander details summary {
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%) !important;
    font-size: 1.4rem !important;
    color: white !important;
    text-align: center !important;
}
</style>
```

## חשוב במיוחד:
- בלי tooltips נסתרים - כל המידע צריך להיות גלוי
- טקסט שחור על רקע לבן בלבד
- כל כפתור צריך להיות ברור למה הוא עושה
- הכל צריך להיות קריא גם בלי להתקרב למסך

תודה! 🙏 