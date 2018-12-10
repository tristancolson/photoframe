import os
import sys
import fnmatch
import psycopg2
import fnmatch
import exifread
from libxmp.utils import file_to_dict
from libxmp import consts
from pprint import pprint

rootdir = "/Volumes/usbdrive1/photos"
###rootdir = "/Users/tristan/photos"

try:
    dbConn = psycopg2.connect("dbname=pframedb user=pframe")
except: 
    print ("ERROR: unable to connect to database")

cur = dbConn.cursor()

# determine how many rows we have now
cur.execute("select count(*) from photos")
result = cur.fetchone()
numRows = result[0]
print ("Deleting {0} existing rows".format(numRows))

# clear existing photos out of table
cur.execute("delete from photos")
dbConn.commit()


print("Processing all photos in ",rootdir);
numPhotos = 0;
for root, dirnames, filenames in os.walk(rootdir):
    for filename in filenames:
        if filename.endswith(('.jpg', '.JPG')):
            fullPath = os.path.join(root, filename)
            print ("TCDEBUG: processing file", fullPath)
            f = open(fullPath, 'rb')
            exifTags = exifread.process_file(f, details=False)

###            print ("EXIF")
###            for tag in exifTags.keys():
###                print ("%s = %s" % (tag, exifTags[tag]))

            xmpTags = file_to_dict(fullPath)
###            print ("XMP")
###            for tag in xmpTags.keys():
###                print ("%s = %s" % (tag, xmpTags[tag]))




            title = ''
            keywords = ''
            description = ''
            if consts.XMP_NS_DC in xmpTags:
                dublinCoreProperties = xmpTags[consts.XMP_NS_DC] # dublin core properties
                for tag in dublinCoreProperties:
                    tagName = tag[0]
                    tagValue = tag[1]
                    if tagValue != "" and tagName.startswith('dc:title'):
                        title = title + tagValue
                    elif tagValue != "" and tagName.startswith('dc:subject'):
                        keywords = keywords + tagValue + " "
                    elif tagValue != "" and tagName.startswith('dc:description'):
                        description = description + tagValue


###            if title != "":
###                photoData["title"] = title
###            if keywords != "":
###                photoData["keywords"] = keywords
###            if "Image ImageDescription" in exifTags:
###                photoData["description"] = exifTags["Image Description"].printable
###            if "Image Make" in exifTags:
###                photoData["cameraMake"] = exifTags["Image Make"].printable
###            if "Image Model" in exifTags:
###                photoData["cameraModel"] = exifTags["Image Model"].printable
###            if "Image DateTime" in exifTags:
###                photoData["dateTime"] = exifTags["Image DateTime"].printable
###            if "EXIF ExposureTime" in exifTags:
###                photoData["exposureTime"] = exifTags["EXIF ExposureTime"].printable
###            if "EXIF FNumber" in exifTags:
###                photoData["fNumber"] = exifTags["EXIF FNumber"].printable
###            if "EXIF ExposureProgram" in exifTags:
###                photoData["exposureProgram"] = exifTags["EXIF ExposureProgram"].printable
###            if "EXIF ISOSpeedRatings" in exifTags:
###                photoData["isoSpeedRatings"] = exifTags["EXIF ISOSpeedRatings"].printable
###            if "EXIF MeteringMode" in exifTags:
###                photoData["meteringMode"] = exifTags["EXIF MeteringMode"].printable
###            if "EXIF Flash" in exifTags:
###                photoData["flash"] = exifTags["EXIF Flash"].printable

            print("TCDEBUG: title is ", title)
            print("TCDEBUG: keywords is ", keywords)
            print("TCDEBUG: description is ", description)
            width = 0
            if "EXIF ExifImageWidth" in exifTags:
                width = exifTags["EXIF ExifImageWidth"].printable
            height = 0
            if "EXIF ExifImageLength" in exifTags:
                height = exifTags["EXIF ExifImageLength"].printable
            type = "jpg"
            insertCmd = "Insert into photos (filename, type, width, height, title, description) values (%s, %s, %s, %s, %s, %s)"
            cur.execute(insertCmd, (fullPath, type, width, height, title, description))
            numPhotos = numPhotos + 1

dbConn.commit()
print (numPhotos, "photos added")

### ###print("Database contents")
### ###for photo in photosTable.find():
### ###    print photo
### 


cur.close()
dbConn.close()
