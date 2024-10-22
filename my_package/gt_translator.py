from googletrans import Translator
from googletrans import LANGUAGES

translator = Translator()


def translate(text: str, src: str = 'auto', dest: str = 'uk') -> str:
    '''
    Функція повертає текст перекладений на задану мову, або повідомлення про помилку.
    '''

    try:
        return translator.translate(text, dest, src).text
    except Exception as e:
        print(f"Помилка: {translate(e)}")


def lang_detect(text: str, set: str = "all") -> str:
    '''
    Функція визначає мову та коефіцієнт довіри для заданого тексту,
    або повертає повідомлення про помилку.
    '''

    detected = translator.detect(text)

    if set == "all":
        return {
            'language': detected.lang,
            'confidence': detected.confidence
        }
    elif set == "lang":
        return detected.lang
    elif set == "confidence":
        return detected.confidence
    else:
        return "Неправильний параметр 'set'"


def code_lang(lang: str) -> str:
    '''
    Функція повертає код мови (відповідно до таблиці), якщо в параметрі lang міститься назва
    мови, або повертає назву мови, якщо в параметрі lang міститься її код,
    або повідомлення про помилку
    '''

    for code, name in LANGUAGES.items():
        if name.lower() == lang:
            return code

    try:
        language_name = LANGUAGES[lang]
        return language_name
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

    try:
        if out == "file":
            with open("language_list.txt", "w", encoding="utf-8") as file:
                file.write(
                    f"{'№':<5}{'ISO-639 code':<14}{'Language Name':<20}{'Text exapmle' if text else ''}\n")
                file.write(f"{'-'*60}\n")

                print("Триває запис таблиці до файлу:")

                lang_list = LANGUAGES.items()

                for i, (code, name) in enumerate(lang_list, start=1):
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

            for i, (code, name) in enumerate(LANGUAGES.items(), start=1):
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
