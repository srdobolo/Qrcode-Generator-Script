import re

def update_static_references(html_content):
    # Pattern to find href or src attributes with static file paths
    pattern = r'(href|src)=["\'](css|js|images)/([^"\']+)["\']'

    # Replacement function to use url_for
    def replacer(match):
        attr = match.group(1)
        folder = match.group(2)
        filename = match.group(3)
        return f'{attr}="{{{{ url_for(\'static\', filename=\'{folder}/{filename}\') }}}}"'

    updated_html = re.sub(pattern, replacer, html_content)
    
    # Also update inline style background-image url
    style_pattern = r'url\(([^)]+)\)'
    def style_replacer(match):
        url = match.group(1).strip('"\'')
        if url.startswith('css/') or url.startswith('js/') or url.startswith('images/'):
            return f"url('{{{{ url_for('static', filename='{url}') }}}}')"
        return match.group(0)

    updated_html = re.sub(style_pattern, style_replacer, updated_html)

    return updated_html

# Example usage: read your HTML file, update, and save
input_file = 'templates/index.html'  # Change to your actual file path if needed
output_file = 'templates/index_updated.html'  # Or use the same as input_file to overwrite

with open(input_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

updated_html = update_static_references(html_content)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(updated_html)

print(f"Updated HTML written to {output_file}")
