from pathlib import Path
import os

def generate_others_page_html(heading, text, font_style, heading_font_size, content_font_size):
    # Create HTML content for the Others Page
    html_content = f"""<!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: '{font_style}', sans-serif;
                margin: 0;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                text-align: center;
            }}
            .others {{
                font-size: {content_font_size}px;
                width: 100%;
                max-width: 800px;
                text-align: center;  /* Center the text */
                margin-top: 20px;
            }}
            h1 {{
                font-size: {heading_font_size}px;
                margin: 0;
                text-align: center;  /* Center the heading */
            }}
        </style>
    </head>
    <body>"""
    
    # Include heading only if provided
    if heading.strip():
        html_content += f"""
        <h1>{heading}</h1>"""
    
    html_content += f"""
        <div class="others">
            <p>{text}</p>
        </div>
    </body>
    </html>
    """
    return html_content


def save_others_page_html(html_content, output_dir='temp_pages', file_name='other.xhtml'):

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return file_path