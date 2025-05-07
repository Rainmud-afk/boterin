import pymorphy2

morph = pymorphy2.MorphAnalyzer()

positive_words = {"счастлив", "рад", "доволен", "спокойный", "вдохновлён"}
negative_words = {"грусть", "печаль", "устал", "злость", "раздражён"}

def analyze_mood(text):
    words = text.lower().split()
    score = 0
    for word in words:
        parsed = morph.parse(word)[0]
        normal = parsed.normal_form
        if normal in positive_words:
            score += 1
        elif normal in negative_words:
            score -= 1
    if score > 0:
        return "Позитивное 🙂"
    elif score < 0:
        return "Негативное 🙁"
    else:
        return "Нейтральное 😐"
