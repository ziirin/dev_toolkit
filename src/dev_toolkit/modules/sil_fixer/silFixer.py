import os
import csv
import argparse

from ...cli_menu.routing import DevTool

# ========================================================================

# Delimitadores y otros
SIL_ID_DELIMITER = '='
SIL_DELIMITER = '~!@#'
CSV_DELIMITER = ';'
NEW_LINE = '\n'

# Identificador de idioma
LANG_COUNT                  = 11
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

# Charsets
LANG_ES_CHARSET             = 'ANSI_CHARSET'
LANG_EN_CHARSET             = 'DEFAULT_CHARSET'
LANG_IT_CHARSET             = 'DEFAULT_CHARSET'
LANG_ZHt_CHARSET            = 'CHINESEBIG5_CHARSET'
LANG_ZHs_CHARSET            = 'GB2312_CHARSET'
LANG_TR_CHARSET             = 'TURKISH_CHARSET'
LANG_FR_CHARSET             = 'ANSI_CHARSET'
LANG_RU_CHARSET             = 'RUSSIAN_CHARSET'
LANG_PT_CHARSET             = 'DEFAULT_CHARSET'
LANG_EL_CHARSET             = 'GREEK_CHARSET'
LANG_DE_CHARSET             = 'ANSI_CHARSET'

# Fuentes
LANG_ES_FONT                = 'Tahoma'
LANG_EN_FONT                = 'Tahoma'
LANG_IT_FONT                = 'Tahoma'
LANG_ZHt_FONT               = 'Tahoma'
LANG_ZHs_FONT               = 'Tahoma'
LANG_TR_FONT                = 'Tahoma'
LANG_FR_FONT                = 'Tahoma'
LANG_RU_FONT                = 'Tahoma'
LANG_PT_FONT                = 'Tahoma'
LANG_EL_FONT                = 'Tahoma'
LANG_DE_FONT                = 'Tahoma'

# Categorías en archivos SILs
SIL_CATEGORY_CAPTIONS       = '[Captions]'
SIL_CATEGORY_CHARSET        = '[CharSets]' # No contiene traducciones
SIL_CATEGORY_COLLECTIONS    = '[Collections]'
SIL_CATEGORY_EXTENDED       = '[Extended]' # Contiene traducciones pero cuidado con IsSubComponent y TypeKind
SIL_CATEGORY_FONTS          = '[Fonts]' # No contiene traducciones
SIL_CATEGORY_HINTS          = '[Hints]'
SIL_CATEGORY_LANG_NAMES     = '[Language names - for internal use only!]' # No contiene traducciones
SIL_CATEGORY_MULTILINES     = '[Multilines]'
SIL_CATEGORY_OPTIONS        = '[OPTIONS]' # No contiene traducciones
SIL_CATEGORY_OTHER          = '[Other]'
SIL_CATEGORY_STRINGS        = '[Strings]'

# ========================================================================

