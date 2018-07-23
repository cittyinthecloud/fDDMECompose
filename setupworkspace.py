import requests

import fs.copy as fscopy
from fs.osfs import OSFS
from fs.memoryfs import MemoryFS
from fs.zipfs import ZipFS
import os
import sys
from clint.textui import puts, indent

puts("Ren'Py setup")

with indent(2):
    cwdfs = OSFS(".")
    tempfs = MemoryFS()

    if "renpy.zip" not in cwdfs.listdir("/"):
        puts("Downloading Ren'Py")
        r = requests.get("https://www.renpy.org/dl/6.99.12.4/renpy-6.99.12.4-sdk.zip", stream=True)
        r.raise_for_status()
        with cwdfs.open("renpy.zip", 'wb') as fd:
            for chunk in progress.bar(r.iter_content(chunk_size=1024)):
                fd.write(chunk)

    puts("Extracting Ren'Py")
    with ZipFS("./renpy.zip") as zipfs:
        fscopy.copy_dir(zipfs, "renpy-6.99.12.4-sdk", tempfs, "renpy")
    cwdfs.remove("renpy.zip")

puts("ModTemplate setup")

with indent(2):
    if "modtemplate.zip" not in cwdfs.listdir("/"):
        puts("Downloading ModTemplate")
        r = requests.get("https://github.com/Monika-After-Story/DDLCModTemplate/releases/download/v1.1.0/DDLCModTemplate_1.1.0.zip", stream=True)
        r.raise_for_status()
        with cwdfs.open("modtemplate.zip", 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)

        puts("Extracting ModTemplate")
        with ZipFS("./modtemplate.zip") as zipfs:
            fscopy.copy_fs(zipfs, tempfs.makedirs("renpy/My DDLC Mod"))
        cwdfs.remove("modtemplate.zip")


        puts("Adding game rpas")
        with indent(2):
            if "ddlc-win.zip" not in cwdfs.listdir("/"):
                puts("Downloading DDLC")
                with indent(2):
                    puts("Getting URL")
                    r = requests.post("https://teamsalvato.itch.io/ddlc/file/594897")
                    r.raise_for_status()
                    ddlcurl = r.json()["url"]
                    puts("Downloading")
                    r=requests.get(ddlcurl, stream=True)
                    with cwdfs.open("ddlc-win.zip", 'wb') as fd:
                        for chunk in r.iter_content(chunk_size=1024):
                            fd.write(chunk)


        puts("Extracting game rpas")
        with ZipFS("./ddlc-win.zip") as zipfs:
            gamefs = zipfs.opendir(zipfs.listdir("/")[0]).opendir("game")
            templatefs = tempfs.opendir("renpy/My DDLC Mod/game")
            for fn in ("images.rpa", "fonts.rpa", "audio.rpa"):
                puts("Extracting {}".format(fn))
                fscopy.copy_file(gamefs, fn, templatefs, fn)

puts("Moving to real filesystem...")
fscopy.copy_fs(tempfs.opendir("renpy"), cwdfs)
