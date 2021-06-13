import os
path = os.environ['PATH']
pgdal= 'C:\\OSGeo4W64\\share\\gdal;'
os.environ['GDAL_DATA']='C:\\OSGeo4W64\\share\\gdal\\gdal-data'
os.environ['GDAL_DRIVER_PATH']='C:\\OSGeo4W64\\share\\gdal\\gdalplugins'
os.environ['PROJ_LIB']='C:\\OSGeo4W64\\share\\gdal\\projlib'
os.environ['PATH'] = "%s;%s" % (pgdal, path)