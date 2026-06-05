import datetime
import os
import re
from pathlib import Path

def _get_svg_files(path: str) -> list[str]:
    svg_files = []
    try:
        for root, _, files in os.walk(path):
            for f in files:
                if Path(f).suffix.lower() == '.svg':
                    svg_files.append(str(Path(root) / f))
    except:
        return []
                
    return svg_files

def render_html_icon_list(dest_path: str, icons_path: str) -> None:
    svg_files = _get_svg_files(icons_path)
    icons_path_to_copy = str(Path(icons_path)).replace('\\', '\\\\') + '\\\\'
    styles = """
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
            color: #333333;
            margin: 30px;
        }

        h1 {
            color: #2c3e50;
            font-size: 24px;
            margin-bottom: 5px;
        }

        h4 {
            color: #7f8c8d;
            font-size: 14px;
            font-weight: normal;
            margin: 5px 0;
        }

        hr {
            border: 0;
            height: 1px;
            background-color: #dcdde1;
            margin: 20px 0 30px 0;
        }

        table, tbody, tr {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            width: 100%;
        }

        td {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            background-color: #ffffff;
            border: 1px solid #e1e8ed;
            border-radius: 8px;
            padding: 15px;
            width: 120px;
            height: 130px;
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
            transition: all 0.2s ease-in-out;
        }

        td:hover {
            background-color: #ffffff;
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            border-color: #3498db;
        }

        td:active {
            transform: translateY(-1px);
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }

        img.svg-icon {
            width: 50px;
            height: 50px;
            object-fit: contain;
            display: block;
            margin: auto;
            pointer-events: none;
        }

        .filename {
            margin-top: 10px;
            font-size: 11px;
            color: #57606f;
            word-break: break-all;
            text-align: center;
            width: 100%;
            line-height: 1.2;
            pointer-events: none;
        }
    """
    
    clipboard_script = """
        function copyToClipboard(element) {
            const text = "{icons_path_to_copy}" + element.querySelector(".filename").innerText;
            navigator.clipboard.writeText(text).then(() => {
                console.log("Copiado: " + text);
                
                const originalColor = element.style.backgroundColor;
                const originalBorder = element.style.borderColor;
                
                element.style.backgroundColor = "#e8f5e9";
                element.style.borderColor = "#2ecc71";
                
                setTimeout(() => {
                    element.style.backgroundColor = originalColor;
                    element.style.borderColor = originalBorder;
                }, 400);
            });
        }
    """.replace('{icons_path_to_copy}', icons_path_to_copy)
    
    filter_script = """
        function filterIconsByTagColor(hexColor) {
            const cells = document.querySelectorAll('td');
            const targetColor = hexColor.toLowerCase();

            cells.forEach(cell => {
                const tags = cell.getAttribute('data-tags') ? cell.getAttribute('data-tags').toLowerCase() : '';
                
                if (tags.includes(targetColor)) {
                    cell.style.display = ''; // Muestra el icono si coincide
                } else {
                    cell.style.display = 'none'; // Lo oculta si no coincide
                }
            });
        }

        function resetColorFilter() {
            document.getElementById('colorPicker').value = '#000000';
            const cells = document.querySelectorAll('td');
            cells.forEach(cell => cell.style.display = '');
        }
    """
    
    html = [
        '<!DOCTYPE html>',
        '<html>',
        '<head>',
        '    <meta charset="UTF-8">',
        '    <title>Listado de SVGs</title>',
        '    <style>',
        f'      {styles}',
        '    </style>',
        '    <script>',
        f'      {clipboard_script}',
        f'      {filter_script}',
        '    </script>',
        '</head>',
        '<body>',
        f'   <h1>Archivos SVG en el directorio "{Path(icons_path)}"</h1>',
        f'   <h4>{len(svg_files)} archivos encontrados.</h4>',
        f'   <h4>Fecha de actualización: [{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]</h4>',
        '    <hr/>',
        '    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 20px; font-family: sans-serif;">',
        '       <label for="colorPicker" style="font-size: 14px; color: #333; cursor: pointer;">Buscar por color:</label>',
        '       <input type="color" id="colorPicker" onchange="filterIconsByTagColor(this.value)" style="border: 1px solid #ccc; width: 40px; height: 30px; cursor: pointer; padding: 0; background: none;">',
        '       <button onclick="resetColorFilter()" style="padding: 6px 12px; font-size: 13px; cursor: pointer;">Mostrar todos</button>',
        '    </div>',
        '    <table>',
        '        <tr>'
    ]
    
    cols_per_row = 6
    count = 0
    
    for svg in svg_files:
        if count > 0 and count % cols_per_row == 0:
            html.append('</tr><tr>')
        
        color_list = []
        with open(svg, 'r') as f:
            svg_content = f.read()
            color_list = extract_hex_colors(svg_content)
            
        color_list_str = ', '.join(color_list)
        html.append(f'<td onclick="copyToClipboard(this)" data-tags="{color_list_str}">')
        html.append(f'<img src="{svg}" class="svg-icon" alt="{Path(svg).name}">')
        html.append(f'<div class="filename">{Path(svg).relative_to(Path(icons_path))}</div>')
        html.append('</td>')
        count += 1
        
    html.append('</tr></table></body></html>')
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))

def extract_hex_colors(input: str) -> list[str]:
    regex_hex = r'#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6})\b'
    coincidencias = re.findall(regex_hex, input)
    return coincidencias