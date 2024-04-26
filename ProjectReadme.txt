Description: 
My project creates a network graph visualization of NYT Bestseller books and allows the user to explore the network by searching for specific books, getting information on specific books (e.g. author, average rating, and popularity based on how many users have added it to their reading log), and getting recommendations based on books they search (which can be filtered by whether the user wants only rated books). This project gathered data from two APIs
--NYT Book API (this grabbed NYT Bestseller titles, these are stored in book_titles.json)
--OpenLibrary API (I used the book_titles.json file to query the API to grab relevant book information such as author, subjects, ratings, and readinglog_count, objects were stored in books.json)

Network Organization:
Nodes: Each node represents a NYT Bestseller. Node color denotes average rating (red: 1-2 stars, orange: 2-3 stars, yellow: 3-4 stars, and green: 4-5 stars). Node size denotes popularity (readinglog_count: the bigger the node, the more popular the book)
Edges: The edges represent common Library of Congress Subject headings between books, but excludes the "New York Times Bestseller" subject heading. 

Here are a list of interactions available:
1. Searching for a book
>>user will be prompted to "Enter the title of the book to search" to which they respond with the book search (case insensitive search)
>>program will respond with whether that book is in the network

2. Getting more information about the book (after user successfully finds a book in the network)
>> user will be prompted to answer: "Do you want to see more information about this book?" to which they respond with "y" or "n"
>> if "y" the program will provide a list to the user containing the book's title, subjects, average rating, and readinglog_count
>> if "n" the program will go back to the options menu

3. Getting book recommendations
>>user will be prompted to "Enter the title of the book to recommend other books:" to which they respond with the book search (case sensitive search)
>>if book is found, will ask the user: "Do you want the recommended books to have a high rating (at least 4 stars)?" to which they respond with "y" or "n"
>>if "y" program will return list of books with at least 2 shared subjects and a rating of 4.0 stars and above
>>if "n" program will return all books with at least 2 shared subjects

Special Instructions/API Keys: 
None to run this program in particular, but NYT Book API does require a key. So if you want to get a different list of NYT Bestsellers or expand the network, you will need to use a key

Required Packages:
networkx
matplotlib

Video Demo:
https://youtu.be/GFeZHgzyBQQ
