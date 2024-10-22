from deep_translator import GoogleTranslator
from langdetect import detect_langs


def translate(text: str, src: str = 'auto', dest: str = 'uk') -> str:
    '''
    Функція повертає текст перекладений на задану мову, або повідомлення про помилку.
    '''

    try:
        return GoogleTranslator(src, dest).translate(text)
    except Exception as e:
        print(f"Помилка: {translate(e)}")


def lang_detect(text: str, set: str = "all") -> str:
    '''
    Функція визначає мову та коефіцієнт довіри для заданого тексту,
    або повертає повідомлення про помилку.
    '''

    detected = detect_langs(text)

    if set == "all":
        return {
            'language': detected[0].lang,
            'confidence': detected[0].prob
        }
    elif set == "lang":
        return detected[0].lang
    elif set == "confidence":
        return detected[0].prob
    else:
        return "Неправильний параметр 'set'"


def code_lang(lang: str) -> str:
    '''
    Функція повертає код мови (відповідно до таблиці), якщо в параметрі lang міститься назва
    мови, або повертає назву мови, якщо в параметрі lang міститься її код,
    або повідомлення про помилку
    '''
    translator = GoogleTranslator()

    for name, code in translator.get_supported_languages(as_dict=True).items():
        if code == lang:
            return name

    try:
        code = translator.get_supported_languages(as_dict=True)[lang]
        return code
    except KeyError:
        return "Мови з такою назвою або кодом не існує"
    except Exception as e:
        print(f"Помилка: {translate(e)}")


def language_list(out="screen", text=None):
    """
    Виводить в файл або на екран таблицю всіх мов, що підтримуються, та їх кодів,
    а також текст, перекладений на цю мову. Повертає 'Ok', якщо всі операції виконані,
    або повідомлення про помилку.

    :param out: 'screen' (по замовченню) - вивести таблицю на екран, 'file' - вивести таблицю в файл
    :param text: текст, який необхідно перекласти. Якщо параметр відсутній, то відповідна колонка в таблиці також повинна бути відсутня.
    :return: 'Ok', якщо операція виконана успішно, або повідомлення про помилку
    """
    translator = GoogleTranslator()

    try:
        if out == "file":
            with open("language_list.txt", "w", encoding="utf-8") as file:
                file.write(
                    f"{'№':<5}{'ISO-639 code':<14}{'Language Name':<20}{'Text exapmle' if text else ''}\n")
                file.write(f"{'-'*60}\n")

                lang_list = translator.get_supported_languages(
                    as_dict=True).items()

                print("Триває запис таблиці до файлу:")

                for i, (name, code) in enumerate(lang_list, start=1):
                    text_example = ''
                    if text:
                        text_example = f"\t{translate(text, 'auto', code)}"
                    file.write(
                        f"{f'{i}.':<5}{code:<13}{name:<20}{text_example}\n")

                    percent_done = round(i / len(lang_list) * 100)
                    print(f"{'=' * (percent_done // 2)} {percent_done}%",
                          end='\r', flush=True)

                file.write(f"{'-'*60}\nOk\n")
            print('\n')

        elif out == 'screen':
            print(
                f"{'№':<5}{'ISO-639 code':<14}{'Language Name':<20}{'Text exapmle' if text else ''}")
            print(f"{'-'*60}")

            for i, (name, code) in enumerate(translator.get_supported_languages(as_dict=True).items(), start=1):
                text_example = ''
                if text:
                    text_example = f"{translate(text, 'auto', code)}"
                print(f"{f'{i}.':<5}{code:<13}{name:<20}{text_example}")

            print(f"{'-'*60}\nOk\n")
        else:
            return "Помилка: Невідомий параметр"

        return "Ok"

    except Exception as e:
        print(f"Помилка: {translate(e)}")
