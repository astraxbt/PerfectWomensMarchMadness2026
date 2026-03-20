# 2026 Women's Bracket Universe

This repository contains the pre-tipoff generated bracket universe split into 8 binary parts for browser upload.

Files:
- all_valid_brackets.part01.bin
- all_valid_brackets.part02.bin
- all_valid_brackets.part03.bin
- all_valid_brackets.part04.bin
- all_valid_brackets.part05.bin
- all_valid_brackets.part06.bin
- all_valid_brackets.part07.bin
- all_valid_brackets.part08.bin
- all_valid_brackets_manifest.txt

The manifest contains the SHA-256 of the original full file and each part.

1. Download all 8 .bin part files plus reassemble_file.py
2. Run: python reassemble_file.py
3. This rebuilds all_valid_brackets.bin
4. Then inspect any bracket with:
   python read_bracket.py 0
   python read_bracket.py 1000
