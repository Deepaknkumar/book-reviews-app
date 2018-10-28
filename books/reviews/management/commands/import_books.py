import csv

from django.core.management import BaseCommand

from reviews.models import Book

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the books data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

class Command(BaseCommand):
    help = "Loads data from books.csv into our Book models"

    def handle(self,*args,**options):
        if Book.objects.exists():
            print("Book data already loaded... Exiting")
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return
        print("Loading Book data from the books.csv file")
        file = open('books.csv')
        reader = csv.reader(file)
        headers = next(reader,None)
        for isbn,title,author,year in reader:
            print(f"Adding {isbn} {title} {author} {year}")
            book = Book(isbn = isbn, title = title, author = author, year = year)
            book.save()
