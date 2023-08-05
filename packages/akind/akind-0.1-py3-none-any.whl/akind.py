import os
import shutil
import sys
import tkinter
import zipfile
from pathlib import Path
from tkinter import filedialog

import img2pdf

# Setting
EXPORT_DIR = "/Volumes/Kindle/documents"

root = tkinter.Tk()
root.withdraw()


def main():
    """Export zip or pdf files to Kindle."""
    if not Path(EXPORT_DIR).exists():
        print("Kindle is not connected.", file=sys.stderr)
        sys.exit(1)

    type_zip = ('zip file', '*.zip')
    type_pdf = ('pdf file', '*.pdf')

    files = filedialog.askopenfiles(filetypes=[type_zip, type_pdf], initialdir=os.path.expanduser('~'))
    for f in files:
        export_path = Path(EXPORT_DIR) / f"{Path(f.name).stem}.pdf"
        if f.name.endswith('.zip'):
            with open(export_path, 'wb') as pdf, zipfile.ZipFile(f.name, 'r') as _zip:
                pdf.write(img2pdf.convert([_zip.open(img) for img in _zip.infolist()]))
        else:
            shutil.copy(f.name, export_path)


if __name__ == '__main__':
    main()
