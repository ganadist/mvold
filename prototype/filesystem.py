import os

MS_DEFAULT = 0
# from sys/mount.h
MS_RDONLY = 1
MS_NOSUID = 2
MS_NODEV  = 4
MS_NOEXEC = 8
MS_REMOUNT = 32
MS_NOATIME = 1024
MS_BIND    = 4096

FlagDict = {
	MS_RDONLY	:'ro',
	MS_NOSUID	:'nosuid',
	MS_NODEV	:'nodev',
	MS_NOEXEC	:'noexec',
	MS_REMOUNT	:'remount',
	MS_NOATIME	:'noatime',
	MS_BIND		:'bind',
	MS_DEFAULT	:'default'
}

#for k, v in FlagDict.iteritems():
#	FlagDict[v] = k

class Interface:
	fstype = ''
	mount_cmd = 'mount'
	fsck_cmd = 'fsck'
	mkfs_cmd = ''

	@classmethod
	def __build_mount_command(cls, device, mntpnt, flags, options):
		flag_string = []
		for flag in FlagDict:
			if (flag & flags):
				flag_string.append(FlagDict[flag])

		return '%(mount)s -t %(fstype)s -o %(options)s %(device)s %(mntpnt)s'%{
				'mount': cls.mount_cmd,
				'fstype': cls.fstype,
				'options': ','.join(flag_string) + ',' + options,
				'device': device,
				'mntpnt': mntpnt,
		}

	@classmethod
	def mount(cls, device, mntpnt, flags, options):
		cmd = cls.__build_mount_command(device, mntpnt, flags, options)
		return os.system(cmd)
	
	@staticmethod
	def check(device, fix = False):
		raise NotImplemented

	@staticmethod
	def format(device, label = None):
		raise NotImplemented

	@staticmethod
	def setLabel(device, name):
		raise NotImplemented

	@staticmethod
	def getLabel(device):
		raise NotImplemented
	
	@staticmethod
	def getUuid(device):
		raise NotImplemented
	
	@staticmethod
	def unmount(device, force = False):
		if force:
			cmd = 'umount -l -f "%s"'%device
		else:
			cmd = 'umount "%s"'%device
		return os.system(cmd)

class Fat(Interface):
	fstype = 'vfat'
	fsck_cmd = 'fsck.vfat'

	@classmethod
	def check(cls, device, fix = False):
		if fix:
			options = '-p -w'
		else:
			options = '-n'
		cmd = '%(fsck)s %(options)s %(device)s'%{
				'fsck': cls.fsck_cmd,
				'options': options,
				'device': device,
		}
		print cmd
		return os.system(cmd)

	@staticmethod
	def format(device, label = None):
		pass

	@staticmethod
	def setLabel(device, name):
		raise NotImplemented

class Isofs(Interface):
	fstype = 'iso9660'

class Ext3(Interface):
	fstype = 'ext3'

class Ext4(Ext3):
	fstype = 'ext4'

class Exfat(Interface):
	fstype = 'exfat'
	@staticmethod
	def mount(device, mntpnt, flags, options):
		raise NotImplemented

class Ssh(Interface):
	fstype = 'sshfs'
	@staticmethod
	def mount(device, mntpnt, flags, options):
		raise NotImplemented

class Ntfs(Interface):
	fstype = 'ntfs'
	mount_cmd = 'mount.ntfs-3g'
	@staticmethod
	def mount(device, mntpnt, flags, options):
		raise NotImplemented

if __name__ == '__main__':
	Fat.check('/dev/sda')
	Fat.mount('/dev/sda', '/media/sda', MS_BIND | MS_RDONLY, 'default')
