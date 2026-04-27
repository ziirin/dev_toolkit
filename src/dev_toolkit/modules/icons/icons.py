import os
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
    html = ['<!DOCTYPE html>',
            '<html>',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <title>Listado de SVGs</title>',
            '    <style>',
            '        table { border-collapse: collapse; }',
            '        td { text-align: center; padding: 15px; vertical-align: top; }',
            '        img.svg-icon { width: 64px; height: 64px; display: block; margin: 0 auto; }',
            '        .filename { margin-top: 8px; font-size: 12px; word-break: break-word; max-width: 100px; }',
            '    </style>',
            '</head>',
            '<body>',
            '    <h1>Archivos SVG en el directorio y subdirectorios</h1>',
            '    <table>',
            '        <tr>']
    
    cols_per_row = 6
    count = 0
    
    for svg in svg_files:
        if count > 0 and count % cols_per_row == 0:
            html.append('</tr><tr>')
        html.append('<td>')
        html.append(f'<img src="{svg}" class="svg-icon" alt="{Path(svg).name}">')
        html.append(f'<div class="filename">{Path(svg).name}</div>')
        html.append('</td>')
        count += 1
        
    html.append('</tr></table></body></html>')
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(''.join(html))