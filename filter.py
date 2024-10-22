import json
import os

from my_package.gt_translator import code_lang, lang_detect
from my_package.gt_translator import translate

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

source_file: str = config['source_filename']

try:
    print(f"Назва файлу: {source_file}")
    print(f"Розмір файлу: {round(os.path.getsize(source_file)/1024, 2)} KB")
except FileNotFoundError:
    print(f"Помилка: Файл {source_file} не знайдено")
    exit()

except Exception as e:
    print(f"Виникла невідома помилка: {translate(e)}")
    exit()

text_extracted = ''

max_word_number = config['word_number']
max_sentence_number = config['sentence_number']

word_number = 0
sentence_number = 0

with open(source_file, 'r', encoding='utf-8') as file:
    for _ in range(config['symbol_number']):
        char = file.read(1)

        if not char:
            sentence_number += 1
            break

        text_extracted += char

        if char.isspace():
            word_number += 1

            if word_number >= max_word_number:
                break

        if char in '.?!':
            sentence_number += 1

            if sentence_number >= max_sentence_number:
                break

print(f"Кількість символів: {len(text_extracted)}")
print(f"Кількість слів: {word_number}")
print(f"Кількість речень: {sentence_number}")

source_lang_code = lang_detect(text_extracted, set='lang')
source_lang = code_lang(source_lang_code)

print(f"Мова тексту: {translate(source_lang)}")

target_language = config['target_language']
text_translated = translate(text_extracted, 'auto', target_language)
target_lang_name = code_lang(target_language)


if config['result_location'] == 'screen':
    print(f"\n{translate(f'Translation to {target_lang_name}')}: \n{text_translated}")

elif config['result_location'] == 'file':
    source_filename_parts = source_file.split('.')
    try:
        with open(f"{'.'.join(source_filename_parts[:-1])}_{target_language}.{source_filename_parts[-1]}", 'w', encoding='utf-8') as result_file:
            result_file.write(text_translated)
            print('Ok')
    except Exception as e:
        print(f"Помилка: {translate(e)}")
else:
    print("Помилка: невідомий параметр 'result_location' - він може мати лише значення 'screen' або 'file'")
