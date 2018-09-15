# hadir

Traverse a directory recursively and print a hash for each subdirectory (and optionally for each file).
The hash for a directory is computed from:
- the hashes of names of its subdirectories
- the hashes of name and contents of each file in the directory.

Optionally, if maximum directory depth is set using the -d flag, the directories at the depth limit also recursively include their subdirectories in hash computation. The hash for a file is simply the hash of its contents.

Includes _hadir-diff_ for comparing generated hash files for added, removed or changed files. This is useful for verifying backups without a direct network connection.

Requires Python 3.2+, has no external dependencies.

## Development install

```
git clone git@github.com:yfkar/hadir.git
pip install -e hadir
```

## Usage examples

Recursively print a hash for subdirectories and files in directory 'whee' up to depth of 3, output to whee.hash:
```
hadir whee -f -d3 -o whee.hash
```

Print list of changed, removed or added files between whee.hash and whee-backup.hash to stdout.
```
hadir-diff whee.hash whee-backup.hash
```

If your installation doesn't have pip, you can just run the included scripts:
```
python hadir.py
python hadir-diff.py
```

## License

The code is licensed under the MIT license.