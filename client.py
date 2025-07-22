
import os
import json
import requests
import questionary


random_book_url = 'http://saynomore.com.ar:8001/random'

def show_random_book(url):
    response = requests.get(url)
    response.raise_for_status()
    book = json.loads(response.text)
    print(book)
    print(type(book))
    print(book["title"])
    title = book['title'] 
    author = book['author']
    year = book['year']
    imageLink = book['imageLink']


show_random_book(random_book_url)