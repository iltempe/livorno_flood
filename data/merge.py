#!/usr/bin/python
# -*- coding: utf-8 -*-
#Reused from https://github.com/emergenzeHack/terremotocentro_geodata/blob/gh-pages/CopernicusEMS/scripts/copernicus_EMSR.py
import os
import zipfile
import shutil
import glob
import shapefile

###############################################################################

folder_input_zip = "/Users/TeoPro/Desktop/livorno/EMSR238/"
folder_output_zip = "/Users/TeoPro/Desktop/livorno/EMSR238/temp/"
array_id = ["_01","_02","_03","_04"]
folder_input_shp = folder_output_zip
folder_output_shp = "/Users/TeoPro/Desktop/livorno/EMSR238/out/"
array_elements = ['area_of_interest', 'crisis_information_poly', 'hydrography_line', 'settlements_point', 'transportation_line','utilities_point','populated_places_point','land_cover_poly']
folder_input_merge = folder_output_shp
folder_output_merge = "/Users/TeoPro/Desktop/livorno/EMSR238/out/"

###############################################################################

def extract_zipped_files (file_name):
    #pass
    print file_name
    file_name_in=folder_input_zip+file_name
    with zipfile.ZipFile(file_name_in, "r") as z:
        z.extractall(folder_output_zip)

def clean_folder ():
    #pass
    folder_del = folder_output_zip + "*.*"
    files = sorted(glob.glob(folder_del))
    for f in files:
        os.remove(f)
    for element in array_elements:
        folder_del = folder_output_shp + element + "/*.*"
        files = sorted(glob.glob(folder_del))
        for f in files:
            os.remove(f)
    for element in array_elements:
        folder_del = folder_output_merge + element + "_merged.*"
        files = sorted(glob.glob(folder_del))
        for f in files:
            os.remove(f)


clean_folder()
#exit()

for file in sorted(os.listdir(folder_input_zip)):
    for id in array_id:
        if id in file:
            if file.endswith(".zip"):
                extract_zipped_files(file)

for file in sorted(os.listdir(folder_input_shp)):
    for element in array_elements:
        if element in file:
            file_move_name_in = folder_input_shp + file
            file_move_name_out = folder_output_shp + element + "/" + file
            shutil.move(file_move_name_in,file_move_name_out)

for category in array_elements:
    folder_input_in = folder_input_merge + category + '/*.shp'
    folder_input_out = folder_output_merge + category + '_merged.shp'
    files = sorted(glob.glob(folder_input_in))
    w = shapefile.Writer()
    for f in files:
        r = shapefile.Reader(f)
        w._shapes.extend(r.shapes())
        w.records.extend(r.records())
        w.fields = list(r.fields)
    w.save(folder_input_out)
    folder_input_in = folder_input_merge + category + '/*.prj'
    folder_input_out = folder_output_merge + category + '_merged.prj'
    files = sorted(glob.glob(folder_input_in))
    for f in files:
        shutil.copy(f,folder_input_out)
        break

print "Finito !"
