import os
import sys
import markdown

def convert_markdown_to_html(input_dir, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Markdown extensions
    md_extensions = [
        'extra',
        'codehilite',
        'toc',
        'tables',
        'fenced_code'
    ]

    # HTML template parts
    html_prefix = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CTF writeups</title>
    <link rel="stylesheet" href="/css/styles.css">
    <link rel="stylesheet" href="/css/posts.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet">
</head>
<body>
    <!-- Header will be loaded here -->
    <div id="header-placeholder"></div>
    <div class="main-content">
        <div class="container">
'''

    html_suffix = '''
    <!-- Footer will be loaded here -->
        </div>
    </div>
    <div id="footer-placeholder"></div>
    <script src="/js/script.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-json.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-ruby.min.js"></script>
</body>
</html>
'''

    # List all .md files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            input_path = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + '.html'
            output_path = os.path.join(output_dir, output_filename)

            with open(input_path, 'r', encoding='utf-8') as md_file:
                md_content = md_file.read()
                html_body = markdown.markdown(md_content, extensions=md_extensions)

            # Combine everything
            full_html = html_prefix + html_body + html_suffix

            with open(output_path, 'w', encoding='utf-8') as html_file:
                html_file.write(full_html)

            print(f"Converted: {filename} -> {output_filename}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python md_to_html.py <input_directory> <output_directory>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist or is not a directory.")
        sys.exit(1)

    convert_markdown_to_html(input_dir, output_dir)

if __name__ == "__main__":
    main()
