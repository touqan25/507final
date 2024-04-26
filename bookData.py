import requests
import json


#Get a list of books from the NYT Books API
def get_bestSellers(year):
    '''
    Retrieves the NYT best sellers titles for a given year from the NYT Books API

    Parameters:
    year (int): the year to retrieve the best sellers for

    Returns:
    list: a list of the best sellers titles for the given year(s)

    '''
    url = f"https://api.nytimes.com/svc/books/v3/lists/full-overview.json?published_date={year}-12-31&api-key=Kutew7VmatcyA09AaeeTWsIudOa0Gx10"
    response = requests.get(url)
    data = json.loads(response.text)

    book_titles =[]
    for bookList in data['results']['lists']:
        for book in bookList['books']:
            title = book['title']
            if title not in book_titles:
                book_titles.append(book['title'])

    return book_titles

class Book:
    def __init__(self, title, author=None, subjects=None, ratings_average=None, readinglog_count=None):
        self.title = title
        self.author = author
        self.subjects = subjects or []
        self.ratings_average = ratings_average
        self.readinglog_count = readinglog_count

    def to_dict(self):
        return {
            'title': self.title,
            'author': self.author,
            'subjects': self.subjects,
            'ratings_average': self.ratings_average,
            'readinglog_count': self.readinglog_count
        }

    def __str__(self):
        return f"Title: {self.title}, Author: {', '.join(self.author)}, Subjects: {', '.join(self.subjects)}, Ratings Average: {self.ratings_average}, Reading Log Count: {self.readinglog_count}"



def get_open_library_data(title):
    '''
    Retrives book data from Open Library API for a given title

    Parameters:
    title (str): the title of the book to retrieve the data for

    Returns:
    dict: a dictionary containing the book data retrieved from Open Library API
    '''
    url = f"https://openlibrary.org/search.json?title={title}"
    response = requests.get(url)
    data = json.loads(response.text)
    if data['numFound'] > 0:
        return data['docs'][0]


def read_book_titles_from_file(filename):
    '''
    Reads the book titles from a json file

    Parameters:
    filename (str): the name of the file to read the book titles from

    Returns:
    list: a list of book titles
    '''
    with open(filename, 'r', encoding='utf-8') as file:
        book_titles = json.load(file)
    book_titles_lower = [title.lower() for title in book_titles]
    return book_titles_lower

def get_book_info(titles):
    '''
    Retrieves the book information for a given list of books from the OpenLibrary API

    Parameters:
    book_titles (list): a list of book titles to retrieve the information

    Returns:
    list: a list of dictionaries containing the book information

    '''
    books = []
    for title in titles:
        book_data = get_open_library_data(title)
        if book_data:
            book_info = extract_book_info(book_data)
            # print("Book Info:", book_info)
            for info in book_info:
                book = Book(info['title'], info['author'], info['subjects'], info['ratings_average'], info['readinglog_count'])
                books.append(book)
    return books

def extract_book_info(book_data):
    '''
    Extracts the book information from the book data retrieved from Open Library API

    Parameters:
    book_data (dict): a dictionary containing the book data retrieved from Open Library API

    Returns:
    list: a list of dictionaries containing the book title, subjects, average rating, and reading log count
    '''
    print("Book Data:", book_data)
    # print("Keys in book data:", book_data.keys())
    book_info = []
    if book_data:
            title = book_data.get('title', "N/A")
            author = book_data.get('author_name', [])
            subjects = book_data.get('subject', [])
            ratings_average = book_data.get('ratings_average', "N/A")
            readinglog_count = book_data.get('readinglog_count', "N/A")
            book_info.append({
                'title': title,
                'author': author,
                'subjects': subjects,
                'ratings_average': ratings_average,
                'readinglog_count': readinglog_count
            })
    return book_info

def save_books_to_file(books, filename):
    '''
    Saves the book information to a json file

    Parameters:
    books (list): a list of dictionaries containing the book information
    filename (str): the name of the file to save the book information to
    '''
    book_dict = {}
    for book in books:
        book_dict[book.title] = book.to_dict()
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(book_dict, file, ensure_ascii=False, indent=4)

def main():
    # Trying to see and understand the results of the API call
    # url = "https://api.nytimes.com/svc/books/v3/lists/full-overview.json?published_date=2021-12-31&api-key=Kutew7VmatcyA09AaeeTWsIudOa0Gx10"
    # response = requests.get(url)
    # data = json.loads(response.text)
    # for list in data['results']['lists']:
    #     for book in list['books']:
    #         print(book['title'])

    # Creating book titles list for the years 2017-2021
    # book_titles = []
    # book_titles.extend(get_bestSellers(2021))
    # book_titles.extend(get_bestSellers(2020))
    # book_titles.extend(get_bestSellers(2019))
    # book_titles.extend(get_bestSellers(2018))
    # book_titles.extend(get_bestSellers(2017))
    # print(book_titles)

    # Trying to see and understand the results of the API call to OpenLibrary
    # title="The Judge's List"

    # url = f"https://openlibrary.org/search.json?title={title}"
    # response = requests.get(url)
    # data = json.loads(response.text)
    # print(data['docs'][0]['ratings_average'])


    # Saving the book titles to a json file, this way we don't have to make the API call every time. Also it was being super flaky on me, so I just wanted to save the data and be done with that part
    # with open('book_titles.json', 'w', encoding='utf-8') as file:
    #     json.dump(book_titles, file, ensure_ascii=False, indent=4)

    # Reading the book titles from the json file
    book_titles = read_book_titles_from_file('book_titles.json')
    books = get_book_info(book_titles[:50])
    # for book in books:
    #     print(book)

    save_books_to_file(books, 'books.json')


    # Getting the book information for the book titles
    # books = get_book_info(book_titles)



if __name__ == "__main__":
    main()


