from googletrans import Translator

text = '''Buenos días cómo estás'''

translator = Translator()

lang = translator.detect(text)
print(lang)

res = translator.translate(text)
print(res)
