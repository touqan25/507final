import networkx as nx
import matplotlib.pyplot as plt
import json

# Load the json data
with open('books.json', 'r') as file:
    book_data = json.load(file)

# Create a networkx graph
G = nx.Graph()

# Add nodes to the graph
for title, data in book_data.items():
    if data['readinglog_count'] != 'N/A':
        node_size = int(data['readinglog_count']) * 10
    else:
        node_size = 10

    star_rating = data['ratings_average']
    if star_rating == 'N/A':
        node_color = 'gray'
    else:
        #to differentiate the books based on star rating in the graph, they will be colored differently 
        star_rating = float(star_rating)
        if star_rating >= 4:
            node_color = 'green'
        elif star_rating >= 3:
            node_color = 'yellow'
        elif star_rating >= 2:
            node_color = 'orange'
        else:
            node_color = 'red'
    G.add_node(title, **data, size=node_size, color=node_color)

# for node, data in G.nodes(data=True):
#     print(node, data)

# Add edges to the graph
for title1, data1 in book_data.items():
    for title2, data2 in book_data.items():
        if title1 != title2:
            # Every single book has New York Times Bestseller as a subject, so I did not think it was important to include that one
            subjects1 = set(data1['subjects']) - {"New York Times Bestseller"}
            subjects2 = set(data2['subjects']) - {"New York Times Bestseller"}
            common_subjects = subjects1.intersection(subjects2)
            num_common_subjects = len(common_subjects)
            #I tried to calculate the edge weight based on the number of common subjects between two books, but to be honest it doesn't seem like it makes a difference? I tried a couple of different things but it doesn't seem to change the graph. I'm okay with what I have accomplished thus far though.
            if num_common_subjects > 0:
                edge_weight = num_common_subjects
                G.add_edge(title1, title2, subjects=common_subjects, weight=edge_weight)


pos = nx.random_layout(G)

# Calculate node size based on readinglog_count
node_sizes = [data.get('size', 10) for node, data in G.nodes(data=True)]
node_sizes = [float(size) for size in node_sizes if size != 'N/A']

# Get node attributes for color
node_colors = [data['color'] for node, data in G.nodes(data=True)]

# Plot the network with customized edge visibility
plt.figure(figsize=(10, 8))
nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color=node_colors, font_size=10, font_weight='bold', edge_color='gray', width=1.0, alpha=0.7)
plt.title('Network of Books')
plt.show()


def search_book(graph):
    '''
    Search for a book in the network

    Parameters:
    graph (networkx.Graph): a networkx graph containing the book data

    Returns:
    str: the title of the book
    '''
    book_title = input("Enter the title of the book to search: ").lower()
    for node_title in graph.nodes:
        if book_title.lower() in node_title.lower():
            print(f"Book '{node_title}' found in the network.")
            option = input("Do you want to see more information about this book? (y/n): ").lower().strip()
            if option == 'y':
                return graph.nodes[node_title]
            else:
                print("Okay, no problem!")
            return None
    else:
        print(f"Book '{book_title}' not found in the network.")
        return None

def recommend_books(graph, book_title):
    '''
    Recommends books based on the given book title, allows user to filter by high rating.

    Parameters:
    graph (networkx.Graph): a networkx graph containing the book data
    book_title (str): the title of the book to recommend other books

    Returns:
    list: a list of recommended books in order of popularity (reading log count)
    '''
    if book_title not in graph.nodes:
        print(f"Book '{book_title}' not found in the network.")
        return None
    
    want_high_rating = input("Do you want the recommended books to have a high rating (at least 4 stars)? (y/n): ").lower().strip()
    if want_high_rating not in ['y', 'n']:
        print("Invalid choice. Please enter 'y' or 'n'.")
        return None

    recommended_books = []
    for neighbor in graph.neighbors(book_title):
        if len(set(graph.nodes[book_title]['subjects']).intersection(set(graph.nodes[neighbor]['subjects']))) >=2:
            if want_high_rating == 'y':
                neighbor_rating = graph.nodes[neighbor]['ratings_average']
                if neighbor_rating != 'N/A' and float(neighbor_rating) >= 4:
                    recommended_books.append(neighbor)
            else:
                recommended_books.append(neighbor)
    recommended_books.sort(key=lambda x: graph.nodes[x].get('readinglog_count', 0), reverse=True)

    recommended_books_by_pop = []
    for book in recommended_books:
        count = graph.nodes[book].get('readinglog_count', 'N/A')
        message = f"{book} ({count} people have read/want to read this book)"
        recommended_books_by_pop.append(message)
    return recommended_books_by_pop

def get_book_data(node):
    '''
    Get the book data (star rating, author, subject, and readinglog_count) from the node

    Parameters:
    node (dict): a dictionary containing the book data

    Returns:
    str: the title of the book
    '''
    print("Here's a little more about this book!")
    for key, value in node.items():
        print(f"{key.capitalize()}: {value}")


def main():
    print("Welcome to the NYT Bestsellers Book Network!")
    print("This network contains 50 books that are New York Times Bestsellers.")
    print("Let's explore the network!")

    while True:
        print("\nOptions:")
        print("1. Search for a book")
        print("2. Recommend books based on a book")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            book_node = search_book(G)
            if book_node:
                get_book_data(book_node)
        elif choice == '2':
            book_title = input("Enter the title of the book to recommend other books: ")
            recommended_books = recommend_books(G, book_title)
            if recommended_books:
                print(f"Recommended books based on '{book_title}':")
                for book in recommended_books:
                    print(book)
        elif choice == '3':
            print("Thank you for exploring the network!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()