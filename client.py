from typing import Any
import os
import json
import requests
import httpx
import questionary
from term_image.image import AutoImage
from term_image import set_cell_ratio
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# ficciones = {
#     # "id": 5,
#     "author": "Jorge Luis Borges",
#     # "country": "Argentina",
#     "imageLink": "images/ficciones.jpg",
#     # "language": "Spanish",
#     # "link": "https://en.wikipedia.org/wiki/Ficciones\n",
#     # "pages": 224,
#     "title": "Ficciones",
#     "year": 1965
# }


random_book_url = 'http://saynomore.com.ar:8001/random'
API_BASE_URL = 'http://saynomore.com.ar:8001/random'

console = Console()
client = httpx.Client(base_url=API_BASE_URL, timeout=10.0)

def get_random_book(url) -> Any:
    response = requests.get(url)
    response.raise_for_status()
    book = json.loads(response.text)
    book = book['book']
    return book

def print_book(book):
        
    info_panel = Panel(
            f"[bold]Autor:[/bold] {book.get('author')}\n"
            f"[bold]País:[/bold] {book.get('country')}\n"
            f"[bold]Idioma:[/bold] {book.get('language')}\n"
            f"[bold]Año:[/bold] {book.get('year')}\n"
            f"[bold]Páginas:[/bold] {book.get('pages')}\n"
            f"[bold]Enlace:[/bold] [link={book.get('link')}]{book.get('link')}[/link]",
    title=f"[bold cyan]{book.get('title')}[/bold cyan]",
    border_style="green",
    expand=False
    )
    console.print(info_panel)
    image_link_path = book.get('imageLink')
    images_path = "http://saynomore.com.ar:8001/images/"
    image_filename = f"{images_path}{book.get('id')}"
    print(image_filename)

    set_cell_ratio(0.5)
    try:
        console.print("Cargando imagen de portada...")
        response = requests.get(image_filename)
        if response.status_code == 200:
            image = AutoImage.from_bytes(response.content, width=50)
            console.print(image)
        else:
            console.print(f"[red]No se pudo descargar la imagen (status: {response.status_code})[/red]")
    except Exception as e:
        console.print(f"[red]Error al mostrar la imagen: {e}[/red]")

        
def show_book(url):
     book = get_random_book(url)
     book_info = print_book(book)
     console.print(book_info)

show_book(random_book_url)


def display_book_list(books: list):
    """Muestra una lista de libros en una tabla."""
    if not books:
        console.print("[yellow]No se encontraron libros.[/yellow]")
        return
        
    table = Table(title="Lista de Libros", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="white")
    table.add_column("Título", style="cyan", no_wrap=True)
    table.add_column("Autor", style="green")
    table.add_column("Año", justify="right")
    table.add_column("Páginas", justify="right")

    for book in books:
        table.add_row(str(book['id']), book['title'], book['author'], str(book['year']), str(book['pages']))
    
    console.print(table)