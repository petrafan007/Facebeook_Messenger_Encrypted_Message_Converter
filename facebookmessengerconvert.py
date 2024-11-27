# Facebook Encrypted Message JSON to HTML Converter v1.0 created 11/26/2024
# This file must be placed in the same folder as your unzipped Facebook Messenger JSON files as well as your media folder.
# When this runs, a window will open where you can select the JSON file of the specific person you want to convert or you
# select "Convert all". New files and folders will be created for each person. Enjoy! -Created by Joseph Jay Cavallaro Jr.
# with the help of Microsoft CoPilot and ChatGPT. Please check out my metal bands Edolus and Visions of Reality. Peace!


import json
import os
import codecs
import webbrowser
from datetime import datetime
import html
import re
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to load JSON data
def load_json(file_path):
    with codecs.open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        return json.load(file)

# Function to format timestamps
def format_timestamp(timestamp):
    dt = datetime.fromtimestamp(timestamp / 1000.0)
    formatted_date = dt.strftime('%m/%d/%Y')
    formatted_time = dt.strftime('%I:%M:%S %p')
    return f"{formatted_date} {formatted_time}"

# Function to format reactions
def format_reactions(reactions):
    if not reactions:
        return ''
    return '; '.join(
        [f'{html.escape(reaction["actor"])}: {handle_over_encoded_characters(reaction["reaction"])}' for reaction in reactions]
    )

# Function to make links clickable
def make_links_clickable(text):
    url_pattern = r'(https?://\S+)'
    return re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', text)

