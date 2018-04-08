# songbook-tools: extra-tools

- [pdf-index-to-file.py](pdf-index-to-file.py) - Given a pdf file, dump the index to a plain-text file. Can be used for, given a pdf songbook, generate a file-avoiding manifest file for blacklisting and avoiding duplicates, that is passed to [song-directory-to-songbook.py](/README.md#contents-and-usage) with the `--manifest` parameter. Parameters (all optional, complementary to CLI queries):
  ```
  -h, --help       show this help message and exit
  --input INPUT    name of the input pdf file (default: "songbook.pdf")
  --output OUTPUT  name of the output txt file (default: "manifest.txt")
  --yes [YES]      accept all, skip all queries (default: "NULL")
  ```

- [song-directory-strip.py](song-directory-strip.py) - Given a directory composed by minimally markuped songs, strip from all the chords.
  ```
  -h, --help       show this help message and exit
  --input INPUT    path of the default song input directory (default: "examples/")
  --output OUTPUT  path of the default song output directory (default: "out/")
  --yes [YES]      accept all, skip all queries (default: "NULL")
  ```
