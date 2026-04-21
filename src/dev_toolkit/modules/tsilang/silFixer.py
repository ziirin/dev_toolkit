import os
import csv
import argparse
from pathlib import Path

# ========================================================================

# Delimitadores y otros
SIL_ID_DELIMITER            = '='
SIL_DELIMITER               = '~!@#'
CSV_DELIMITER               = ';'
NEW_LINE                    = '\n'

# Identificador de idioma
LANG_ES                     = 'SPANISH'
LANG_EN                     = 'ENGLISH'
LANG_IT                     = 'ITALIAN'
LANG_ZHt                    = 'TRADITIONAL_CHINESE'
LANG_ZHs                    = 'SIMPLIFIED_CHINESE'
LANG_TR                     = 'TURKISH'
LANG_FR                     = 'FRENCH'
LANG_RU                     = 'RUSSIAN'
LANG_PT                     = 'PORTUGUESE'
LANG_EL                     = 'GREEK'
LANG_DE                     = 'GERMAN'

LANGUAGES = {
    LANG_ES: {
        'charset': 'ANSI_CHARSET',
        'font': 'Tahoma',
        'index': 0
    },
    LANG_EN: {
        'charset': 'DEFAULT_CHARSET',
        'font': 'Tahoma',
        'index': 1
    },
    LANG_IT: {
        'charset': 'DEFAULT_CHARSET',
        'font': 'Tahoma',
        'index': 2
    },
    LANG_ZHt: {
        'charset': 'CHINESEBIG5_CHARSET',
        'font': 'Tahoma',
        'index': 3
    },
    LANG_ZHs: {
        'charset': 'GB2312_CHARSET',
        'font': 'Tahoma',
        'index': 4
    },
    LANG_TR: {
        'charset': 'TURKISH_CHARSET',
        'font': 'Tahoma',
        'index': 5
    },
    LANG_FR: {
        'charset': 'ANSI_CHARSET',
        'font': 'Tahoma',
        'index': 6
    },
    LANG_RU: {
        'charset': 'RUSSIAN_CHARSET',
        'font': 'Tahoma',
        'index': 7
    },
    LANG_PT: {
        'charset': 'DEFAULT_CHARSET',
        'font': 'Tahoma',
        'index': 8
    },
    LANG_EL: {
        'charset': 'GREEK_CHARSET',
        'font': 'Tahoma',
        'index': 9
    },
    LANG_DE: {
        'charset': 'ANSI_CHARSET',
        'font': 'Tahoma',
        'index': 10
    },
}

# Categorías en archivos SILs
SIL_CATEGORY_CAPTIONS       = '[Captions]'
SIL_CATEGORY_CHARSET        = '[CharSets]' # No contiene traducciones
SIL_CATEGORY_COLLECTIONS    = '[Collections]'
SIL_CATEGORY_DIALOGS        = '[Dialogs]'
SIL_CATEGORY_EXTENDED       = '[Extended]' # Contiene traducciones pero cuidado con IsSubComponent y TypeKind
SIL_CATEGORY_FONTS          = '[Fonts]' # No contiene traducciones
SIL_CATEGORY_HINTS          = '[Hints]'
SIL_CATEGORY_LANG_NAMES     = '[Language names - for internal use only!]' # No contiene traducciones
SIL_CATEGORY_MULTILINES     = '[Multilines]'
SIL_CATEGORY_OPTIONS        = '[OPTIONS]' # No contiene traducciones
SIL_CATEGORY_OTHER          = '[Other]'
SIL_CATEGORY_STRINGS        = '[Strings]'

# ========================================================================

def get_lang_names() -> list[str]:
    return [lang for lang in sorted(LANGUAGES.keys(), key=lambda _key: LANGUAGES[_key]['index'])]

