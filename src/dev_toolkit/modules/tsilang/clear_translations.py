import os
import sys
import chardet

new_content = ["      73007400430061007000740069006F006E0073005F0055006E00690063006F00\n",
			   "      640065000D000A0073007400480069006E00740073005F0055006E0069006300\n",
			   "      6F00640065000D000A007300740044006900730070006C00610079004C006100\n",
			   "      620065006C0073005F0055006E00690063006F00640065000D000A0073007400\n",
			   "      46006F006E00740073005F0055006E00690063006F00640065000D000A007300\n",
			   "      74004D0075006C00740069004C0069006E00650073005F0055006E0069006300\n",
			   "      6F00640065000D000A007300740053007400720069006E00670073005F005500\n",
			   "      6E00690063006F00640065000D000A00730074004F0074006800650072005300\n",
			   "      7400720069006E00670073005F0055006E00690063006F00640065000D000A00\n",
			   "      7300740043006F006C006C0065006300740069006F006E0073005F0055006E00\n",
			   "      690063006F00640065000D000A00730074004300680061007200530065007400\n",
			   "      73005F0055006E00690063006F00640065000D000A00}\n"]

new_content_mainform = ["      73007400430061007000740069006F006E0073005F0055006E00690063006F00\n",
						"      640065000D000A0073007400480069006E00740073005F0055006E0069006300\n",
						"      6F00640065000D000A007300740044006900730070006C00610079004C006100\n",
						"      620065006C0073005F0055006E00690063006F00640065000D000A0073007400\n",
						"      46006F006E00740073005F0055006E00690063006F00640065000D000A007300\n",
						"      74004D0075006C00740069004C0069006E00650073005F0055006E0069006300\n",
						"      6F00640065000D000A007300740044006C006700730043006100700074006900\n",
						"      6F006E0073005F0055006E00690063006F00640065000D000A00730074005300\n",
						"      7400720069006E00670073005F0055006E00690063006F00640065000D000A00\n",
						"      730074004F00740068006500720053007400720069006E00670073005F005500\n",
						"      6E00690063006F00640065000D000A00730074004C006F00630061006C006500\n",
						"      73005F0055006E00690063006F00640065000D000A007300740043006F006C00\n",
						"      6C0065006300740069006F006E0073005F0055006E00690063006F0064006500\n",
						"      0D000A0073007400430068006100720053006500740073005F0055006E006900\n",
						"      63006F00640065000D000A00}\n"]


def detect_encoding(file_path: str):
	with open(file_path, 'rb') as f:
		result = chardet.detect(f.read())
	return result['encoding']


def remove_translation_data(folder: str) -> None:
	norm_folder = os.path.normpath(folder)

	ext = ".dfm"
	for root, _, files in os.walk(norm_folder):
		for filename in files:
			if filename.endswith(ext):
				full_path = os.path.join(root, filename)

				encoding = detect_encoding(full_path)
				with open(full_path, 'r', encoding=encoding, errors='ignore') as file:
					lines = file.readlines()

				translation_data_present = any('TranslationData = {' in line for line in lines)

				if translation_data_present:
					content = new_content
					if filename == "mainform.dfm":
						content = new_content_mainform
					print(full_path)
					with open(full_path, 'w', encoding=encoding) as file:
						within_braces = False
						inside_extended = False
						for line in lines:
							if 'TranslationData = {' in line:
								within_braces = True
								file.write(line)
								for item in content:
									file.write(item)
							elif '}' in line and within_braces:
								within_braces = False
								continue
							elif within_braces:
								continue
							elif 'ExtendedTranslations' in line:
								file.write(line)
								indent = line[:len(line) - len(line.lstrip())]
								file.write(f"{indent}>\n")
								inside_extended = True
								continue
							elif inside_extended:
								if '>' in line:
									inside_extended = False
							else:
								file.write(line)


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Falta el directorio sobre el que actuar.")
	else:
		directory = sys.argv[1]
		remove_translation_data(directory)
