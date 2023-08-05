import numpy as np
from PIL.Image import Image as PIL_Image

def dimensions(im):
	if isinstance(im, np.ndarray):
		if im.ndim != 3:
			import pdb; pdb.set_trace()
		assert im.ndim == 3, "Only RGB images are currently supported!"
		return im.shape
	elif isinstance(im, PIL_Image):
		w, h = im.size
		c = len(im.getbands())
		# assert c == 3, "Only RGB images are currently supported!"
		return h, w, c
	else:
		raise ValueError("Unknown image instance ({})!".format(type(im)))

def asarray(im, dtype=np.uint8):
	if isinstance(im, np.ndarray):
		return im.astype(dtype)
	elif isinstance(im, PIL_Image):
		return np.asarray(im, dtype=dtype)
	else:
		raise ValueError("Unknown image instance ({})!".format(type(im)))
