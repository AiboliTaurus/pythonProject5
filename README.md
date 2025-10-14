# Проект обработки финансовых операций

## О проекте

Проект представляет собой набор инструментов для обработки и анализа финансовых операций, включая маскирование данных, фильтрацию и сортировку операций.

## Цель проекта

Разработка и поддержка набора функций для:

- Маскирования конфиденциальных данных (номера карт и счетов)
- Обработки и фильтрации операций по различным критериям
- Преобразования и сортировки данных по дате

## Установка

Для установки проекта выполните следующие действия:

1.  Клонируйте репозиторий:

bash

git clone &lt;ссылка_на_репозиторий&gt;

1.  Установите зависимости:

bash

pip install -r requirements.txt

## Структура проекта

- masks - модуль для работы с маскированием данных
- widget - модуль для обработки виджетов и преобразования данных
- processing - модуль для обработки и фильтрации операций
- tests - каталог с тестовыми файлами
- generators - новый модуль для работы с генераторами данных

## Тестирование

Для запуска тестов используйте:

bash

pytest

## Требования к окружению

- Python 3.8+
- pytest
- Все зависимости из файла requirements.txt

## Новый модуль: generators

Модуль предоставляет инструменты для работы с генераторами данных при обработке финансовых операций.

### filter_by_currency

Функция для фильтрации транзакций по валюте операции.

## Пример использования:

python

from generators import filter_by_currency

### Пример списка транзакций

transactions = \[...\] # ваш список транзакций

### Фильтрация по USD

usd_transactions = filter_by_currency(transactions, "USD")

for _ in range(2):

print(next(usd_transactions))

### transaction_descriptions

Генератор для получения описаний транзакций.

## Пример использования:

python

from generators import transaction_descriptions

### Пример списка транзакций

transactions = \[...\] # ваш список транзакций

### Получение описаний

descriptions = transaction_descriptions(transactions)

for _ in range(5):

print(next(descriptions))

### card_number_generator

Генератор для создания номеров банковских карт в заданном диапазоне.

## Пример использования:

python

from generators import card_number_generator

### Генерация номеров карт

for card_number in card_number_generator(1, 5):

print(card_number)

### Формат вывода:

0000 0000 0000 0001

0000 0000 0000 0002

0000 0000 0000 0003

0000 0000 0000 0004

0000 0000 0000 0005

## Документация по использованию

Все функции модуля generators предназначены для эффективной работы с большими объемами данных и обеспечивают:

- Последовательную обработку данных
- Низкое потребление памяти
- Простоту интеграции в существующие процессы обработки данных
## Модуль generators
Модуль предоставляет инструменты для работы с генераторами данных при обработке финансовых операций.

### filter_by_currency
Функция для фильтрации транзакций по валюте операции.

### Пример использования:

```python
from generators import filter_by_currency

transactions = [...]  # ваш список транзакций
usd_transactions = filter_by_currency(transactions, "USD")


for _ in range(2):
    print(next(usd_transactions))
transaction_descriptions
```
## Генератор для получения описаний транзакций.

### Пример использования:

```python
from generators import transaction_descriptions

transactions = [...]  # ваш список транзакций
descriptions = transaction_descriptions(transactions)

for _ in range(5):
    print(next(descriptions))
card_number_generator
```
## Генератор для создания номеров банковских карт в заданном диапазоне.

### Пример использования:

```python
from generators import card_number_generator

for card_number in card_number_generator(1, 5):
    print(card_number)
Формат вывода:

0000 0000 0000 0001
0000 0000 0000 0002
0000 0000 0000 0003
0000 0000 0000 0004
0000 0000 0000 0005
```
### Модуль decorators
log
#### Декоратор для логирования выполнения функций. Позволяет записывать логи в файл или консоль.

### Использование:

```python
@log(filename="mylog.txt")
def my_function(x, y):
    return x + y
```
