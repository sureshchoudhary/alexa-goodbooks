import sys,xmltodict
from collections import OrderedDict
import requests

class BookQuery():
    def __init__(self,key,query):
        self.books = []
        br = None

        try:
            br = requests.get('https://www.goodreads.com/search/index.xml?key=' + key + '&q=' + query)
        except requests.exceptions.ConnectionError:
            # do nothing - keep None
            pass

        if br == None or br == "":
            pass
        elif br.status_code != 200:
            pass
        else:
            doc = xmltodict.parse(br.text)
            try:
                books = doc['GoodreadsResponse']['search']['results']['work']
                if type(books) is OrderedDict:
                    # if just single entry, append to the empty list
                    self.books.append(books)
                else:
                    # if multiple entries are found, it will already be a list
                    self.books = books

            except TypeError:
                # do nothing - keep None
                pass

    def _get_field(self,field):
        pass

    def _get_book_id(self,book):
        book_id = 0
        try:
            book_id = book['best_book']['id']
        except KeyError:
            pass
        if type(book_id) is OrderedDict:
            book_id = book['best_book']['id']['#text']

        return book_id

    def _get_author(self,book):
        author_id = 0
        try:
            author_id = book['best_book']['author']['id']
        except KeyError:
            pass
        if type(author_id) is OrderedDict:
            author_id = book['best_book']['author']['id']['#text']

        author_name = book['best_book']['author']['name']

        return author_id,author_name

    def _get_rating(self,book):
        rating  = 0
        try:
            rating = book['average_rating']
        except KeyError:
            pass
        if type(rating) is OrderedDict:
            rating = book['average_rating']['#text']

        return rating

    def _get_published_year(self,book):
        published = 0
        try:
            published = book['original_publication_year']['#text']
        except KeyError:
            pass
        if published == None or int(published) < 0:
            published = 0

        return published

    def get_book(self):
        for book in self.books:
            book_id = self._get_book_id(book)

            title   = book['best_book']['title']

            author_id,author_name  = self._get_author(book)

            rating = self._get_rating(book)
            published_year = self._get_published_year(book)

            yield (int(book_id),title,int(author_id),author_name,rating,published_year)


if __name__ == '__main__':
    key = sys.argv[1]
    title = sys.argv[2]

    bq = BookQuery(key,title)

    if bq.books == []:
        print("No books")
    else:
        for book_id,title,author_id,author,rating,published in bq.get_book():
            print(book_id,title,author_id,author,rating,published)
