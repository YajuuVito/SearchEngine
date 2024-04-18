import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from collections import deque
import json


def crawl(start_url, max_pages):
    queue = deque([(start_url, 0)])  # Queue to store URLs to be crawled

    while queue and len(visited) < max_pages:
        url, parent_id = queue.popleft()
        visited.add(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_id = process_page(url, soup, parent_id)
        visited.add(url)

        # Enqueue child pages
        if len(visited) < max_pages:
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                absolute_url = urljoin(url, href)
                if absolute_url not in visited:
                    queue.append((absolute_url, page_id))


def get_last_modified(url):
    # Send a HEAD request to the URL to retrieve the headers
    response = requests.head(url)

    # Retrieve the Last-Modified header
    last_modified_header = response.headers.get('Last-Modified')

    if last_modified_header:
        # Parse the last modified date from the header
        last_modified_date = datetime.strptime(last_modified_header, '%a, %d %b %Y %H:%M:%S %Z')
        return last_modified_date.strftime('%Y-%m-%d %H:%M:%S')

    return 'Unknown'


def get_page_size(url):
    # Send a HEAD request to the URL to retrieve the headers
    response = requests.head(url)

    # Retrieve the Content-Length header
    content_length_header = response.headers.get('Content-Length')

    if content_length_header:
        # Convert the content length to an integer
        content_length = int(content_length_header)
        return content_length

    return 0


def generate_page_id():
    global page_counter
    page_id = page_counter
    page_counter += 1
    return page_id


def add_link_relation(parent_id, child_id):
    if parent_id == 0:
        # root page
        return
    if parent_id not in file_structure:
        file_structure[parent_id] = []
    file_structure[parent_id].append(child_id)


def process_page(url, soup, parent_id):
    # Extract and store relevant information from the page
    # For example, you can extract the title, content, etc.
    title = soup.title.text
    content = soup.get_text()

    # Retrieve the last modified date of the page
    last_modified = get_last_modified(url)

    # Retrieve the size of the page
    page_size = get_page_size(url)

    # Assign a unique page-ID to the current page
    page_id = generate_page_id()
    page_id_list[page_id] = url

    # Store the parent-child link relation in the file structure
    add_link_relation(parent_id, page_id)

    # Print the URL and title of the processed page
    print("page_id:", page_id)
    print("parent_id:", parent_id)
    print("URL:", url)
    print("Title:", title)
    print("Last Modified:", last_modified)
    print("Size:", page_size, "bytes")
    # print("Content:", content)
    print()

    # 创建一个Python对象
    data = {
        "page_id": page_id,
        "parent_id:": parent_id,
        "URL": url,
        "Title": title,
        "Last Modified": last_modified,
        "Size": page_size,
        "Content": content
    }

    # 将Python对象转换为JSON字符串
    json_data = json.dumps(data)

    # 写入JSON字符串到文件
    with open("data.json", "a") as file:
        file.write(json_data)
        file.write("\n")

    return page_id


# Example usage
start_url = 'https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm'
max_pages = 500
page_counter = 1
visited = set()
file_structure = {}
page_id_list = {}
crawl(start_url, max_pages)

# Print the file structure
print("File Structure:")
for parent_id, child_ids in file_structure.items():
    print("Parent ID:", parent_id, "Parent url:", page_id_list[parent_id])
    print("Child IDs:", child_ids)
    for child_id in child_ids:
        print("Child url:", page_id_list[child_id])
    print()

    data = {
        "Parent_ID": parent_id,
        "Child_IDs": child_ids,
    }

    json_adj_matrix = json.dumps(data)

    with open("adj_matrix.json", "a") as file_adj_matrix:
        file_adj_matrix.write(json_adj_matrix)
        file_adj_matrix.write("\n")