# Function to generate the HTML content
def generate_html(messages, media_folder, media_path_prefix):
    html_content = r"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Facebook Messages</title>
        <style>
            body { font-family: Arial, sans-serif; }
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #ddd; padding: 8px; }
            th {
                background-color: #f2f2f2;
                position: sticky;
                top: 0;
                z-index: 1;
            }
            td { background-color: #fff; }
        </style>
    </head>
    <body>
        <h1 style="text-align: center;">Facebook Messages</h1>
        <table>
            <tr>
                <th>Date & Time</th>
                <th>Name</th>
                <th>Reactions</th>
                <th>Message</th>
            </tr>"""

    for message in messages:
        sender = html.escape(message["senderName"])
        timestamp = format_timestamp(message["timestamp"])

        if message["type"] == "text":
            text = handle_over_encoded_characters(message.get("text", ""))
            message_content = make_links_clickable(text)
        else:
            text = html.escape(message.get("text", ""))
            message_content = make_links_clickable(text)

        reactions = format_reactions(message.get("reactions", []))

        media_items = message.get("media", [])
        if media_items:
            for media_item in media_items:
                media_uri = media_item.get("uri", "")
                if media_uri:
                    filename = os.path.basename(media_uri)
                    media_path = os.path.join(media_folder, filename)
                    if os.path.exists(media_path):
                        if media_uri.lower().endswith(('.jpg', '.jpeg', '.png')):
                            message_content += f'<br><img src="{media_path_prefix}/{filename}" alt="{media_uri}" style="max-width: 100%; height: auto;">'
                        elif media_uri.lower().endswith(('.mp4', '.mov')):
                            message_content += f'<br><video controls><source src="{media_path_prefix}/{filename}" type="video/mp4">Your browser does not support the video tag.</video>'
                        elif media_uri.lower().endswith('.wav'):
                            message_content += f'<br><audio controls><source src="{media_path_prefix}/{filename}" type="audio/wav">Your browser does not support the audio tag.</audio>'
                    else:
                        message_content += f'<br>Media file not found: {media_path_prefix}/{filename}'

        html_content += f'''
        <tr>
            <td>{timestamp}</td>
            <td>{sender}</td>
            <td>{reactions}</td>
            <td>{message_content}</td>
        </tr>
        '''

    html_content += r"""</table>
    </body>
    </html>"""

    return html_content

# Function to handle over-encoded characters
def handle_over_encoded_characters(text):
    try:
        text = html.escape(text)
    except UnicodeEncodeError:
        return html.escape(text)
    return text

# Function to copy relevant media files
def copy_media_files(messages, media_folder, dest_media_folder):
    os.makedirs(dest_media_folder, exist_ok=True)
    for message in messages:
        media_items = message.get("media", [])
        if media_items:
            for media_item in media_items:
                media_uri = media_item.get("uri", "")
                if media_uri:
                    filename = os.path.basename(media_uri)
                    src_media_path = os.path.join(media_folder, filename)
                    dest_media_path = os.path.join(dest_media_folder, filename)
                    if os.path.exists(src_media_path):
                        shutil.copy(src_media_path, dest_media_path)

# Function to save HTML file
def save_html_file(messages, media_folder, output_file, media_path_prefix):
    html_content = generate_html(messages, media_folder, media_path_prefix)
    with open(output_file, "w", encoding='utf-8') as file:
        file.write(html_content)

# Function to process a single JSON file
def process_json_file(file_path):
    try:
        # Load JSON and process
        data = load_json(file_path)
        messages = data.get("messages", [])
        if not messages:  # Skip files without messages
            return f"Skipped: No messages found in {file_path}"

        media_folder = os.path.join(os.path.dirname(file_path), "media")
        json_filename = os.path.splitext(os.path.basename(file_path))[0]
        dest_media_folder = os.path.join(os.path.dirname(file_path), f"{json_filename}_media")
        output_file = os.path.join(os.path.dirname(file_path), f"{json_filename}.html")

        # Copy relevant media files
        copy_media_files(messages, media_folder, dest_media_folder)

        # Save HTML file
        save_html_file(messages, dest_media_folder, output_file, f"{json_filename}_media")

        return f"HTML file generated: {output_file}"
    except Exception as e:
        return f"Error processing {file_path}: {str(e)}"

# GUI Application
class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Encrypted Message JSON to HTML Converter")

        # Top label
        label = tk.Label(root, text="Facebook Encrypted Message JSON to HTML Converter", font=("Arial", 14))
        label.pack(pady=10)

        # Convert JSON File button
        self.convert_button = tk.Button(root, text="Convert JSON File", command=self.convert_file, font=("Arial", 12))
        self.convert_button.pack(pady=5)

        # Convert All button
        self.convert_all_button = tk.Button(root, text="Convert All", command=self.convert_all_files, font=("Arial", 12))
        self.convert_all_button.pack(pady=5)

    def convert_file(self):
        # Open file dialog to select the JSON file
        file_path = filedialog.askopenfilename(
            title="Select JSON File",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if file_path:
            result = process_json_file(file_path)
            self.show_results(result)

    def convert_all_files(self):
        directory = filedialog.askdirectory(title="Select Folder")
        if not directory:
            messagebox.showerror("Error", "No folder selected!")
            return

        success_files = []
        skipped_files = []

        for file_name in os.listdir(directory):
            if file_name.endswith(".json"):
                file_path = os.path.join(directory, file_name)
                result = process_json_file(file_path)
                if "HTML file generated" in result:
                    success_files.append(result)
                else:
                    skipped_files.append(result)

        # Display results
        result_message = "Conversion Results:\n\n"
        result_message += "Successfully Converted Files:\n" + "\n".join(success_files) + "\n\n"
        result_message += "Skipped Files:\n" + "\n".join(skipped_files) + "\n\nReason: Files without messages were skipped."
        self.show_results(result_message)

    def show_results(self, result_message):
        # Create a scrollable Toplevel window for results
        results_window = tk.Toplevel(self.root)
        results_window.title("Conversion Results")

        # Create a Text widget with a scrollbar
        text_widget = tk.Text(results_window, wrap=tk.WORD, font=("Arial", 12), width=80, height=25)
        scrollbar = tk.Scrollbar(results_window, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        # Pack the widgets
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Insert results into the Text widget
        text_widget.insert(tk.END, result_message)
        text_widget.configure(state=tk.DISABLED)  # Make the Text widget read-only

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()