def read_sil(sil_path: str, lang_list: list[str] | None = None) -> tuple[dict, dict]:
    sil_data = {}
    errors = {}
    
    if not lang_list:
        lang_list = [
            LANG_ES,
            LANG_EN,
            LANG_IT,
            LANG_ZHt,
            LANG_ZHs,
            LANG_TR,
            LANG_FR,
            LANG_RU,
            LANG_PT,
            LANG_EL,
            LANG_DE
        ]
    
    try:
        with open(sil_path, 'r', encoding='utf-8') as sil_file:
            lines = sil_file.readlines()
            
            cur_category = ''
            for (idx, line) in enumerate(lines):
                if line.endswith('\n'):
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
        for (category, data) in sil_data.items():
            # Añadimos el título de la categoría
            lines.append(NEW_LINE) # Salto de línea entre categorías
            lines.append(category)
            lines.append(NEW_LINE)
            
            # Excepciones con valores fijos
            if category == SIL_CATEGORY_LANG_NAMES:
                lines.append(f'Language_1={LANG_ES.replace("_", " ")}' + NEW_LINE)
                lines.append(f'Language_10={LANG_EL.replace("_", " ")}' + NEW_LINE)
                lines.append(f'Language_11={LANG_DE.replace("_", " ")}' + NEW_LINE)
                lines.append(f'Language_2={LANG_EN.replace("_", " ")}' + NEW_LINE)
                lines.append(f'Language_3={LANG_IT.replace("_", " ")}' + NEW_LINE)
                lines.append(f'Language_4={LANG_ZHt.replace("_", " ")}' + NEW_LINE)
                lines.append(f'Language_5={LANG_ZHs.replace("_", " ")}' + NEW_LINE)
                lines.append(f'Language_6={LANG_TR.replace("_", " ")}' + NEW_LINE)
                lines.append(f'Language_7={LANG_FR.replace("_", " ")}' + NEW_LINE)
                lines.append(f'Language_8={LANG_RU.replace("_", " ")}' + NEW_LINE)
                lines.append(f'Language_9={LANG_PT.replace("_", " ")}' + NEW_LINE)
                continue
            if category == SIL_CATEGORY_OPTIONS:
                lines.append('CommentsFile=' + NEW_LINE)
                lines.append(f'Delimiter={SIL_DELIMITER}' + NEW_LINE)
                lines.append('IsUTF8File=1' + NEW_LINE)
                continue
            
            # Añadimos las líneas que tienen contenido
            for translation in data:
                lines.append(
                    translation.get('id', '') + SIL_ID_DELIMITER +
                    translation.get(LANG_ES, '') + SIL_DELIMITER +
                    translation.get(LANG_EN, '') + SIL_DELIMITER +
                    translation.get(LANG_IT, '') + SIL_DELIMITER +
                    translation.get(LANG_ZHt, '') + SIL_DELIMITER +
                    translation.get(LANG_ZHs, '') + SIL_DELIMITER +
                    translation.get(LANG_TR, '') + SIL_DELIMITER +
                    translation.get(LANG_FR, '') + SIL_DELIMITER +
                    translation.get(LANG_RU, '') + SIL_DELIMITER +
                    translation.get(LANG_PT, '') + SIL_DELIMITER +
                    translation.get(LANG_EL, '') + SIL_DELIMITER +
                    translation.get(LANG_DE, '') + SIL_DELIMITER +
                    NEW_LINE
                )
                
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
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
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
    header = [
        'category',
        'id',
        LANG_ES,
        LANG_EN,
        LANG_IT,
        LANG_ZHt,
        LANG_ZHs,
        LANG_TR,
        LANG_FR,
        LANG_RU,
        LANG_PT,
        LANG_EL,
        LANG_DE
    ]
    csv_data = [header]
    
    # Preparar datos en formato lista de listas
    for (category, category_data) in sil_data.items():
        for data in category_data:
            csv_item = []
            csv_item.append(category)
            csv_item.append(data['id'])
            csv_item.append(data.get(LANG_ES, ''))
            csv_item.append(data.get(LANG_EN, ''))
            csv_item.append(data.get(LANG_IT, ''))
            csv_item.append(data.get(LANG_ZHt, ''))
            csv_item.append(data.get(LANG_ZHs, ''))
            csv_item.append(data.get(LANG_TR, ''))
            csv_item.append(data.get(LANG_FR, ''))
            csv_item.append(data.get(LANG_RU, ''))
            csv_item.append(data.get(LANG_PT, ''))
            csv_item.append(data.get(LANG_EL, ''))
            csv_item.append(data.get(LANG_DE, ''))
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
                        if indexed_data[_id][LANG_ES]:
                            data[LANG_ES] = indexed_data[_id][LANG_ES]
                        if indexed_data[_id][LANG_EN]:
                            data[LANG_EN] = indexed_data[_id][LANG_EN]
                        if indexed_data[_id][LANG_IT]:
                            data[LANG_IT] = indexed_data[_id][LANG_IT]
                        if indexed_data[_id][LANG_ZHt]:
                            data[LANG_ZHt] = indexed_data[_id][LANG_ZHt]
                        if indexed_data[_id][LANG_ZHs]:
                            data[LANG_ZHs] = indexed_data[_id][LANG_ZHs]
                        if indexed_data[_id][LANG_TR]:
                            data[LANG_TR] = indexed_data[_id][LANG_TR]
                        if indexed_data[_id][LANG_FR]:
                            data[LANG_FR] = indexed_data[_id][LANG_FR]
                        if indexed_data[_id][LANG_RU]:
                            data[LANG_RU] = indexed_data[_id][LANG_RU]
                        if indexed_data[_id][LANG_PT]:
                            data[LANG_PT] = indexed_data[_id][LANG_PT]
                        if indexed_data[_id][LANG_EL]:
                            data[LANG_EL] = indexed_data[_id][LANG_EL]
                        if indexed_data[_id][LANG_DE]:
                            data[LANG_DE] = indexed_data[_id][LANG_DE]
                else:
                    continue
        else:
            continue

    return (base_data, {})

# ========================================================================

