import requests

import fs.copy as fscopy
from fs.osfs import OSFS
from fs.memoryfs import MemoryFS
from fs.zipfs import ZipFS
import os
import sys

print("Ren'Py setup")

#with MemoryFS() as tempfs:
cwdfs = OSFS(".")
tempfs = MemoryFS()

if "ddlc-win.zip" not in cwdfs.listdir("/"):
    print("Please place a copy of ddlc-win.zip next to this app.")
    input("Press enter to continue...")
    sys.exit()

if "renpy.zip" not in cwdfs.listdir("/"):
    print("---- Downloading Ren'Py")
    r = requests.get("https://www.renpy.org/dl/6.99.12.4/renpy-6.99.12.4-sdk.zip")
    r.raise_for_status()
    with cwdfs.open("renpy.zip", 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)

print("---- Extracting Ren'Py")
with ZipFS("./renpy.zip") as zipfs:
    fscopy.copy_dir(zipfs, "renpy-6.99.12.4-sdk", tempfs, "renpy")
cwdfs.remove("renpy.zip")

print("ModTemplate setup")
if "modtemplate.zip" not in cwdfs.listdir("/"):
    print("---- Downloading ModTemplate")
    r = requests.get("https://github.com/Monika-After-Story/DDLCModTemplate/releases/download/v1.1.0/DDLCModTemplate_1.1.0.zip")
    r.raise_for_status()
    with cwdfs.open("modtemplate.zip", 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)

print("---- Extracting ModTemplate")
with ZipFS("./modtemplate.zip") as zipfs:
    fscopy.copy_fs(zipfs, tempfs.makedirs("renpy/My DDLC Mod"))
cwdfs.remove("modtemplate.zip")

print("---- Extracting game rpas")
with ZipFS("./ddlc-win.zip") as zipfs:
    gamefs = zipfs.opendir(zipfs.listdir("/")[0]).opendir("game")
    templatefs = tempfs.opendir("renpy/My DDLC Mod/game")
    for fn in ("images.rpa", "fonts.rpa", "audio.rpa"):
        print("--------- Extracting {}".format(fn))
        fscopy.copy_file(gamefs, fn, templatefs, fn)

print("Moving to real filesystem...")
fscopy.copy_fs(tempfs.opendir("renpy"), cwdfs)
