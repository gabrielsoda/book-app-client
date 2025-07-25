from rich.console import Console
from rich.panel import Panel
from term_image.image import AutoImage
from term_image import set_cell_ratio
import requests

# Configuración
random_book_url = 'http://saynomore.com.ar:8001/random'
console = Console()
set_cell_ratio(0.5)  # Ajusta según tu terminal

def get_random_book(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['book']

def print_book(book: dict):
    # Panel de información
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

    image_path = book.get('imageLink')
    if not image_path:
        console.print("[yellow]Este libro no tiene una imagen asociada.[/yellow]")
        return

    image_url = f"http://saynomore.com.ar:8001/{image_path}"

    try:
        console.print("Cargando imagen de portada...")
        response = requests.get(image_url, timeout=5)
        if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
            image = AutoImage.from_bytes(response.content, width=50)
            console.print(image)
        else:
            console.print(f"[red]No se pudo descargar la imagen (status: {response.status_code}).[/red]")
    except Exception as e:
        console.print(f"[red]Error al mostrar la imagen: {e}[/red]")

def show_book(url: str):
    book = get_random_book(url)
    print_book(book)

# Ejecutar
show_book(random_book_url)
