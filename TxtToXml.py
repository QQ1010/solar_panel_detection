# 【.txt檔案格式】
# OBJECTID,PolygonOID,Position,TIF_ID,X,Y
# 1,0,NW,4478,191400.701700000092387,191400.701700000092387
# 2,0,NE,4478,191400.923700000159442,191400.923700000159442
# 3,0,SW,4478,191399.098100000061095,191399.098100000061095
# 4,0,SE,4478,191400.923700000159442,191400.923700000159442
# => 四個資料為一個.xml檔案
# 【.xml檔案格式】
#<?xml version="1.0" encoding="utf-8"?>
# <annotation>
# 	<filename>000000001.tif</filename>
# 	<source>
# 		<annotation>ESRI ArcGIS Pro</annotation>
# 	</source>
# 	<size>
# 		<width>256</width>
# 		<height>256</height>
# 		<depth>4</depth>
# 	</size>
# 	<object>
# 		<name>1</name>
# 		<bndbox>
# 			<xmin>191399.098100000061095</xmin>
# 			<xmax>191400.923700000159442</xmax>
# 			<ymin>191399.098100000061095</ymin>
# 			<ymax>191400.923700000159442</ymax>
# 		</bndbox>
# 	</object>
# </annotation>

from xml.dom.minidom import Document
import os
from tqdm import tqdm
from osgeo import gdal

class Object():
    def __init__(self,objID,polyID,position,tifID,x,y):
        self.objID = objID
        self.polyID = polyID
        self.position = position
        self.tifID = int(tifID)
        self.x = x
        self.y = y


def createObj(xml,obj_annotation,x_min,y_min,x_max,y_max):
    object = xml.createElement('object')
    name = xml.createElement('name')
    name_txt = xml.createTextNode('1')
    name.appendChild(name_txt)
    bndbox = xml.createElement('bndbox')
    xmin = xml.createElement('xmin')
    xmin_txt = xml.createTextNode(x_min)
    xmin.appendChild(xmin_txt)
    ymin = xml.createElement('ymin')
    ymin_txt = xml.createTextNode(y_min)
    ymin.appendChild(ymin_txt)
    xmax = xml.createElement('xmax')
    xmax_txt = xml.createTextNode(x_max)
    xmax.appendChild(xmax_txt)
    ymax = xml.createElement('ymax')
    ymax_txt = xml.createTextNode(y_max)
    ymax.appendChild(ymax_txt)
    bndbox.appendChild(xmin)
    bndbox.appendChild(xmax)
    bndbox.appendChild(ymin)
    bndbox.appendChild(ymax)
    object.appendChild(name)
    object.appendChild(bndbox)
    obj_annotation.appendChild(object)

def txtToXml(txt_path,xml_path,tif_path):
    gdal.PushErrorHandler('CPLQuietErrorHandler')
    gdal.UseExceptions()
    # .txt data to save in txt_data as a Object())
    txt_data = []
    datanum = 0
    with open(txt_path) as f:
        for line in tqdm(f.readlines()):
            txt = line.strip().split(',')
            if(txt[0] != "OBJECTID"):
                txt_data.append(Object(txt[0],txt[1],txt[2],txt[3],txt[4],txt[5]))
                datanum += 1
    f.close()
    txt_data.sort(key=lambda x:x.tifID)
    # print(datanum) 26536
    # print(txt_data[datanum].tifID) 6074

    # make the xml
    # range need to change according to the number of xml
    index = 0
    while(index < datanum):
        os.chdir(tif_path)
        tif_file = gdal.Open('Sample50_' + str(txt_data[index].tifID) +'.tif')

        xmldoc = Document()

        annotation = xmldoc.createElement('annotation')
        xmldoc.appendChild(annotation)


        filename = xmldoc.createElement('filename')
        annotation.appendChild(filename)
        filename_txt = xmldoc.createTextNode(str(txt_data[index].tifID).zfill(9) + '.tif')
        filename.appendChild(filename_txt)
        
        source = xmldoc.createElement('source')
        source_annotation = xmldoc.createElement('annotation')
        source_annotation_txt = xmldoc.createTextNode('ESRI ArcGIS Pro')
        source_annotation.appendChild(source_annotation_txt)
        source.appendChild(source_annotation)
        annotation.appendChild(source)

        # get width and height from .tif
        size = xmldoc.createElement('size')
        width = xmldoc.createElement('width')
        width_txt = xmldoc.createTextNode(str(tif_file.RasterXSize))
        width.appendChild(width_txt)
        height = xmldoc.createElement('height')
        height_txt = xmldoc.createTextNode(str(tif_file.RasterYSize))
        height.appendChild(height_txt)
        depth = xmldoc.createElement('depth')
        depth_txt = xmldoc.createTextNode('4')
        depth.appendChild(depth_txt)
        size.appendChild(width)
        size.appendChild(height)
        size.appendChild(depth)
        annotation.appendChild(size)

        x_min = min(txt_data[index].x, txt_data[index+1].x, txt_data[index+2].x, txt_data[index+3].x)
        y_min = min(txt_data[index].y, txt_data[index+1].y, txt_data[index+2].y, txt_data[index+3].y)
        x_max = max(txt_data[index].x, txt_data[index+1].x, txt_data[index+2].x, txt_data[index+3].x)
        y_max = max(txt_data[index].y, txt_data[index+1].y, txt_data[index+2].y, txt_data[index+3].y)
        
        createObj(xmldoc,annotation,x_min,y_min,x_max,y_max)
        tif = txt_data[index].tifID
        if(index + 4 < datanum):
            next_tif = txt_data[index+4].tifID
            index += 4
            while(tif == next_tif and index < datanum):
                x_min = min(txt_data[index].x, txt_data[index+1].x, txt_data[index+2].x, txt_data[index+3].x)
                y_min = min(txt_data[index].y, txt_data[index+1].y, txt_data[index+2].y, txt_data[index+3].y)
                x_max = max(txt_data[index].x, txt_data[index+1].x, txt_data[index+2].x, txt_data[index+3].x)
                y_max = max(txt_data[index].y, txt_data[index+1].y, txt_data[index+2].y, txt_data[index+3].y)
                createObj(xmldoc,annotation,x_min,y_min,x_max,y_max)
                index += 4
                if(index < datanum):
                    next_tif = txt_data[index].tifID
        else:
            os.chdir(xml_path)
            outputfile = str(txt_data[index].tifID).zfill(9) + ".xml"
            with open(outputfile,'wb') as fw:
                fw.write(xmldoc.toprettyxml(indent='\t', encoding='utf-8'))
            fw.close()
            break

        # create the output file
        os.chdir(xml_path)
        outputfile = str(txt_data[index-4].tifID).zfill(9) + ".xml"
        with open(outputfile,'wb') as fw:
            fw.write(xmldoc.toprettyxml(indent='\t', encoding='utf-8'))
        fw.close()

        #close the tif file
        tif_file = None


if __name__ == "__main__":
    data_path = os.path.join(os.getcwd(),'Sample_Corner_Point.txt')
    Tif_path = os.path.join(os.getcwd(),'tif floder')
    pic_path = os.path.join(os.getcwd(), 'result')
    txtToXml(data_path,pic_path,Tif_path)

