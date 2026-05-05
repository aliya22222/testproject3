import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = 'data.json'

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []

        # Создаем интерфейс
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Поля для ввода
        frame_input = ttk.Frame(self.root)
        frame_input.pack(padx=10, pady=10, fill='x')

        ttk.Label(frame_input, text="Название книги").grid(row=0, column=0, sticky='w')
        self.entry_title = ttk.Entry(frame_input)
        self.entry_title.grid(row=0, column=1, sticky='ew')

        ttk.Label(frame_input, text="Автор").grid(row=1, column=0, sticky='w')
        self.entry_author = ttk.Entry(frame_input)
        self.entry_author.grid(row=1, column=1, sticky='ew')

        ttk.Label(frame_input, text="Жанр").grid(row=2, column=0, sticky='w')
        self.entry_genre = ttk.Entry(frame_input)
        self.entry_genre.grid(row=2, column=1, sticky='ew')

        ttk.Label(frame_input, text="Количество страниц").grid(row=3, column=0, sticky='w')
        self.entry_pages = ttk.Entry(frame_input)
        self.entry_pages.grid(row=3, column=1, sticky='ew')

        # Кнопка добавления
        self.btn_add = ttk.Button(frame_input, text="Добавить книгу", command=self.add_book)
        self.btn_add.grid(row=4, column=0, columnspan=2, pady=5)

        # Таблица для отображения книг
        self.tree = ttk.Treeview(self, columns=('Автор', 'Жанр', 'Страниц'), show='headings')
        self.tree.heading('Автор', text='Автор')
        self.tree.heading('Жанр', text='Жанр')
        self.tree.heading('Страниц', text='Страниц')
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

        # Фильтры
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(padx=10, pady=5, fill='x')

        ttk.Label(filter_frame, text="Фильтр по жанру").grid(row=0, column=0)
        self.genre_filter = ttk.Entry(filter_frame)
        self.genre_filter.grid(row=0, column=1)

        ttk.Label(filter_frame, text="Страниц больше").grid(row=0, column=2)
        self.pages_filter = ttk.Entry(filter_frame)
        self.pages_filter.grid(row=0, column=3)

        self.btn_filter = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        self.btn_filter.grid(row=0, column=4, padx=5)

        self.btn_clear_filter = ttk.Button(filter_frame, text="Сбросить фильтр", command=self.load_data)
        self.btn_clear_filter.grid(row=0, column=5, padx=5)

    def add_book(self):
        title = self.entry_title.get().strip()
        author = self.entry_author.get().strip()
        genre = self.entry_genre.get().strip()
        pages = self.entry_pages.get().strip()

        # Валидация
        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return
        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом")
            return

        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        }

        self.books.append(book)
        self.save_data()
        self.load_data()
        self.clear_inputs()

    def clear_inputs(self):
        self.entry_title.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_pages.delete(0, tk.END)

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.books = json.load(f)
        else:
            self.books = []

        for book in self.books:
            self.tree.insert('', 'end', values=(book['author'], book['genre'], book['pages']), text=book['title'])

    def apply_filter(self):
        genre_filter = self.genre_filter.get().strip().lower()
        pages_filter = self.pages_filter.get().strip()

        filtered_books = self.books

        if genre_filter:
            filtered_books = [b for b in filtered_books if b['genre'].lower() == genre_filter]
        if pages_filter:
            if not pages_filter.isdigit():
                messagebox.showerror("Ошибка", "Количество страниц для фильтра должно быть числом")
                return
            pages_threshold = int(pages_filter)
            filtered_books = [b for b in filtered_books if b['pages'] > pages_threshold]

        self.tree.delete(*self.tree.get_children())
        for book in filtered_books:
            self.tree.insert('', 'end', values=(book['author'], book['genre'], book['pages']), text=book['title'])

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()