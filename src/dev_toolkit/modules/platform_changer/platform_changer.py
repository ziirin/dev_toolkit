import os
import glob
import shutil
import re
from datetime import datetime
import xml.etree.ElementTree as ET

def _replace_cbproj_options(file_path, is_64bits, modify_version, config):
    if not file_path or not os.path.exists(file_path):
        return False

    try:
        # Registrar el namespace para evitar que ElementTree añada prefijos como 'ns0:'
        # Los .cbproj suelen usar este namespace de MSBuild
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"
        ET.register_namespace('', namespace)
        ns = {'ms': namespace}

        tree = ET.parse(file_path)
        root = tree.getroot()

        name_project = os.path.splitext(os.path.basename(file_path))[0]
        today = datetime.now()
        year, month, day = today.year, today.month, today.day

        # Tipo de aplicación (se determina en el primer PropertyGroup)
        app_type = ""

        # Buscamos todos los PropertyGroup
        for property_group in root.findall('ms:PropertyGroup', ns):
            
            # 1. Lógica para PropertyGroup sin atributos (Configuración general)
            if not property_group.attrib:
                node_app_type = property_group.find('ms:AppType', ns)
                if node_app_type is not None:
                    app_type = node_app_type.text

                node_platform = property_group.find('ms:Platform', ns)
                if node_platform is not None:
                    node_platform.text = "Win64" if is_64bits else "Win32"

                if config is not None:
                    c = config
                    # Proyectos especiales que siempre van en Release
                    if name_project in ["sisl43", "smlib", "importExport", "ines_glu32", "WnLib"]:
                        c = "Release"
                    
                    node_config = property_group.find('ms:Config', ns)
                    if node_config is not None:
                        node_config.text = c
                continue

            # 2. Lógica de Versión (VerInfo_Keys)
            if modify_version and app_type == "Application":
                keys_node = property_group.find('ms:VerInfo_Keys', ns)
                if keys_node is not None and keys_node.text:
                    content = keys_node.text
                    new_ver = f"{year}.{month}.{day}.0"
                    
                    content = re.sub(r"FileVersion=[0-9.]*", f"FileVersion={new_ver}", content)
                    content = re.sub(r"ProductVersion=[0-9.]*", f"ProductVersion={new_ver}", content)
                    keys_node.text = content

                # Nodos de versión individuales
                version_map = {
                    'VerInfo_MajorVer': str(year),
                    'VerInfo_MinorVer': str(month),
                    'VerInfo_Release': str(day)
                }
                for tag, value in version_map.items():
                    node = property_group.find(f'ms:{tag}', ns)
                    if node is not None:
                        node.text = value

            # 3. Lógica para Condición '$(Base)'!=''
            condition = property_group.attrib.get('Condition', '')
            if "'$(Base)'!=''" == condition:
                # RunBCCOutOfProcess
                rbcc = property_group.find('ms:RunBCCOutOfProcess', ns)
                if rbcc is None:
                    rbcc = ET.SubElement(property_group, f"{{{namespace}}}RunBCCOutOfProcess")
                rbcc.text = "true" if is_64bits else "false"

                # SubProcessesNumber
                sub_proc = property_group.find('ms:SubProcessesNumber', ns)
                if sub_proc is None:
                    sub_proc = ET.SubElement(property_group, f"{{{namespace}}}SubProcessesNumber")
                sub_proc.text = str(os.cpu_count() or 1)

        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        return True

    except Exception as e:
        print(f"Error procesando {file_path}: {e}")
        return False

def platform_changer(values: dict[str, list[str]], modify_version: bool):
    # Obtener archivos .cbproj
    for directory, value in values.items():
        path_search = os.path.join(directory, '*.cbproj')
        found = glob.glob(path_search, recursive=False)
        
        # Modificar .cbproj
        is_64bits = (value[0] == 'w64')
        config = value[1]
        for f in found:
            _replace_cbproj_options(f, is_64bits, modify_version, config)

    # Copiar DLLs
    pattern = re.compile(r'^c:\\fuentes\\nucleo\\[^\\]+\\app$', re.IGNORECASE)
    for directory, value in values.items():
        if not pattern.match(directory):
            continue
        
        dll_base_path = os.path.join(directory, 'dlls')
        if os.path.exists(dll_base_path):
            # Borrar DLLs anteriores en \App\
            app_path = os.path.join(directory)
            for old_dll in glob.glob(os.path.join(app_path, '*.dll')):
                try:
                    os.remove(old_dll)
                except OSError:
                    pass

            # Origen según plataforma
            is_64bits = (value[0] == 'w64')
            sub_dir = 'Win64' if is_64bits else 'Win32'
            src_path = os.path.join(dll_base_path, sub_dir)
            
            if os.path.exists(src_path):
                for dll_item in os.listdir(src_path):
                    full_file_name = os.path.join(src_path, dll_item)
                    if os.path.isfile(full_file_name):
                        shutil.copy(full_file_name, app_path)