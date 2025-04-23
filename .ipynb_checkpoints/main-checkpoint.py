from PIL import Image  # Add this at the top of your file
import base64
from io import BytesIO
from lxml import etree
from bs4 import BeautifulSoup
from ebooklib import epub

def create_epub(pages, title, author, include_content_page, up_file):
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
    image_sol = epub.EpubImage()
    image_sol.set_content(open("Screenshot (57).png", 'rb').read())
    image_sol.file_name = "images/copywright_sol.png"  # Save with a specific name in EPUB
    book.add_item(image_sol)
    book.add_item(image_nu)

    if up_file:
        try:
            # Read the uploaded file content
            file_content = up_file.read()
            
            # Create a temporary file
            temp_path = f"temp_{up_file.name}"
            with open(temp_path, "wb") as f:
                f.write(file_content)
            
            # Open and verify the image
            with Image.open(temp_path) as img:
                # Convert to PNG format
                output_buffer = BytesIO()
                img.save(output_buffer, format="PNG")
                image_content = output_buffer.getvalue()
            
            # Add to epub
            image_up = epub.EpubItem(
                uid="image_up",
                file_name="images/up.png",
                media_type="image/png",
                content=image_content
            )
            book.add_item(image_up)
            
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
        except Exception as e:
            print(f"Error processing uploaded image: {e}")

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
