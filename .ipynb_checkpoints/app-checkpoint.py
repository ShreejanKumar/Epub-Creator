from title_page import generate_title_page_html, save_title_page_html
from copywright import generate_copyright_page_html, save_copyright_page_html
from others import generate_others_page_html, save_others_page_html
import streamlit as st
from main import create_epub
import os

st.title("EPUB Creator")

# Book Details Inputs
book_title = st.text_input("Book Title", value="My Book Title")
author = st.text_input("Author", value="Author Name")
num_chapters = st.number_input('How many chapters do you want to add?', min_value=1, max_value=50, step=1, value=1)

fonts = ["Helvetica", "Helvetica-Bold", "Courier", "Times-Roman"]

additional_pages_options = ["Title Page", "Copyright Page", "Others"]
selected_pages = st.multiselect("Select additional pages to include:", additional_pages_options)

additional_pages = []

# Handle Title Page
if "Title Page" in selected_pages:
    with st.expander("Title Page Details"):
        st.subheader("Title Page Configuration")
        tp_title = st.text_input("Title (for Title Page)", value=book_title, key="tp_title")
        tp_subtitle = st.text_input("Subtitle (optional)", value="", key="tp_subtitle")  # Make subtitle optional
        tp_author = st.text_input("Author Name (optional)", value="", key="tp_author")  # Make author optional
        
        # Use sliders for font sizes
        tp_title_font_size = st.slider(
            "Title Font Size",
            min_value=20,
            max_value=100,
            step=2,
            value=36,
            key="tp_title_font_size"
        )
        tp_subtitle_font_size = st.slider(
            "Subtitle Font Size",
            min_value=14,
            max_value=50,
            step=2,
            value=24,
            key="tp_subtitle_font_size"
        )
        tp_author_font_size = st.slider(
            "Author Name Font Size",
            min_value=14,
            max_value=50,
            step=2,
            value=20,
            key="tp_author_font_size"
        )
        
        tp_font_style = st.selectbox(
            "Font Style for Title Page:",
            fonts,
            index=0,
            key="tp_font_style"
        )

        # Append Title Page details to additional_pages
        title_page_content = {
            'title': tp_title,
            'title_font_size': tp_title_font_size,
            'font_style': tp_font_style
        }

        # Include subtitle only if it is provided
        if tp_subtitle.strip():  # Check if the subtitle is not empty
            title_page_content['subtitle'] = tp_subtitle
            title_page_content['subtitle_font_size'] = tp_subtitle_font_size

        # Include author only if it is provided
        if tp_author.strip():  # Check if the author is not empty
            title_page_content['author'] = tp_author
            title_page_content['author_font_size'] = tp_author_font_size
        
        additional_pages.append({
            'type': 'Title Page',
            'content': title_page_content
        })

if "Copyright Page" in selected_pages:
    with st.expander("Copyright Page Details"):
        st.subheader("Copyright Page Configuration")
        cp_author_name = st.text_input("Author Name", value=author, key="cp_author_name")
        cp_typesetter_name = st.text_input("Typesetter Name", value="Typesetter Name", key="cp_typesetter_name")
        cp_printer_name = st.text_input("Printer Name", value="Printer Name", key="cp_printer_name")
        
        # Append Copyright Page details to additional_pages
        additional_pages.append({
            'type': 'Copyright Page',
            'content': {
                'author_name': cp_author_name,
                'typesetter_name': cp_typesetter_name,
                'printer_name': cp_printer_name,
            }
        })

if "Others" in selected_pages:
    with st.expander("Others Page Details"):
        st.subheader("Others Page Configuration")
        
        # Get heading and content from the user
        others_heading = st.text_input("Page Heading", value="Custom Page Heading", key="others_heading")
        others_content = st.text_area("Page Content", value="This is the content for the others page.", height=200, key="others_content")

        # Get font style and sizes
        others_font_style = st.selectbox("Font Style for Others Page:", fonts, key="others_font_style")
        others_heading_font_size = st.slider(
            "Heading Font Size",
            min_value=20,
            max_value=100,
            step=2,
            value=36,
            key="others_heading_font_size"
        )
        others_content_font_size = st.slider(
            "Content Font Size",
            min_value=14,
            max_value=50,
            step=2,
            value=20,
            key="others_content_font_size"
        )

        # Append Others Page details to additional_pages
        additional_pages.append({
            'type': 'Others Page',
            'content': {
                'heading': others_heading,
                'text': others_content,
                'font_style': others_font_style,
                'heading_font_size': others_heading_font_size,
                'content_font_size': others_content_font_size
            }
        })


