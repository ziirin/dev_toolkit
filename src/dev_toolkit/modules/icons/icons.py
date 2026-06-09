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

        .grid-container {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            width: 100%;
            justify-content: flex-start;
        }

        .icon-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            background-color: #ffffff;
            border: 1px solid #e1e8ed;
            border-radius: 8px;
            padding: 15px;
            flex: 1 1 120px;
            max-width: 160px;
            height: 130px;
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
            transition: all 0.2s ease-in-out;
        }

        .icon-card:hover {
            background-color: #ffffff;
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            border-color: #3498db;
        }

        .icon-card:active {
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
        
        .fixed-tools {
            position: fixed;
            bottom: 25px;
            right: 25px;
            background-color: #ffffff;
            border: 2px solid #3498db; /* Borde de color de énfasis */
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 10px 25px rgba(52, 152, 219, 0.2); /* Sombra con un toque azul */
            display: flex;
            flex-direction: column;
            gap: 12px;
            z-index: 1000;
            min-width: 220px;
        }

        .fixed-tools h5 {
            margin: 0 0 4px 0;
            color: #2c3e50;
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .fixed-tools div {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
        }

        .fixed-tools hr {
            border: 0;
            height: 1px;
            background-color: #e1e8ed;
            margin: 4px 0;
        }
        
        .fixed-tools button {
            padding: 8px 14px;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            border-radius: 6px;
            transition: all 0.2s ease;
        }

        .btn-reset {
            border: 1px solid #dcdde1;
            background-color: #f8f9fa;
            color: #2c3e50;
        }

        .btn-reset:hover {
            background-color: #e1e8ed;
        }

        .btn-scroll {
            border: none;
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: #ffffff;
        }

        .btn-scroll:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(52, 152, 219, 0.3);
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
            const cells = document.querySelectorAll('.icon-card');
            const targetColor = hexColor.toLowerCase();

            cells.forEach(cell => {
                const tags = cell.getAttribute('data-tags') ? cell.getAttribute('data-tags').toLowerCase() : '';
                
                if (tags.includes(targetColor)) {
                    cell.style.display = 'flex'; // Mantiene el formato flex original al mostrarse
                } else {
                    cell.style.display = 'none';
                }
            });
        }

        function resetColorFilter() {
            document.getElementById('colorPicker').value = '#000000';
            const cells = document.querySelectorAll('.icon-card');
            cells.forEach(cell => cell.style.display = 'flex');
        }
        
        function togglePanel(collapse) {
            const content = document.getElementById('panelContent');
            const btnFold = document.getElementById('btnFold');
            const btnUnfold = document.getElementById('btnUnfold');
            const panel = document.getElementById('fixedToolsPanel');

            if (collapse) {
                content.style.display = 'none';
                btnFold.style.display = 'none';
                btnUnfold.style.display = 'block';
                panel.style.minWidth = 'auto';
                panel.style.padding = '10px';
            } else {
                content.style.display = 'flex';
                btnFold.style.display = 'block';
                btnUnfold.style.display = 'none';
                panel.style.minWidth = '220px';
                panel.style.padding = '20px';
            }
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
        '    <div class="fixed-tools" id="fixedToolsPanel">',
        '       <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 5px; width: 100%;">',
        '           <h5 style="margin: 0;">Panel de Filtros</h5>',
        '           <button onclick="togglePanel(true)" id="btnFold" style="padding: 2px 6px; font-size: 11px; cursor: pointer; border: 1px solid #dcdde1; background: #f8f9fa; border-radius: 4px;">▼ Plegar</button>',
        '       </div>',
        '       <div id="panelContent" style="display: flex; flex-direction: column; gap: 12px; width: 100%;">',
        '           <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px;">',
        '               <label for="colorPicker" style="font-size: 13px; color: #57606f; font-weight: 500; cursor: pointer;">Filtrar por color:</label>',
        '               <input type="color" id="colorPicker" onchange="filterIconsByTagColor(this.value)" style="border: 1px solid #ccc; width: 45px; height: 32px; cursor: pointer; padding: 0; background: none; border-radius: 4px;">',
        '           </div>',
        '           <button class="btn-reset" onclick="resetColorFilter()">Mostrar todos</button>',
        '           <hr/>',
        '           <button class="btn-scroll" onclick="window.scrollTo({top: 0, behavior: \'smooth\'})">▲ Volver arriba</button>',
        '       </div>',
        '       <button onclick="togglePanel(false)" id="btnUnfold" style="display: none; padding: 6px 12px; font-size: 13px; font-weight: 600; cursor: pointer; border: none; background: #3498db; color: white; border-radius: 6px; width: 100%;">☰ Abrir Filtros</button>',
        '    </div>',
        '    <div class="grid-container">'
    ]
    
    for svg in svg_files:
        color_list = []
        
        with open(svg, 'r') as f:
            svg_content = f.read()
            color_list = extract_hex_colors(svg_content)
            
        color_list_str = ', '.join(color_list)
        html.append(f'    <div class="icon-card" onclick="copyToClipboard(this)" data-tags="{color_list_str}">')
        html.append(f'        <img src="{svg}" class="svg-icon" alt="{Path(svg).name}">')
        html.append(f'        <div class="filename">{Path(svg).relative_to(Path(icons_path))}</div>')
        html.append('    </div>')
    
    html.append('    </div>\n</body>\n</html>')
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))

def extract_hex_colors(input: str) -> list[str]:
    regex_hex = r'#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6})\b'
    coincidencias = re.findall(regex_hex, input)
    return coincidencias