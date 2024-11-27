from PIL import Image  # Add this at the top of your file
import base64
from io import BytesIO

def generate_copyright_page_html(author_name, typesetter_name, printer_name, press_name, year, isbn, up_file):
    
    if press_name == "Nu Voice Press":
        base_img_data = ""
        if up_file != '':  # With uploaded file
            file_bytes = up_file.read()
            with open(f"./temp_{up_file.name}", "wb") as f:
                f.write(file_bytes)
            base_img = Image.open(f"./temp_{up_file.name}")
            
            # Convert image to Base64
            buffered = BytesIO()
            base_img.save(buffered, format="PNG")  # Save as PNG format
            base_img_data = base64.b64encode(buffered.getvalue()).decode("utf-8")
            uploaded_image_tag = (f'<img src="data:image/png;base64,{base_img_data}" alt="Uploaded Image" class="uploaded-image"/><br/>' 
                                  if base_img_data else "")
            
            html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Helvetica', sans-serif;
                text-align: center;
            }}
            .copyright {{
                margin: 20px;
            }}
            .logo {{
                width: 200px;  /* Increase width */
                height: auto;  /* Maintain aspect ratio */
            }}
            .uploaded-image {{
                max-width: 100%;
                height: auto;
            }}
        </style>
    </head>
    <body>
        <div class="copyright">
            <img src="images/copywright_nu.png" alt="Logo" class="logo"/><br/>
            <p>Copyright © {author_name} {year}</p>
            <p>The moral rights of the author have been asserted. Database right NU VOICE PRESS (maker).</p>
            <p>This is a work of fiction, and all characters and incidents described in this book are the product of the author's imagination. Any resemblance to actual persons, living or dead, is entirely coincidental.</p>
            <p>All rights reserved. Enquiries concerning reproduction outside the scope of the above should be sent to NU VOICE PRESS at the address above.</p>
            <p>ISBN: {isbn}</p>
            <p>Typeset by {typesetter_name}</p>
            <p>Printed at {printer_name}</p>
            <p>Published by Nu Voice Press</p>
            {uploaded_image_tag}
        </div>
    </body>
    </html>
    """
        else:  # Without uploaded file
            html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Helvetica', sans-serif;
                text-align: center;
            }}
            .copyright {{
                margin: 20px;
            }}
            .logo {{
                width: 200px;  /* Increase width */
                height: auto;  /* Maintain aspect ratio */
            }}
        </style>
    </head>
    <body>
        <div class="copyright">
            <img src="images/copywright_nu.png" alt="Logo" class="logo"/><br/>
            <p>Copyright © {author_name} {year}</p>
            <p>The moral rights of the author have been asserted. Database right NU VOICE PRESS (maker).</p>
            <p>This is a work of fiction, and all characters and incidents described in this book are the product of the author's imagination. Any resemblance to actual persons, living or dead, is entirely coincidental.</p>
            <p>All rights reserved. Enquiries concerning reproduction outside the scope of the above should be sent to NU VOICE PRESS at the address above.</p>
            <p>ISBN: {isbn}</p>
            <p>Typeset by {typesetter_name}</p>
            <p>Printed at {printer_name}</p>
            <p>Published by Nu Voice Press</p>
        </div>
    </body>
    </html>
    """
    else:  # Solomon Press
        base_img_data = ""
        if up_file:  # With uploaded file
            
            file_bytes = up_file.read()
            with open(f"./temp_{up_file.name}", "wb") as f:
                f.write(file_bytes)
            base_img = Image.open(f"./temp_{up_file.name}")
            
            # Convert image to Base64
            buffered = BytesIO()
            base_img.save(buffered, format="PNG")  # Save as PNG format
            base_img_data = base64.b64encode(buffered.getvalue()).decode("utf-8")
            uploaded_image_tag = (f'<img src="data:image/png;base64,{base_img_data}" alt="Uploaded Image" class="uploaded-image"/><br/>' 
                                  if base_img_data else "")
            
            html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Helvetica', sans-serif;
                text-align: center;
            }}
            .copyright {{
                margin: 20px;
            }}
            .logo {{
                width: 180px;  /* Increase width */
                height: auto;  /* Maintain aspect ratio */
            }}
            .uploaded-image {{
                max-width: 100%;
                height: auto;
            }}
        </style>
    </head>
    <body>
        <div class="copyright">
            <img src="images/copywright_sol.png" alt="Logo" class="logo"/><br/>
            <p>Copyright © {author_name} {year}</p>
            <p>This is a work of fiction, and all characters and incidents described in this book are the product of the author's imagination. Any resemblance to actual persons, living or dead, is entirely coincidental.</p>
            <p>All rights reserved. Enquiries concerning reproduction outside the scope of the above should be sent to Solomon Press at the below address.</p>
            <p>Address : Unit-125, First floor, Vipul Trade Centre, Sector-48, Sohna Road, South City-2 Gurugram, Haryana,122018.</p>
            <p>ISBN: {isbn}</p>
            <p>Typeset by {typesetter_name}</p>
            <p>Printed at {printer_name}</p>
            <p>Published by Solomon Press {year}</p>
            {uploaded_image_tag}
        </div>
    </body>
    </html>
    """
        else:  # Without uploaded file
            html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Helvetica', sans-serif;
                text-align: center;
            }}
            .copyright {{
                margin: 20px;
            }}
            .logo {{
                width: 180px;  /* Increase width */
                height: auto;  /* Maintain aspect ratio */
            }}
        </style>
    </head>
    <body>
        <div class="copyright">
            <img src="images/copywright_sol.png" alt="Logo" class="logo"/><br/>
            <p>Copyright © {author_name} {year}</p>
            <p>This is a work of fiction, and all characters and incidents described in this book are the product of the author's imagination. Any resemblance to actual persons, living or dead, is entirely coincidental.</p>
            <p>All rights reserved. Enquiries concerning reproduction outside the scope of the above should be sent to Solomon Press at the below address.</p>
            <p>Address : Unit-125, First floor, Vipul Trade Centre, Sector-48, Sohna Road, South City-2 Gurugram, Haryana,122018.</p>
            <p>ISBN: {isbn}</p>
            <p>Typeset by {typesetter_name}</p>
            <p>Printed at {printer_name}</p>
            <p>Published by Solomon Press {year}</p>
        </div>
    </body>
    </html>
    """
    return html_content

def save_copyright_page_html(html_content):
    # Save the generated HTML content to a temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode='w', encoding='utf-8') as f:
        f.write(html_content)
        return f.name