if __name__ == '__main__':
    program_description = '''
    SIL FIXER
    Permite realizar una serie de operaciones sobre un archivo sil.
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
       - Si la traducción es distinto de vacío en A y en B, siempre manda B.
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
    
    # Completar lista de idiomas   
    if len(args.lang_list) > 0:
        lang_list = [lang.upper() for lang in args.lang_list]
    else:
        lang_list = [
            LANG_ES,
            LANG_EN,
            LANG_IT,
            LANG_ZHt,
            LANG_ZHs,
            LANG_TR,
            LANG_FR,
            LANG_RU,
            LANG_PT,
            LANG_EL,
            LANG_DE
        ]

    ext = os.path.splitext(args.input)[1]
    if  ext.upper() == '.SIL':
        input_data, errors = read_sil(args.input, lang_list)
    elif ext.upper() == '.CSV':
        input_data, errors = read_csv(args.input)
    else:
        raise Exception(f'ERR. Formato de entrada desconocido ({ext}).')
            
    # Join
    if args.join_file_path:
        if os.path.isfile(args.join_file_path):
            ext = os.path.splitext(args.join_file_path)[1]
            if  ext.upper() == '.SIL':
                join_data, _ = read_sil(args.join_file_path, [
                    LANG_ES,
                    LANG_EN,
                    LANG_IT,
                    LANG_ZHt,
                    LANG_ZHs,
                    LANG_TR,
                    LANG_FR,
                    LANG_RU,
                    LANG_PT,
                    LANG_EL,
                    LANG_DE
                ])
            elif ext.upper() == '.CSV':
                join_data, _ = read_csv(args.join_file_path)
            else:
                raise Exception(f'ERR. Formato de entrada desconocido ({ext}).')
            input_data, errors = join(input_data, join_data)
        else:
            raise Exception(f'Err. El archivo "{args.join_file_path}" no existe.')
    
            
    # Clear empty english rows
    if args.rme:
        for category, category_data in input_data.items():
            for data in category_data:
                if not data[LANG_EN]:
                    data[LANG_IT] = ''
                    data[LANG_ZHt] = ''
                    data[LANG_ZHs] = ''
                    data[LANG_TR] = ''
                    data[LANG_FR] = ''
                    data[LANG_RU] = ''
                    data[LANG_PT] = ''
                    data[LANG_EL] = ''
                    data[LANG_DE] = ''
            
    # Charset
    if args.chs:
        for data in input_data.get(SIL_CATEGORY_CHARSET, []):
            data[LANG_ES] = LANG_ES_CHARSET
            data[LANG_EN] = LANG_EN_CHARSET
            data[LANG_IT] = LANG_IT_CHARSET
            data[LANG_ZHt] = LANG_ZHt_CHARSET
            data[LANG_ZHs] = LANG_ZHs_CHARSET
            data[LANG_TR] = LANG_TR_CHARSET
            data[LANG_FR] = LANG_FR_CHARSET
            data[LANG_RU] = LANG_RU_CHARSET
            data[LANG_PT] = LANG_PT_CHARSET
            data[LANG_EL] = LANG_EL_CHARSET
            data[LANG_DE] = LANG_DE_CHARSET
    
    # Font
    if args.fnt:
        for data in input_data.get(SIL_CATEGORY_FONTS, []):
            data[LANG_ES] = LANG_ES_FONT
            data[LANG_EN] = LANG_EN_FONT
            data[LANG_IT] = LANG_IT_FONT
            data[LANG_ZHt] = LANG_ZHt_FONT
            data[LANG_ZHs] = LANG_ZHs_FONT
            data[LANG_TR] = LANG_TR_FONT
            data[LANG_FR] = LANG_FR_FONT
            data[LANG_RU] = LANG_RU_FONT
            data[LANG_PT] = LANG_PT_FONT
            data[LANG_EL] = LANG_EL_FONT
            data[LANG_DE] = LANG_DE_FONT
    
    # Errores durante la lectura del archivo de entrada
    print(f'Errores: {sum(1 for err in errors.values() if err.startswith("ERR."))}')
    print(f'Warnings: {sum(1 for err in errors.values() if err.startswith("WRN."))}')
    if args.verbose:
        for n_line, err in errors.items():
            print(f'  Line: {n_line}: {err}')
        print()
    
    # Escribir el output
    output_path = args.output if args.output else args.input
    ext = os.path.splitext(output_path)[1]
    if  ext.upper() == '.SIL':
        write_sil(output_path, input_data)
    elif ext.upper() == '.CSV':
        write_csv(output_path, input_data)
    else:
        raise Exception(f'Err. Formato de salida desconocido ({ext}).')