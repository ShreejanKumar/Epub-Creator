import streamlit as st
from title_page import generate_title_page_html, save_title_page_html
from copywright import generate_copyright_page_html, save_copyright_page_html
from others import generate_others_page_html, save_others_page_html
from main import create_epub
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setup Google Sheets API client using credentials from secrets
def get_gspread_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Access the credentials from the Streamlit secrets
    creds_dict = {
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"],
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"]
    }

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    return client

# Access the Google Sheet
def get_google_sheet(client, spreadsheet_url):
    sheet = client.open_by_url(spreadsheet_url).sheet1  # Opens the first sheet
    return sheet

# Read the password from the first cell
def read_password_from_sheet(sheet):
    password = sheet.cell(1, 1).value  # Reads the first cell (A1)
    return password

# Update the password in the first cell
def update_password_in_sheet(sheet, new_password):
    sheet.update_cell(1, 1, new_password)  # Updates the first cell (A1) with the new password

# Initialize gspread client and access the sheet
client = get_gspread_client()
sheet = get_google_sheet(client, st.secrets["spreadsheet"])

# Read the password from the Google Sheet
PASSWORD = read_password_from_sheet(sheet)

# Initialize session state for authentication and password reset
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'password' not in st.session_state:
    st.session_state['password'] = PASSWORD
if 'reset_mode' not in st.session_state:
    st.session_state['reset_mode'] = False

# Function to check password
def check_password(password):
    return password == st.session_state['password']

# Password reset function
def reset_password(new_password, confirm_password):
    if new_password != confirm_password:
        st.error("Passwords do not match!")
    else:
        # Update the password both in session state and in Google Sheets
        st.session_state['password'] = new_password
        update_password_in_sheet(sheet, new_password)
        st.session_state['reset_mode'] = False
        st.success("Password reset successfully!")

# Authentication block
if not st.session_state['authenticated']:
    st.title("Login to EPUB Creator")

    # Input password
    password_input = st.text_input("Enter Password", type="password")
    
    if st.button("Login"):
        if check_password(password_input):
            st.session_state['authenticated'] = True
            st.success("Login successful!")
        else:
            st.error("Incorrect password!")

    # Link to reset password
    if st.button("Reset Password?"):
        st.session_state['reset_mode'] = True

# Reset password block
if st.session_state['reset_mode']:
    st.title("Reset Password")

    old_password = st.text_input("Enter Old Password", type="password")
    new_password = st.text_input("Enter New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")
    
    if st.button("Reset Password"):
        if old_password == st.session_state['password']:
            reset_password(new_password, confirm_password)
        else:
            st.error("Incorrect old password!")
    
    # Go back to login
    if st.button("Back to Login"):
        st.session_state['reset_mode'] = False

if st.session_state['authenticated'] and not st.session_state['reset_mode']:

    st.title("EPUB Creator")
    
    # Book Details Inputs
    book_title = st.text_input("Book Title", value="My Book Title")
    author = st.text_input("Author", value="Author Name")
    num_chapters = st.number_input('How many chapters do you want to add?', min_value=1, step=1, value=1)
    include_content_page = st.checkbox("Include Content Page", value=True)
    
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
            cp_press_name = st.selectbox("Press Name", options=["Nu Voice Press", "Solomon Press"], key="cp_press_name")
            cp_year = st.text_input("Year", value="Year", key="cp_year")
            cp_isbn = st.text_input("ISBN", value="Isbn", key="cp_isbn")
            
            # Append Copyright Page details to additional_pages
            additional_pages.append({
                'type': 'Copyright Page',
                'content': {
                    'author_name': cp_author_name,
                    'typesetter_name': cp_typesetter_name,
                    'printer_name': cp_printer_name,
                    'press_name': cp_press_name,
                    'year': cp_year,
                    'isbn': cp_isbn
                }
            })
    
    if "Others" in selected_pages:
        with st.expander("Others Page Details"):
            st.subheader("Others Page Configuration")
            num_others = st.number_input("Number of Others Pages", min_value=1, max_value=10, value=1)
            # Get heading and content from the user
            for i in range(num_others):
                others_heading = st.text_input(f"Page Heading {i+1} (optional)", value="", key=f"others_heading_{i}")
                others_content = st.text_area(f"Page Content {i+1}", value="This is the content for the others page.", height=200, key=f"others_content_{i}")
        
                # Get font style and sizes
                others_font_style = st.selectbox(f"Font Style for Others Page {i+1}:", fonts, key=f"others_font_style_{i}")
                others_heading_font_size = st.slider(
                    f"Heading Font Size (optional) {i+1}",  # Indicating it's optional
                    min_value=20,
                    max_value=100,
                    step=2,
                    value=36,
                    key=f"others_heading_font_size_{i}"
                )
                others_content_font_size = st.slider(
                    f"Content Font Size {i+1}",
                    min_value=14,
                    max_value=50,
                    step=2,
                    value=20,
                    key=f"others_content_font_size_{i}"
                )
        
                # Append Others Page details to additional_pages
                additional_pages.append({
                    'type': 'Others Page',
                    'content': {
                        'heading': others_heading,  # Will pass empty string if not provided
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
                if not content['press_name']:
                    missing_fields.append("Press Name for Copyright Page")
                if not content['year']:
                    missing_fields.append("Year for Copyright Page")
                if not content['isbn']:
                    missing_fields.append("ISBN for Copyright Page")
            elif page['type'] == 'Others Page':
                content = page['content']
                if not content['text']:
                    missing_fields.append("Content for Others Page")
                if not content['font_style']:
                    missing_fields.append("Font Style for Others Page")
                if not content['content_font_size']:
                    missing_fields.append("Content Font Size for Others Page")
    
        if missing_fields:
            st.error(f"Please fill in the following fields: {', '.join(missing_fields)}")
        else:
            with st.spinner('Generating EPUB...'):
                try:
                    # List to hold processed pages (additional pages first)
                    processed_pages = []
    
                    # Initialize a counter for page numbering
                    page_number = 0
                    
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
                                'number': page_number  # Set to current page number
                            })
                            page_number += 1  # Increment page number
                    
                        elif page['type'] == 'Copyright Page':
                            content = page['content']
                            html_content = generate_copyright_page_html(
                                author_name=content['author_name'],
                                typesetter_name=content['typesetter_name'],
                                printer_name=content['printer_name'],
                                press_name=content['press_name'],
                                year = content['year'],
                                isbn = content['isbn']
                            )
                            html_path = save_copyright_page_html(html_content)
                            processed_pages.append({
                                'title': 'Copyright Page',
                                'content': html_content,
                                'number': page_number  # Set to current page number
                            })
                            page_number += 1  # Increment page number
                    
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
                                'number': page_number  # Set to current page number
                            })
                            page_number += 1  # Increment page number
                    
                    # Now add the chapters
                    for i in range(num_chapters):
                        processed_pages.append({
                            'title': chapter_title[i],
                            'content': chapter_html[i],
                            'number': page_number  # Continue numbering from where we left off
                        })
                        page_number += 1  # Increment page number for the next chapter
    
                    # Create EPUB with all pages
                    output_file = create_epub(processed_pages, book_title, author, include_content_page)
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