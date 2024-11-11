from lxml import etree
from bs4 import BeautifulSoup
from ebooklib import epub

def create_epub(pages, title, author, include_content_page):
    """
    Creates an EPUB book from additional pages and chapters.

    Parameters:
    - pages: List of dictionaries with keys 'title', 'content', and 'number'.
             Additional pages should have 'number' set to 0 or another value to ensure ordering.
    - title: Title of the book.
    - author: Author of the book.

    Returns:
    - output_file_name: The name of the generated EPUB file.
    """
    # Create an EPUB book
    book = epub.EpubBook()
    
    # Set metadata
    book.set_title(title)
    book.set_language('en')
    book.add_author(author)
    image_nu = epub.EpubImage()
    image_nu.set_content(open("Screenshot (53).png", 'rb').read())
    image_nu.file_name = "images/copywright_nu.png"  # Save with a specific name in EPUB
    book.add_item(image_nu)
    image_sol = epub.EpubImage()
    image_sol.set_content(open("Screenshot (57).png", 'rb').read())
    image_sol.file_name = "images/copywright_sol.png"  # Save with a specific name in EPUB
    book.add_item(image_sol)

    epub_items = []
    toc = []

    # Sort pages based on 'number' to ensure correct order
    sorted_pages = sorted(pages, key=lambda x: x['number'])

    for page in sorted_pages:
        page_title = page.get('title', '').strip()  # Get the title and strip any whitespace
        page_number = page['number']
        html_content = page['content']

        # Parse HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        if page_number == 0:
            # For additional pages like Title Page, use a specific naming convention
            file_name = f'page_{page_title.replace(" ", "_").lower()}.xhtml'
        else:
            file_name = f'chapter_{page_number}.xhtml'

        # Create an EPUB HTML item
        epub_page = epub.EpubHtml(title=page_title, file_name=file_name, lang='en')
        epub_page.content = str(soup)

        # Add page to the book
        book.add_item(epub_page)
        epub_items.append(epub_page)

        # Add to Table of Contents if the title is not empty
        if page_title:
            toc.append(epub.Link(file_name, page_title, file_name))

    # Define Table of Contents
    if include_content_page:
        book.toc = tuple(toc)
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        spine_items = ['nav'] + epub_items
        book.spine = spine_items

        # Write the EPUB file
        output_file_name = f'{title.replace(" ", "_")}.epub'
        epub.write_epub(output_file_name, book, {})
        return output_file_name
    
    else:

        # Add default NCX and Nav files
        book.add_item(epub.EpubNav())
    
        # Define Spine
        spine_items = epub_items
        book.spine = spine_items
    
        # Write the EPUB file
        output_file_name = f'{title.replace(" ", "_")}.epub'
        epub.write_epub(output_file_name, book, {})
        return output_file_name