def read_sil(sil_path: str, lang_list: list[str]) -> tuple[dict, dict]:
    sil_data = {}
    errors = {}
    
    try:
        with open(sil_path, 'r', encoding='utf-8') as sil_file:
            lines = sil_file.readlines()
            
            cur_category = ''
            for (idx, line) in enumerate(lines):
                if line.endswith(NEW_LINE):
                    line = line[:-1]
                
                # Líneas de categorías
                if line.startswith('[') and line.endswith(']'):
                    cur_category = line[0:line.find(']') + 1]
                    sil_data[cur_category] = []
                    continue
                # Líneas vacías
                if line == '\ufeff' or not line:
                    continue
                
                # Si se encuentran traducciones antes de la aparición de cualquier categoría
                # Ej. [Captions]
                if not cur_category:
                    errors[idx] = 'ERR. Esta traducción no pertenece a ninguna categoría.'
                    continue
                
                # Líenas que no tengan ID
                line_id_pos = line.find(SIL_ID_DELIMITER)
                if line_id_pos == -1:
                    errors[idx] = 'ERR. No se pudo obtener un ID válido para esta traducción.'
                    continue
                
                # Eliminamos el ultimo separador
                if line.endswith(SIL_DELIMITER):
                    line = line[:-len(SIL_DELIMITER)]
                
                # Se extrae el ID y las traducciones
                line_id = line.split(SIL_ID_DELIMITER)[0]
                line_values = line[line_id_pos + 1:].split(SIL_DELIMITER)
                
                # Casos en los que se escriben valores fijos desde write_sil()
                if cur_category == SIL_CATEGORY_EXTENDED and line_id.endswith('_IsSubComponent'):
                    continue
                if cur_category == SIL_CATEGORY_EXTENDED and line_id.endswith('_TypeKind'):
                    continue
                if cur_category == SIL_CATEGORY_LANG_NAMES:
                    continue
                if cur_category == SIL_CATEGORY_OPTIONS:
                    continue
                
                # Si difiere la cantidad de idiomas
                if len(line_values) != len(lang_list):
                    errors[idx] = 'WRN. El número de idiomas en esta traducción es distinto a los idiomas definidos.'
                
                # Crear el objeto con la informaicón de esa línea
                line_obj = {}
                line_obj['id'] = line_id
                for (lang_idx, lang) in enumerate(lang_list):
                    if lang_idx < len(line_values):
                        line_obj[lang] = line_values[lang_idx]
                    else:
                        line_obj[lang] = ''
                    
                sil_data[cur_category].append(line_obj)
    except:
        return ({}, {})
    return (sil_data, errors)
            
def write_sil(sil_path: str, sil_data: dict) -> tuple[bool, str]:
    try:
        # Si la ruta al directorio padre no existe, la creamos
        os.makedirs(os.path.dirname(sil_path), exist_ok=True)
        
        # Añadir categorías si faltan
        if SIL_CATEGORY_LANG_NAMES not in sil_data.keys():
            sil_data[SIL_CATEGORY_LANG_NAMES] = []
        if SIL_CATEGORY_OPTIONS not in sil_data.keys():
            sil_data[SIL_CATEGORY_OPTIONS] = []
        
        # Preparar líneas
        lines = []
        sorted_keys = [
            SIL_CATEGORY_CAPTIONS,
            SIL_CATEGORY_CHARSET,
            SIL_CATEGORY_COLLECTIONS,
            SIL_CATEGORY_DIALOGS,
            SIL_CATEGORY_EXTENDED,
            SIL_CATEGORY_FONTS,
            SIL_CATEGORY_HINTS,
            SIL_CATEGORY_LANG_NAMES,
            SIL_CATEGORY_MULTILINES,
            SIL_CATEGORY_OPTIONS,
            SIL_CATEGORY_OTHER,
            SIL_CATEGORY_STRINGS
        ]
        for category in sorted_keys:
            data = sil_data.get(category, [])
            if len(data) == 0 and category not in [SIL_CATEGORY_LANG_NAMES, SIL_CATEGORY_OPTIONS]:
                continue
            
            # Añadimos el título de la categoría
            lines.append(NEW_LINE) # Salto de línea entre categorías
            lines.append(category)
            lines.append(NEW_LINE)
            
            # Excepciones con valores fijos
            if category == SIL_CATEGORY_LANG_NAMES:
                lang_name_lines = []
                for lang in get_lang_names():
                    lang_name_lines.append(f'Language_{LANGUAGES[lang]["index"] + 1}={lang.replace("_", " ")}' + NEW_LINE)
                
                # Para mantener un orden específico donde entre Language_1 y Language_2, van Language_10, Language_11, etc...
                lang_name_lines.sort(key=lambda _key: _key.split('=')[0])
                lines += lang_name_lines
                continue
            if category == SIL_CATEGORY_OPTIONS:
                lines.append('CommentsFile=' + NEW_LINE)
                lines.append(f'Delimiter={SIL_DELIMITER}' + NEW_LINE)
                lines.append('IsUTF8File=1' + NEW_LINE)
                continue
            
            # Añadimos las líneas que tienen contenido
            for translation in data:
                line_id = translation.get('id', '')
                
                # Para las cadenas que contienen distintos valores de una lista, deben
                # agruparse entre comillas si tienen espacios
                need_quote_marks = category in [SIL_CATEGORY_EXTENDED, SIL_CATEGORY_MULTILINES] and \
                    (line_id.endswith('.Items') or line_id.endswith('.Tabs') or line_id.endswith('.Categories'))
                if need_quote_marks:
                    line = line_id + SIL_ID_DELIMITER
                    
                    for lang in get_lang_names():
                        trans_values = translation.get(lang, '').split(',')
                        quoted_trans_list = []
                        quoted_trans = None
                        if len(trans_values) >= 2:
                            for trans_value in trans_values:
                                stripped_value = trans_value.strip()
                                if ' ' in stripped_value and not (stripped_value.startswith('\"') and stripped_value.endswith('\"')):
                                    quoted_trans_list.append(f'"{stripped_value}"')
                                else:
                                    quoted_trans_list.append(stripped_value)
                            quoted_trans = ','.join(quoted_trans_list)
                        line += (quoted_trans if quoted_trans else translation.get(lang, '')) + SIL_DELIMITER
                        
                    lines.append(line + NEW_LINE)
                else:
                    line = line_id + SIL_ID_DELIMITER
                    for lang in get_lang_names():
                        line += translation.get(lang, '') + SIL_DELIMITER
                    line += NEW_LINE
                    lines.append(line)
                
                # Añadimos las líneas de IsSubComponent y TypeKind con valores fijos
                if category == SIL_CATEGORY_EXTENDED:
                    lines.append(translation.get('id', '') + '_IsSubComponent' + SIL_ID_DELIMITER + '0' + NEW_LINE)
                    lines.append(translation.get('id', '') + '_TypeKind' + SIL_ID_DELIMITER + 'tkUnknown' + NEW_LINE)
        
        # Escribir archivo
        with open(sil_path, 'w', encoding='utf-8-sig') as sil_file:
            lines.append(NEW_LINE) # Los sil acaban con una línea vacía
            sil_file.writelines(lines)
        
    except Exception as e:
        return (False, e)

