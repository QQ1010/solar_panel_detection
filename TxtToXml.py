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

class Object():
    def __init__(self,objID,polyID,position,tifID,x,y):
        self.objID = objID
        self.polyID = polyID
        self.position = position
        self.tifID = tifID
        self.x = x
        self.y = y


def txtToXml(txt_path,xml_path):
    # .txt data to save in txt_data as a Object())
    txt_data = []
    with open(txt_path) as f:
        for line in tqdm(f.readlines()):
            txt = line.strip().split(',')
            txt_data.append(Object(txt[0],txt[1],txt[2],txt[3],txt[4],txt[5]))
    f.close()
    # print(txt_data[1].objID)

    # make the xml
    # range need to change according to the number of xml
    for index in range(6634):  
        xmldoc = Document()

        annotation = xmldoc.createElement('annotation')
        xmldoc.appendChild(annotation)


        filename = xmldoc.createElement('filename')
        annotation.appendChild(filename)
        filename_txt = xmldoc.createTextNode(str(index+1).zfill(9) + '.tif')
        filename.appendChild(filename_txt)
        
        source = xmldoc.createElement('source')
        source_annotation = xmldoc.createElement('annotation')
        source_annotation_txt = xmldoc.createTextNode('ESRI ArcGIS Pro')
        source_annotation.appendChild(source_annotation_txt)
        source.appendChild(source_annotation)
        annotation.appendChild(source)

        size = xmldoc.createElement('size')
        width = xmldoc.createElement('width')
        width_txt = xmldoc.createTextNode('256')
        width.appendChild(width_txt)
        height = xmldoc.createElement('height')
        height_txt = xmldoc.createTextNode('256')
        height.appendChild(height_txt)
        depth = xmldoc.createElement('depth')
        depth_txt = xmldoc.createTextNode('4')
        depth.appendChild(depth_txt)
        size.appendChild(width)
        size.appendChild(height)
        size.appendChild(depth)
        annotation.appendChild(size)

        
        x_min = txt_data[index*4 + 1].x
        y_min = txt_data[index*4 + 1].y
        x_max = txt_data[index*4 + 1].x
        y_max = txt_data[index*4 + 1].y
        for i in range(index*4+1,index*4+5):
            if(txt_data[i].x < x_min):
                x_min = txt_data[i].x
            if(txt_data[i].x > x_max):
                x_max = txt_data[i].x
            if(txt_data[i].y < y_min):
                y_min = txt_data[i].y
            if(txt_data[i].y > y_max):
                y_max = txt_data[i].y
        
        object = xmldoc.createElement('object')
        name = xmldoc.createElement('name')
        name_txt = xmldoc.createTextNode('1')
        name.appendChild(name_txt)
        bndbox = xmldoc.createElement('bndbox')
        xmin = xmldoc.createElement('xmin')
        xmin_txt = xmldoc.createTextNode(x_min)
        xmin.appendChild(xmin_txt)
        ymin = xmldoc.createElement('ymin')
        ymin_txt = xmldoc.createTextNode(y_min)
        ymin.appendChild(ymin_txt)
        xmax = xmldoc.createElement('xmax')
        xmax_txt = xmldoc.createTextNode(x_max)
        xmax.appendChild(xmax_txt)
        ymax = xmldoc.createElement('ymax')
        ymax_txt = xmldoc.createTextNode(y_max)
        ymax.appendChild(ymax_txt)
        bndbox.appendChild(xmin)
        bndbox.appendChild(xmax)
        bndbox.appendChild(ymin)
        bndbox.appendChild(ymax)
        object.appendChild(name)
        object.appendChild(bndbox)
        annotation.appendChild(object)
        

        # create the output file
        os.chdir(xml_path)
        outputfile = str(index+1).zfill(9) + ".xml"
        with open(outputfile,'wb') as fw:
            fw.write(xmldoc.toprettyxml(indent='\t', encoding='utf-8'))
        fw.close()



if __name__ == "__main__":
    data_path = os.path.join(os.getcwd(),'Sample_Corner_Point.txt')
    pic_path = os.path.join(os.getcwd(), 'result')
    txtToXml(data_path,pic_path)