
import mp3

def get_mp3_info(file):
	file.seek(0)
	info = mp3.mp3info(fp=file)
	file.seek(0)
	info.update(mp3.get_mp3tag(fp=file))
	return info

def is_mp3(fp):
		fp.seek(0)
		bf = fp.read(1024)
		import magic
		mc = magic.open(magic.MAGIC_MIME)
		mc.load()
		if mc.buffer(bf) != 'audio/mpeg':
			return False
		return True