def read_csv(csv_path: str) -> tuple[dict, dict]:
    try:
        raw_data = []
        csv_data = {}
        errors = {}
        with open(csv_path, 'rb') as csv_file:
            if csv_file.read(3) == b'\xef\xbb\xbf':
                encoding = 'utf-8-sig'
            else:
                encoding = 'utf-8'
        
        with open(csv_path, 'r', encoding=encoding) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=CSV_DELIMITER)
            raw_data = [row for row in reader]
        
        for (idx, data) in enumerate(raw_data):
            category = data.get('category', '')
            if category:
                if category not in csv_data.keys():
                    csv_data[category] = []
            else:
                errors[idx] = 'ERR. Esta traducción no pertenece a ninguna categoría.'
                continue
                
            data.pop('category')
            csv_data[category].append(data)
            
    except:
        return ({}, {})
    return (csv_data, errors)

def write_csv(csv_path: str, sil_data: dict) -> tuple[bool, str]:
    # Cabecera CSV
    csv_data = [['category', 'id'] + get_lang_names()]
    
    # Preparar datos en formato lista de listas
    for (category, category_data) in sil_data.items():
        for data in category_data:
            csv_item = [category, data['id']]
            for lang in get_lang_names():        
                csv_item.append(data.get(lang, ''))
            csv_data.append(csv_item)
    
    # Escribir CSV
    try:
        # Si la ruta al directorio padre no existe, la creamos
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=CSV_DELIMITER)
            csv_writer.writerows(csv_data)
    except Exception as e:
        return (False, e)

def join(base_data: dict, join_data: dict) -> tuple[dict, dict]:
    indexed_data = {}
    for category, category_data in join_data.items():
        for data in category_data:
            _id = f'{category}|{data["id"]}'
            indexed_data[_id] = data
    
    for category, category_data in base_data.items():
        if join_data.get(category, ''):
            for data in category_data:
                if data.get('id', ''):
                    _id = f'{category}|{data["id"]}'
                    if _id in indexed_data.keys():
                        for lang in get_lang_names():                        
                            if indexed_data[_id].get(lang, ''):
                                data[lang] = indexed_data[_id][lang]
                else:
                    continue
        else:
            continue

    return (base_data, {})

