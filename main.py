import numpy as np
import requests
from matplotlib import pyplot as plt
import json
from tkinter import Tk, Button, Label, messagebox, Entry, Text, END


def capture_data():
    url = "http://192.168.1.30/api/v1/profile/capture?count=1000/results"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(response.json())
        else:
            messagebox.showerror("Ошибка", f"Не удалось захватить данные. Код ошибки: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка при захвате данных: {str(e)}")

def get_results(text_field):
    url = "http://192.168.1.30/api/v1/smart/graph/results"
    try:
        response = requests.get(url)
        json_data = json.loads(response.text)
        segments = json_data["profile"]["approximation"]
        if response.status_code == 200:
            # Очистка текстового поля перед добавлением новых данных
            text_field.delete('1.0', END)
            # Добавление результатов в текстовое поле
            text_field.insert(END, str(segments))
            print(str(segments))

            # Построение графика с линиями между каждой парой точек
            plt.figure(figsize= (4, 7))  # Устанавливаем размер фигуры для лучшего визуального представления
            plt.xlim(-160, 160)  # Устанавливаем пределы оси X
            plt.ylim(0, 300)  # Устанавливаем пределы оси Y

            for segment in segments:
                x_values = [segment['p1x'], segment['p2x']]
                y_values = [segment['p1z'], segment['p2z']]
                plt.plot(x_values, y_values, 'b')  # Используем синий цвет для линий

            plt.title('Линии между точками из результатов')
            plt.xlabel('X')
            plt.ylabel('Z')

            # Отображаем график
            plt.show()
        else:
            messagebox.showerror("Ошибка", f"Не удалось получить результаты. Код ошибки: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка при получении результатов: {str(e)}")

# Создание окна
root = Tk()
root.title("Лазерный датчик")

# Создание текстового поля для вывода результатов
results_text = Text(root, height=30, width=50)
results_text.pack(pady=10)

# Создание кнопок и привязка функций к ним
capture_button = Button(root, text="Захватить данные", command=capture_data)
capture_button.pack(pady=10)

# Передаем текстовое поле как аргумент в функцию get_results при нажатии кнопки
results_button = Button(root, text="Получить результаты", command=lambda: get_results(results_text))
results_button.pack(pady=10)

root.mainloop()
