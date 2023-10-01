import re


def check_name_safety(name: str) -> bool:
    # Паттерн для безопасных символов
    pattern = r'^[a-zA-Z0-9\-_/\\.]+$'

    # Проверяем, соответствует ли строка паттерну
    return bool(re.match(pattern, name))

# if __name__ == '__main__':
#     print(check_name_safety('concept_1324.pdf'))