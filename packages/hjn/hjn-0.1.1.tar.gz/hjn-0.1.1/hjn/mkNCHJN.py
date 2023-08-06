#coding=utf8
import numpy as np
import netCDF4 as nc
import datetime

class ttt():
	def __init__(self,a):
		print(a)

class dataClass():
	data_ = None
	name_ = None
	coordinate_ = None
	unit_ = None
	missing_value_ = np.NAN
	scala_factor_ = float(1.0)
	add_offset_ = float(0.0)

	def __init__(self,data, name, coordinate, unit,missing_value=np.NAN, scala_factor=float(1.0), add_offset=float(0.0)):
		self.data_, self.name_, self.coordinate_, self.unit_ ,self.missing_value_ ,self.scala_factor_,self.add_offset_= data, name, coordinate, unit,missing_value, scala_factor, add_offset

	def print(self):
		print(self.data_, self.name_, self.coordinate_, self.unit_,self.missing_value_,self.scala_factor_,self.add_offset_)
		
def mkNCCommonUni(output,dateTimeStart,dateTimeArr,isoArr,latArr,lonArr,dataClass4D=None,dataClass3D=None,dataClass2D=None):
    dataset = nc.Dataset(output,'w',format='NETCDF4',zlib=True) #'NETCDF4_CLASSIC')
    
    
    dataset.createDimension("time", len(dateTimeArr))
    if not isoArr is None:
        dataset.createDimension("isobaric", len(isoArr))
        
    dataset.createDimension("lat", len(latArr))
    dataset.createDimension("lon", len(lonArr))
    
    
    dataset.createVariable("time", np.float32, ("time"), zlib=True)
    if not isoArr is None:
        dataset.createVariable("isobaric", np.float32, ("isobaric"), zlib=True)
    dataset.createVariable("lat", np.float32, ("lat"), zlib=True)
    dataset.createVariable("lon", np.float32, ("lon"), zlib=True)
    
    for e in dataClass3D:
        dataset.createVariable(e.name_, np.float32, tuple(["time","lat","lon"]), zlib=True)
    
    
    dataset.variables["time"][:] = dateTimeArr
    dataset.variables["time"].units = 'hours since %s'%(dateTimeStart.strftime("%Y-%m-%d %H:%M:%S"))
    dataset.variables["time"].calendar = 'gregorian'

    if not isoArr is None:
        dataset.variables["isobaric"][:] = isoArr
        taset.variables["isobaric"].units="hPa"
        taset.variables["isobaric"].positive="up"
        
    dataset.variables["lat"][:] = latArr
    dataset.variables['lat'].units = 'degrees_north'
    
    dataset.variables["lon"][:] = lonArr
    dataset.variables['lon'].units = 'degrees_east'
        
    
    for e in dataClass3D:
        dataset.variables[e.name_][:] = e.data_
        dataset.variables[e.name_].units = e.unit_
        dataset.variables[e.name_].coordinate = e.coordinate_
        dataset.variables[e.name_].missing_value = e.missing_value_
        dataset.variables[e.name_].scala_factor = e.scala_factor_
        dataset.variables[e.name_].add_offset = e.add_offset_
    
    dataset.close()