st.header("Upload Chapter Files")
chapter_html = []
chapter_title = []

for i in range(num_chapters):
    st.subheader(f"Chapter {i + 1}")
    file = st.file_uploader(f"Upload HTML file for Chapter {i + 1}", type="html", key=f"file_{i}")
    if file is not None:
        # Use the .read() method to get the content from the uploaded file (BytesIO)
        html_content = file.read().decode('utf-8')  # Decode from bytes to string
        chapter_html.append(html_content)
    t = st.text_input("Chapter Title", key=f"chp_title_{i}")
    chapter_title.append(t)
    



if st.button("Create EPUB"):
    # Validate inputs
    missing_fields = []
    if not book_title:
        missing_fields.append("Book Title")

    # Validate additional pages if necessary
    for page in additional_pages:
        if page['type'] == 'Title Page':
            content = page['content']
            if not content['title']:
                missing_fields.append("Title for Title Page")
            # No need to check subtitle and author presence as they are optional
        elif page['type'] == 'Copyright Page':
            content = page['content']
            if not content['author_name']:
                missing_fields.append("Author Name for Copyright Page")
            if not content['typesetter_name']:
                missing_fields.append("Typesetter Name for Copyright Page")
            if not content['printer_name']:
                missing_fields.append("Printer Name for Copyright Page")
        elif page['type'] == 'Others Page':
            content = page['content']
            if not content['heading']:
                missing_fields.append("Heading for Others Page")
            if not content['text']:
                missing_fields.append("Content for Others Page")
            if not content['font_style']:
                missing_fields.append("Font Style for Others Page")
            if not content['heading_font_size']:
                missing_fields.append("Heading Font Size for Others Page")
            if not content['content_font_size']:
                missing_fields.append("Content Font Size for Others Page")

    if missing_fields:
        st.error(f"Please fill in the following fields: {', '.join(missing_fields)}")
    else:
        with st.spinner('Generating EPUB...'):
            try:
                # List to hold processed pages (additional pages first)
                processed_pages = []

                # Handle additional pages first
                for page in additional_pages:
                    if page['type'] == 'Title Page':
                        content = page['content']
                        html_content = generate_title_page_html(
                            title=content['title'],
                            subtitle=content.get('subtitle', ''),  # Use .get() to avoid KeyError
                            author=content.get('author', ''),  # Use .get() to avoid KeyError
                            title_font_size=content['title_font_size'],
                            subtitle_font_size=content.get('subtitle_font_size', 0),  # Default to 0 if not provided
                            author_font_size=content.get('author_font_size', 0),  # Default to 0 if not provided
                            font_style=content['font_style']
                        )
                        html_path = save_title_page_html(html_content)
                        processed_pages.append({
                            'title': 'Title Page',
                            'content': html_content,
                            'number': 0  # Ensures it's first
                        })
                    elif page['type'] == 'Copyright Page':
                        content = page['content']
                        html_content = generate_copyright_page_html(
                            author_name=content['author_name'],
                            typesetter_name=content['typesetter_name'],
                            printer_name=content['printer_name']
                        )
                        html_path = save_copyright_page_html(html_content)
                        processed_pages.append({
                            'title': 'Copyright Page',
                            'content': html_content,
                            'number': 1  # Ensures it's second
                        })
                    elif page['type'] == 'Others Page':
                        content = page['content']
                        html_content = generate_others_page_html(
                            heading=content['heading'],
                            text=content['text'],
                            font_style=content['font_style'],
                            heading_font_size=content['heading_font_size'],
                            content_font_size=content['content_font_size']
                        )
                        html_path = save_others_page_html(html_content)
                        processed_pages.append({
                            'title': content['heading'],
                            'content': html_content,
                            'number': 2
                        })
                for i in range(num_chapters):
                    processed_pages.append({
                        'title': chapter_title[i],
                        'content': chapter_html[i],
                        'number': 2 + i })

                # Create EPUB with all pages
                output_file = create_epub(processed_pages, book_title, author)
                st.success(f"EPUB created successfully: {output_file}")

                # Provide a download button for the EPUB
                with open(output_file, "rb") as epub_file:
                    st.download_button(
                        label="Download EPUB",
                        data=epub_file,
                        file_name=output_file,
                        mime="application/epub+zip"
                    )

            except Exception as e:
                st.error(f"An error occurred: {e}")