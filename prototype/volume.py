import os, stat

class Device:
	major = 0
	minor = 0
	node  = ''

	def __init__(self, major, minor):
		self.major = major
		self.minor = minor
		self.node = '/dev/block/mvold/%s:%s'%(major, minor)

	@staticmethod
	def create(event):
		major = event['MAJOR']
		minor = event['MINOR']
		return Device(major, minor)

	def mknod(self):
		os.mknod(self.node, mode = stat.S_IFBLK | 0666,
				device = os.makedev(int(self.major), int(self.minor)))
	
	def getNode(self):
		return self.node

	def __repr__(self):
		return 'Device(' + ','.join((self.major, self.minor)) + ')'

class Volume:
	size = 0
	filesystem = None

	def __init__(self, event):
		self.device = Device.create(event)

	def getDisk(self):
		pass
	
	def getFilesystem(self):
		pass
	
	def setFilesystem(self, filesystem):
		self.filesystem = filesystem
	
	def format(self, label = None):
		pass
	
	def check(self, force = False):
		pass
	
	def setLabel(self, label):
		pass
	
	def getLabel(self):
		pass
	
	def getUuid(self):
		pass
	
	def mount(self, mntpnt = None):
		pass
	
	def unmount(self, force = False):
		pass

	def getDevice(self):
		return self.device

	def destroy(self):
		pass

class Disk:
	vendor = ''
	model = ''
	removable = True
	size = 0

	def __init__(self, event):
		self.device = Device.create(event)

	def getVolumes(self):
		pass

	def getDevice(self):
		return self.device

	def destroy(self):
		pass
