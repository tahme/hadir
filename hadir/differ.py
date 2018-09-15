#!/usr/bin/env python3
import argparse
import os, sys
from .writer import writer

def cmp(a,b):
	# Determine which folder is first in the hash list.
	# Directories are traversed depth-first, contents sorted
	# alphabetically with directories before files.
	if a==b:
		return 0
	if a is None:
		return -1
	if b is None:
		return 1
	if a == "./":
		return 1
	if b == "./":
		return -1
	parts_a = a.split("/")
	parts_b = b.split("/")
	i = 0
	a_file = False
	b_file = False
	while True:
		if len(parts_a)-1<=i:
			a_file = True
			if len(parts_a[i]) == 0: return 1
		if len(parts_b)-1<=i:
			b_file = True
			if len(parts_b[i]) == 0: return -1
		if a_file and not b_file:
			return 1
		if b_file and not a_file:
			return -1
		if parts_a[i] == parts_b[i]:
			i+=1
			continue
		if parts_a[i] < parts_b[i]:
			return -1
		else:
			return 1

def main():
	parser = argparse.ArgumentParser(description="Recursive md5 sum")
	parser.add_argument("src", type=str, help="Source hash file")
	parser.add_argument("dst", type=str, help="Destination hash file")
	parser.add_argument("-o", "--output", help="Output file")
	args = parser.parse_args()
	output_file = args.output
	try:
		src_file = None
		dst_file = None
		if not os.path.isfile(args.src):
			print("Error: '%s' does not exist or is not a file" % args.src, file=sys.stderr)
			exit(-1)
		if not os.path.isfile(args.dst):
			print("Error '%s' does not exist or is not a file"  % args.src, file=sys.stderr)
			exit(-1)
		src_file = open(args.src, "r", encoding="utf-8")
		dst_file = open(args.dst, "r", encoding="utf-8")
		path1 = None
		path2 = None
		path1_found = True
		path2_found = True
		comp = -1
		with writer(output_file) as out:
			while True:
				# Read hash files line by line. Advance the file
				# whose current line points behind in path traversal
				# order. If both files point at the same path, compare
				# hashes and advance the first file.
				while comp < 0:
					if not path1_found:
						print("- " + path1, file=out)
					src_line = src_file.readline().rstrip()
					if len(src_line) == 0:
						hash1, path1 == "", ""
						comp = 1
						break
					hash1, path1 = src_line.split(" ", 1)
					path1_found = False
					comp = cmp(path1, path2)

				while comp > 0:
					if not path2_found:
						print("+ " + path2, file=out)
					dst_line = dst_file.readline().rstrip()
					if len(dst_line) == 0:
						hash2, path2 == "", ""
						comp = -1
						break
					hash2, path2 = dst_line.split(" ", 1)
					path2_found = False
					comp = cmp(path1, path2)

				if len(src_line) == 0 and len(dst_line) == 0:
					break

				if comp == 0:
					path1_found = True
					path2_found = True
					if hash1 != hash2:
						print("! " + path1, file=out)
					comp = -1

	finally:
		if dst_file is not None:
			dst_file.close()
		if src_file is not None:
			src_file.close()

