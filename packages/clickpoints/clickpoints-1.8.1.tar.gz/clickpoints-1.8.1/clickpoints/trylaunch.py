from clickpoints.launch import main
import os

import sys

#sys.argv.append(r"D:\Repositories\ClickPointsExamples\TweezerVideos\001\track.cdb")
#sys.argv.append(r"D:\Repositories\ClickPoints\clickpoints\addons\Westernblot\western.cdb")
#sys.argv.append(r"D:\Repositories\ClickPoints\clickpoints\addons\Kymograph\20140601-20140701.cdb")
#sys.argv.append(r"D:\Repositories\ClickPointsExamples\PlantRoot\dronpa.cdb")
#sys.argv.append(r"D:\Repositories\ClickPointsExamples\TweezerVideos\002\test.cdb")
#sys.argv.append(r"D:\Repositories\ClickPointsExamples\TweezerVideos\002\frame0000.jpg")
#sys.argv.append(r"D:\TestData\Tina2\2017-07-12\test.cdb")
#sys.argv.append(r"D:\Repositories\ClickPointsExamples\OpenSlide\CMU-1\CMU-1-40x - 2010-01-12 13.24.05.vms")
#sys.argv.append(r"D:\Repositories\ClickPointsExamples\OpenSlide\CMU-1\test.cdb")
#sys.argv.append(r"D:\USB_Sicherungskopie_2019_01_11\Schatzi\output.tif")
#sys.argv.append(r"D:\Repositories\ClickPointsExamples\OpenSlide\CMU-1\CMU-1-40x - 2010-01-12 13.24.05_macro.jpg")
#sys.argv.append(r"D:\TestData\Tina2\2017-07-12\20170712-110355_Mic2_rep0116_pos0_x0_y0_mode0_zMaxIndices73.tif")
#sys.argv.append(r"D:\TestData\Tina2\2017-07-12\test_sort.cdb")

if 0:
    import shutil
    shutil.copy(r"D:\TestData\Tina2\2017-07-12\test - Kopie.cdb", r"D:\TestData\Tina2\2017-07-12\current_test.cdb")
    sys.argv.append(r"D:\TestData\Tina2\2017-07-12\current_test.cdb")

#sys.argv.append(r"D:\TestData\Tina2\2017-07-12\test.cdb")
#sys.argv.append(r"D:\Repositories\ClickPointsExamples\PlantRoot\plant_root_right.cdb")
#sys.argv.append(r"D:\TestData\MEF_Test_20000_3\20160415-173301_Mic4_rep4_pos0_x3_y0_modeFluo6_zMinProj.tif")
#sys.argv.append(r"D:\Repositories\PenguDatabase\71f4f4d9-1a99-424b-82b0-c9a2f4bb4e17.cdb")
#sys.argv.append(r"C:\Users\Richard\Downloads\tmp\IMG_6804.JPG")

if 0:
    #main(r"D:\TestData\PenguinAndPanorama\ge_pinguarival_20160401.jpg")
    main(r"D:\TestData\PenguinAndPanorama\20180815-103431_000_GX6600_snap_rotated Panorama.jpg")
    exit()
if 0:
    main(r"D:\TestData\test-images-new-camera\text.cdb")
if 1:
    main(r"D:\USB_Sicherungskopie_2019_01_11\Schatzi\output.tif")
    exit()
if 0:
    os.chdir(r"D:\2013-04-17")
    main(r"20130417-103114_Crozet_GoPro.jpg")
    exit()
if 0:
    os.chdir(r"D:\Repositories\ClickPointsExamples\TweezerVideos\001")
    main(r"frame0000.jpg")
    exit()
if 0:
    main(r"D:\TestData\Cardiomyocytes3\test.cdb")
    exit()
if 0:
    main(r"D:\TestData\test-images-new-camera\\")
    exit()


def getCurrentVersion():
    import json
    import os
    import natsort
    result = os.popen("conda search -c rrgerum -f clickpoints --json").read()
    result = json.loads(result)
    try:
        version = natsort.natsorted([f["version"] for f in result["clickpoints"]])[-1]
    except KeyError:
        return None
    return version

#import time
#time.clock()
#print("newest Version", getCurrentVersion())
#print(time.clock())
#import clickpoints
#print("current version", clickpoints.__version__)

def getCurrentVersionHG():
    import json
    import os
    import subprocess
    import natsort
    try:
        result = subprocess.check_output("hg id -n -R \""+os.path.join(os.path.dirname(__file__), "..")+"\"", stderr=subprocess.STDOUT).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        return None
    print("->", result)

def getNewestVersionHG():
    import os
    import subprocess
    try:
        result = subprocess.check_output("hg pull -R \"" + os.path.join(os.path.dirname(__file__), "..") + "\"",
                                         stderr=subprocess.STDOUT)
        result = subprocess.check_output("hg log -l 1 --template \"{rev}\" -R \"" + os.path.join(os.path.dirname(__file__), "..") + "\"",
                                         stderr=subprocess.STDOUT).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        return None
    return result

#getCurrentVersionHG()
#getNewestVersionHG()