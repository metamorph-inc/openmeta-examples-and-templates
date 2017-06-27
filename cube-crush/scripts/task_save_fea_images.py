from glob import glob
from zipfile import ZipFile
from os.path import basename

if __name__ == "__main__":
    files = glob("Analysis/Patran_Nastran/*.png") + \
            glob("Analysis/Patran_Nastran/*.jpg")
    with ZipFile('FEA_Images.zip', 'w') as zout:
        for file in files:
            zout.write(file, basename(file))