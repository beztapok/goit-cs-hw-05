import requests
import string
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

# Функція для завантаження тексту з URL
def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        print(f"Помилка: {e}")
        return None

# Функція для видалення знаків пунктуації
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

# Функція мапінгу (створює пари слово -> 1)
def map_function(word):
    return word.lower(), 1

# Функція шифтування (групування однакових слів)
def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

# Функція редукції (підсумовує кількість кожного слова)
def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# Функція виконання MapReduce
def map_reduce(text):
    # Видалення пунктуації
    text = remove_punctuation(text)
    words = text.split()

    # Паралельний Мапінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Шифтування
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

# Функція для візуалізації топ-слова
def visualize_top_words(word_count, top_n=10):
    # Сортування слів за частотою
    sorted_words = sorted(word_count.items(), key=lambda item: item[1], reverse=True)
    
    # Вибір топ-N слів
    top_words = sorted_words[:top_n]
    words, frequencies = zip(*top_words)

    # Візуалізація
    plt.barh(words, frequencies, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.gca().invert_yaxis()  # Щоб топ слова були зверху
    plt.show()

if __name__ == '__main__':
    # URL до тексту 
    url = "https://www.gutenberg.org/files/84/84-0.txt"  # Можна змінити URL на будь-який інший
    text = get_text(url)

    if text:
        # Виконання MapReduce для підрахунку слів
        word_count = map_reduce(text)

        # Візуалізація топ 10 найчастіше вживаних слів
        visualize_top_words(word_count, top_n=10)
    else:
        print("Помилка: Не вдалося отримати текст.")
