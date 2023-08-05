import sys
import ctypes
from Phidget22.PhidgetSupport import PhidgetSupport
from Phidget22.Async import *
from Phidget22.VoltageOutputRange import VoltageOutputRange
from Phidget22.PhidgetException import PhidgetException

from Phidget22.Phidget import Phidget

class VoltageOutput(Phidget):

	def __init__(self):
		Phidget.__init__(self)
		self.handle = ctypes.c_void_p()
		self._setVoltage_async = None
		self._onsetVoltage_async = None

		__func = PhidgetSupport.getDll().PhidgetVoltageOutput_create
		__func.restype = ctypes.c_int32
		res = __func(ctypes.byref(self.handle))

		if res > 0:
			raise PhidgetException(res)

	def __del__(self):
		Phidget.__del__(self)

	def setEnabled(self, Enabled):
		_Enabled = ctypes.c_int(Enabled)

		__func = PhidgetSupport.getDll().PhidgetVoltageOutput_setEnabled
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _Enabled)

		if result > 0:
			raise PhidgetException(result)


	def getEnabled(self):
		_Enabled = ctypes.c_int()

		__func = PhidgetSupport.getDll().PhidgetVoltageOutput_getEnabled
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_Enabled))

		if result > 0:
			raise PhidgetException(result)

		return _Enabled.value

	def getVoltage(self):
		_Voltage = ctypes.c_double()

		__func = PhidgetSupport.getDll().PhidgetVoltageOutput_getVoltage
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_Voltage))

		if result > 0:
			raise PhidgetException(result)

		return _Voltage.value

	def setVoltage(self, Voltage):
		_Voltage = ctypes.c_double(Voltage)

		__func = PhidgetSupport.getDll().PhidgetVoltageOutput_setVoltage
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _Voltage)

		if result > 0:
			raise PhidgetException(result)


	def getMinVoltage(self):
		_MinVoltage = ctypes.c_double()

		__func = PhidgetSupport.getDll().PhidgetVoltageOutput_getMinVoltage
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MinVoltage))

		if result > 0:
			raise PhidgetException(result)

		return _MinVoltage.value

	def getMaxVoltage(self):
		_MaxVoltage = ctypes.c_double()

		__func = PhidgetSupport.getDll().PhidgetVoltageOutput_getMaxVoltage
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MaxVoltage))

		if result > 0:
			raise PhidgetException(result)

		return _MaxVoltage.value

	def setVoltage_async(self, Voltage, asyncHandler):
		_Voltage = ctypes.c_double(Voltage)

		_ctx = ctypes.c_void_p()
		if asyncHandler != None:
			_ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
		_asyncHandler = AsyncSupport.getCallback()

		__func = PhidgetSupport.getDll().PhidgetVoltageOutput_setVoltage_async
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _Voltage, _asyncHandler, _ctx)

		if result > 0:
			raise PhidgetException(result)


	def getVoltageOutputRange(self):
		_VoltageOutputRange = ctypes.c_int()

		__func = PhidgetSupport.getDll().PhidgetVoltageOutput_getVoltageOutputRange
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_VoltageOutputRange))

		if result > 0:
			raise PhidgetException(result)

		return _VoltageOutputRange.value

	def setVoltageOutputRange(self, VoltageOutputRange):
		_VoltageOutputRange = ctypes.c_int(VoltageOutputRange)

		__func = PhidgetSupport.getDll().PhidgetVoltageOutput_setVoltageOutputRange
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _VoltageOutputRange)

		if result > 0:
			raise PhidgetException(result)

