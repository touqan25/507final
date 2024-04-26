Data Sources:
1. NYT Book API
>> Origin: https://developer.nytimes.com/docs/books-product/1/routes/lists/full-overview.json/get
>> Sample Response: https://developer.nytimes.com/docs/books-product/1/types/OverviewResponse
>> Format: JSON (both what it returns and how I saved the data)
>> Accessed by: I accessed the data by querying the API using this search query: "https://api.nytimes.com/svc/books/v3/lists/full-overview.json?published_date={year}-12-31&api-key=Kutew7VmatcyA09AaeeTWsIudOa0Gx10" I originally got about 5 years worth of data, but this proved too much to deal with all at once when querying the next API.
>> I stored these data in book_titles.json so I would not have to repeatedly call the API (especially since it was a little unreliable)
>> Data Summary: I only stored the book titles from this API return

2. OpenLibrary API
>> Origin: https://openlibrary.org/dev/docs/api/search
>> Sample Response: https://openlibrary.org/search.json?q=the+lord+of+the+rings
>> Format: JSON (both what it returns and how I saved the data)
>> Accessed by: I accessed the data by querying the API using this search query: "url = f"https://openlibrary.org/search.json?title={title}" -- paired with a function that loops through the book_titles.json (which I got from the API query above). This API was also slow and unreliable, and my computer really could only handle grabbing so many books. So, I grabbed the first 50 books for the sake of this project and visualizing the network. However, you can change that number (line 181) to grab more book data. 
>> I stored these data in books.json as a dict of dicts (optimal structure for networkX)
>> Data Summary: from this query I pulled the title, author, subject list, ratings_average, and readinglog_count.
