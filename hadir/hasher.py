#!/usr/bin/env python3

import argparse
import hashlib
import os, sys
from .writer import writer


def hash_string(string, hash_fun=hashlib.sha1):
	hash = hash_fun()
	hash.update(bytes(string, encoding='utf-8'))
	return hash

def hash_file(filename, hash_fun, blocksize=65536):
	hash = hash_fun()
	with open(filename, "rb") as f:
		for block in iter(lambda: f.read(blocksize), b""):
			hash.update(block)
	return hash

def main():
	parser = argparse.ArgumentParser(description="Generate hashes from a directory tree.")
	parser.add_argument("directory", type=str, help="target directory")
	parser.add_argument("-d", "--depth", type=int, help="directory depth")
	parser.add_argument("-f", "--file-hashes", help="also output file hashes", action="store_true")
	parser.add_argument("-o", "--output", help="output file")
	parser.add_argument("-H", "--hash",
		choices=["sha1", "sha256", "sha512","md5"], default="sha1", help="hash algorithm, sha1 is the default")
	args = parser.parse_args()

	max_depth = args.depth
	output_file = args.output
	file_hashes = args.file_hashes
	hash_fun = {
		'sha1': hashlib.sha1,
		'sha256': hashlib.sha256,
		"sha512": hashlib.sha512,
		"md5": hashlib.md5
	}[args.hash]

	with writer(output_file) as out:
		root = args.directory
		# Recurse directory contents in lexicographical order with directories first.
		def recurse(path, hash_fun, depth=0):
			items = os.listdir(path)
			items.sort()
			hash = hash_fun()

			paths = [name for name in items if os.path.isdir(os.path.join(path, name))]
			for p in paths:
				try:
					hash_sum = recurse(os.path.join(path,p), hash_fun=hash_fun, depth=depth+1)
					hash.update(hash_string(os.path.basename(p), hash_fun=hash_fun).digest())
					if max_depth is not None and depth >= max_depth:
						hash.update(hash_sum.digest())
				except (OSError, IOError) as e:
					print("skipping: %s" % e, file=sys.stderr)

			files = [name for name in items if not os.path.isdir(os.path.join(path, name))]
			for f in files:
				try:
					file_path = os.path.join(path, f)
					hash.update(hash_string(os.path.basename(file_path), hash_fun).digest())
					hash_sum = hash_file(file_path, hash_fun)
					if file_hashes and (max_depth is None or depth < max_depth):
						print(hash_sum.hexdigest() + " " + os.path.relpath(file_path, root).replace(os.sep, "/"), file=out)
					hash.update(hash_sum.digest())
				except (OSError, IOError) as e:
					print("skipping: %s" % e, file=sys.stderr)

			if max_depth is None or depth <= max_depth:
				print(hash.hexdigest() + " " + os.path.relpath(path, root).replace(os.sep, "/") + "/", file=out)
			return hash

		recurse(root, hash_fun)
