def process_with_claude(text):
    prompt = f"""
Išanalizuokite šį lietuvišką tekstą:
1. Patikrinkite rašybos ir gramatikos klaidas
2. Sutvarkykite skyrybą
3. Pažymėkite kirčiuotus skiemenis naudojant akūto ženklą (´) virš kirčiuotos balsės
4. Suskaičiuokite visas klaidas (rašybos, gramatikos ir skyrybos)

Tekstas:
\"""
{text}
\"""

Grąžinkite JSON objektą su:
{{
    "corrected_text": "pataisytas tekstas su kirčiais",
    "error_count": klaidų skaičius,
    "error_details": "trumpas klaidų aprašymas"
}}

Pastaba: kirčiuokite tik tuos žodžius, kurie turi aiškų kirčiavimą pagal lietuvių kalbos taisykles."""

    try:
        response = anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1500,
            temperature=0.1,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        import json
        result = json.loads(response.content[0].text.strip())
        
        # Добавляем обратную связь только если есть ошибки
        if result['error_count'] > 0:
            result['feedback'] = get_random_feedback(result['error_count'])
        else:
            result['feedback'] = "🌟 Puiku! Tekstas parašytas be klaidų! ⭐"
            
        return result
        
    except Exception as e:
        app.logger.error(f"API klaida: {e}")
        return {
            "corrected_text": text,
            "error_count": 0,
            "error_details": "Įvyko klaida analizuojant tekstą",
            "feedback": "😅 Atsiprašome, įvyko klaida! Bandykite dar kartą! 🔄"
        }
