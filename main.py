import json
import os
from http.client import HTTPException
from typing import List

from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    publication_date: str
    genres: List[str]

# Путь к файлу данных
BOOKS_FILE = "Database.json"


def read_books():
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "read") as file:
            return json.load(file)
    return []


# Функция для записи данных в файл
def write_books(books):
    with open(BOOKS_FILE, "write") as file:
        json.dump(books, file, indent=4)


# CRUD
#Создать новую книгу
@app.post("/books", response_model=Book)
def create_book(new_book: Book):
    books = read_books()
    # Проверка на существование книги
    for book in books:
        if book['title'] == new_book.title:
            raise HTTPException(status_code=400, detail="Книга уже существует")

#Получить информацию о книге
@app.get("/books/{book_title}", response_model=Book)
def read_book(book_title: str):
    books = read_books()
    for book in books:
        if book['title'] == book_title:
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")


    books.append(new_book.dict())
    write_books(books)
    return new_book


#Обновить данные о книге
@app.put("/books/{book_title}", response_model=Book)
def update_book(book_title: str, updated_book: Book):
    books = read_books()
    for i, book in enumerate(books):
        if book['title'] == book_title:
            books[i] = updated_book.dict()
            write_books(books)
            return updated_book
    raise HTTPException(status_code=404, detail="Книга не найдена")


#Удалить книгу
@app.delete("/books/{book_title}")
def delete_book(book_title: str):
    books = read_books()
    for i, book in enumerate(books):
        if book['title'] == book_title:
            del books[i]
            write_books(books)
            return {"message": "Книга успешно удалена"}
    raise HTTPException(status_code=404, detail="Книга не найдена")