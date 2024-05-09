import re


def check_name_safety(name: str) -> bool:
    # Паттерн для безопасных символов (включая русские буквы и пробелы)
    pattern = r'^[a-zA-Zа-яА-Я0-9()\-_/\\.\s]+$'

    # Проверяем, соответствует ли строка паттерну
    return bool(re.match(pattern, name))


if __name__ == '__main__':
    print(check_name_safety('KhOBOD_Spark_streaming_Kafka_amp_NoSQL_over_BigData (2).pdf'))
