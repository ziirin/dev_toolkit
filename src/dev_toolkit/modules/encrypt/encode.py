import numpy as np
from PIL import Image
from pathlib import Path
import math
import os

def encode_file_to_images(input_path, base_filename, max_dim=512):
    """
    Reads a file and encodes its content into RGB images.
    Uses UTF-8 to avoid 'charmap' errors.
    """
    try:
        # Forzamos la codificación utf-8 para leer archivos con ñ, tildes, etc.
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        # Si falla, intentamos con latin-1 que suele aceptar bytes crudos
        with open(input_path, 'r', encoding='latin-1') as f:
            text = f.read()

    # Filtramos a ASCII extendido (0-255)
    data = [ord(char) if ord(char) <= 255 else 0 for char in text]
    
    chars_per_image = max_dim * max_dim * 3
    chunks = [data[i:i + chars_per_image] for i in range(0, len(data), chars_per_image)]
    
    for index, chunk in enumerate(chunks):
        num_pixels = math.ceil(len(chunk) / 3)
        side = math.ceil(math.sqrt(num_pixels))
        
        total_required = side * side * 3
        padding = total_required - len(chunk)
        chunk.extend([0] * padding)
        
        pixel_matrix = np.array(chunk, dtype=np.uint8).reshape((side, side, 3))
        img = Image.fromarray(pixel_matrix, 'RGB')
        
        filename = str(Path(f"{base_filename}_{index}.png"))
        img.save(filename)
        print(f"Saved: {filename} ({side}x{side} px)")

def decode_images_to_text(file_list, output_txt):
    """
    Reads images and saves the reconstructed text into a file.
    """
    full_text = []
    for filename in sorted(file_list):
        img = Image.open(filename).convert('RGB')
        pixel_matrix = np.array(img)
        flattened_data = pixel_matrix.flatten()
        
        # Filtramos ceros (padding)
        chars = [chr(val) for val in flattened_data if val != 0]
        full_text.append("".join(chars))
    
    final_content = "".join(full_text)
    
    # Guardamos el resultado especificando utf-8
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"Success: Text restored to {output_txt}")

# --- MODO DE USO ---
if __name__ == "__main__":
    input_file = r"C:\Fuentes\Nucleo\ShoeData\tlast.cpp" 
    
    if os.path.exists(input_file):
        encode_file_to_images(input_file, "encoded_archive")
        
        # Para decodificar:
        images = [f for f in os.listdir() if f.startswith("encoded_archive") and f.endswith(".png")]
        decode_images_to_text(images, "restored_text.txt")
    else:
        print(f"Error: No se encuentra el archivo {input_file}")