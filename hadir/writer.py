import contextlib
import sys

@contextlib.contextmanager
def writer(filename=None):
	if filename is None:
		f = sys.stdout
		yield f
	else:
		try:
			f = open(filename, "w", encoding="utf-8")
			yield f
		finally:
			f.close()

