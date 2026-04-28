import datetime
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
    html = [
        '<!DOCTYPE html>',
        '<html>',
        '<head>',
        '    <meta charset="UTF-8">',
        '    <title>Listado de SVGs</title>',
        '    <style>',
        '        table { border-collapse: collapse; }',
        '        /* Estilo actualizado con cursor pointer y transición */',
        '        td { text-align: center; padding: 15px; vertical-align: top; cursor: pointer; transition: background 0.2s; border-radius: 5px; }',
        '        td:hover { background-color: #f0f0f0; }',
        '        td:active { background-color: #e0e0e0; }',
        '        img.svg-icon { width: 64px; height: 64px; display: block; margin: 0 auto; pointer-events: none; }',
        '        .filename { margin-top: 8px; font-size: 12px; word-break: break-word; max-width: 100px; pointer-events: none; }',
        '    </style>',
        '    <script>',
        '        function copyToClipboard(element) {',
        '            const text = element.querySelector(".filename").innerText;',
        '            navigator.clipboard.writeText(text).then(() => {',
        '                console.log("Copiado: " + text);',
        '                // Opcional: feedback visual simple',
        '                const originalColor = element.style.backgroundColor;',
        '                element.style.backgroundColor = "#c8e6c9";',
        '                setTimeout(() => element.style.backgroundColor = originalColor, 300);',
        '            });',
        '        }',
        '    </script>',
        '</head>',
        '<body>',
        f'    <h1>Archivos SVG en el directorio "{icons_path}"</h1>',
        f'    <h4>{len(svg_files)} archivos encontrados.</h4>',
        f'    <h4>Fecha de actualización: [{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]</h4>',
        '    <hr/>',
        '    <table>',
        '        <tr>'
    ]
    
    cols_per_row = 6
    count = 0
    
    for svg in svg_files:
        if count > 0 and count % cols_per_row == 0:
            html.append('</tr><tr>')
        
        # Añadimos el evento onclick que llama a la función JS
        html.append('<td onclick="copyToClipboard(this)">')
        html.append(f'<img src="{svg}" class="svg-icon" alt="{Path(svg).name}">')
        html.append(f'<div class="filename">{Path(svg).name}</div>')
        html.append('</td>')
        count += 1
        
    html.append('</tr></table></body></html>')
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))