def process_file(input_file: str, args: argparse.Namespace) -> None:
    # Completar lista de idiomas   
    if len(args.lang_list) > 0:
        lang_list = [lang.upper() for lang in args.lang_list]
    else:
        lang_list = get_lang_names()
    
    ext = os.path.splitext(input_file)[1] 
    if  ext.upper() == '.SIL':
        input_data, errors = read_sil(input_file, lang_list)
    elif ext.upper() == '.CSV':
        input_data, errors = read_csv(input_file)
    else:
        raise Exception(f'ERR. Formato de entrada desconocido ({ext}).')
            
    # Join
    if args.join_file_path:
        if os.path.isfile(args.join_file_path):
            ext = os.path.splitext(args.join_file_path)[1]
            if  ext.upper() == '.SIL':
                join_data, _ = read_sil(args.join_file_path, get_lang_names())
            elif ext.upper() == '.CSV':
                join_data, _ = read_csv(args.join_file_path)
            else:
                raise Exception(f'ERR. Formato de entrada desconocido ({ext}).')
            input_data, errors = join(input_data, join_data)
        else:
            raise Exception(f'Err. El archivo "{args.join_file_path}" no existe.')
    
            
    # Clear empty english rows
    if args.rme:
        for category_data in input_data.values():
            for data in category_data:
                if not data[LANG_EN]:
                    for lang in get_lang_names():
                        if lang != LANG_ES and lang != LANG_EN and lang in data.keys():
                            data[lang] = ''
            
    # Charset
    if args.chs:
        for data in input_data.get(SIL_CATEGORY_CHARSET, []):
            for lang in get_lang_names():
                if lang != 'id':
                    data[lang] = LANGUAGES[lang]['charset']
    
    # Font
    if args.fnt:
        for data in input_data.get(SIL_CATEGORY_FONTS, []):
            for lang in data.keys():
                if lang != 'id':
                    data[lang] = LANGUAGES[lang]['font']
    
    # Errores durante la lectura del archivo de entrada
    print(f'Errores: {sum(1 for err in errors.values() if err.startswith("ERR."))}')
    print(f'Warnings: {sum(1 for err in errors.values() if err.startswith("WRN."))}')
    if args.verbose:
        for n_line, err in errors.items():
            print(f'  Line: {n_line}: {err}')
        print()
    
    # Escribir el output
    output_file = args.output if args.output else input_file
    ext = os.path.splitext(output_file)[1]
    if  ext.upper() == '.SIL':
        write_sil(output_file, input_data)
    elif ext.upper() == '.CSV':
        write_csv(output_file, input_data)
    else:
        raise Exception(f'Err. Formato de salida desconocido ({ext}).')

# ========================================================================

if __name__ == '__main__':
    program_description = '''
    SIL FIXER
    Permite realizar una serie de operaciones sobre los archivos de traducción.
    '''
    parser = argparse.ArgumentParser(description=program_description)
    
    parser.add_argument('--lang-list',
                        dest='lang_list',
                        nargs='*',
                        action='store',
                        required=False,
                        default=[],
                        type=str,
                        help='Lista de idiomas que contiene el SIL. Si no se utiliza, se considera que incluye todos los idiomas.')
    
    parser.add_argument('--input', '-i',
                        dest='input',
                        action='store',
                        required=True,
                        type=str,
                        help='Archivo SIL o CSV de entrada.')
    
    parser.add_argument('--output', '-o',
                        dest='output',
                        action='store',
                        default='',
                        required=False,
                        type=str,
                        help='Archivo SIL o CSV de salida. Si no se declara, es igual al de entrada.')
    
    join_help = '''
    Unifica el archivo actual (A) con otro archivo SIL o CSV (B). El resultado es A con las traducciones de B.
       - Si la traducción es distinta de vacío en A y en B, siempre manda B.
       - Si la traducción es vacío en A y existe en B, manda B.
       - Si la traducción es vacío en B y existe en A, manda A.
    '''
    parser.add_argument('--join', '-j',
                        dest='join_file_path',
                        action='store',
                        default='',
                        required=False,
                        type=str,
                        help=join_help)
    
    parser.add_argument('--remove-empty-english', '-rme',
                        dest='rme',
                        action='store_true',
                        default=False,
                        help='Elimina las traducciones para todas aquellas filas en las que el inglés esté vacío. La columna "español" no se modifica.')
    
    parser.add_argument('--charset', '-chs',
                        dest='chs',
                        action='store_true',
                        default=False,
                        help='Establece el valor recomendado en todos los valores de Charset.')
    
    parser.add_argument('--font', '-fnt',
                        dest='fnt',
                        action='store_true',
                        default=False,
                        help='Establece el valor "Tahoma" en todos los valores de Font.')
    
    parser.add_argument('--verbose', '-v',
                        dest='verbose',
                        action='store_true',
                        default=False,
                        help='Muestra los errores encontrados durante la lectura del archivo SIL de entrada.')
    
    args = parser.parse_args()
    # ---
    
    try:
        if os.path.isdir(args.input):
            # Si es una carpeta, forzamos a sobreescribir el archivo original
            args.output = ''
            folder_path = Path(args.input)
            sil_files = list(folder_path.glob('**/*.[sS][iI][lL]'))
        elif os.path.isfile(args.input):
            sil_files = [args.input]
        else:
            raise Exception(f'Err. Input erróneo. El archivo o directorio podría no existir ({args.input}).')
        
        print('============')
        for sil_file in sil_files:
            process_file(sil_file, args)
            print(f'> Archivo procesado: {sil_file}')
            print('============')
        print('> Fin.')
        print('============')
    except Exception as e:
        print('============')
        print(f'> {e}')
        print('============')