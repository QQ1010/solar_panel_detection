# 方法一：直接打指令 shp轉json
# > activate gdal_env
# > ogr2ogr -f GeoJSON -lco RFC7946=YES result.json output.shp


# 目前轉檔格是錯誤，無法使用，待修改
# 方法二：程式轉檔
# conda 安裝指令
# conda install -c conda-forge geopandas
import geopandas as gpd
import os

def shp2gj(input_file,output_file):
    data = gpd.read_file(input_file)
    data.to_file(output_file, driver="GeoJSON" , encoding='utf-8')
    print('Success!')

if __name__ == "__main__":
    shp_file = os.path.join(os.getcwd(),'output.shp')
    json_file = os.path.join(os.getcwd(),'test.json')
    shp2gj(shp_file,json_file)