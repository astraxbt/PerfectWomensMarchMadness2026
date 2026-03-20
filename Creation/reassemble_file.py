import os
import hashlib

PART_FILES = [
    "all_valid_brackets.part01.bin",
    "all_valid_brackets.part02.bin",
    "all_valid_brackets.part03.bin",
    "all_valid_brackets.part04.bin",
    "all_valid_brackets.part05.bin",
    "all_valid_brackets.part06.bin",
    "all_valid_brackets.part07.bin",
    "all_valid_brackets.part08.bin",
]

OUTPUT_FILE = "all_valid_brackets.bin"


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def main():
    for part in PART_FILES:
        if not os.path.exists(part):
            print(f"Missing file: {part}")
            return

    with open(OUTPUT_FILE, "wb") as out:
        for part in PART_FILES:
            print(f"Adding {part} ...")
            with open(part, "rb") as f:
                while True:
                    chunk = f.read(1024 * 1024)
                    if not chunk:
                        break
                    out.write(chunk)

    print(f"\nDone. Rebuilt file: {OUTPUT_FILE}")
    print(f"Size: {os.path.getsize(OUTPUT_FILE):,} bytes")
    print(f"SHA-256: {sha256_of_file(OUTPUT_FILE)}")


if __name__ == "__main__":
    main()