# songbook-tools: extra-tools

- [pdf-index-to-file.py](pdf-index-to-file.py) - Given a pdf file, dump the index to a plain-text file. Can be used for, given a pdf songbook, generate a file-avoiding manifest file for blacklisting and avoiding duplicates, that is passed to [song-directory-to-songbook.py](/README.md#contents-and-usage) with the `--manifest` parameter. Parameters (all optional, complementary to CLI queries):
  ```
  -h, --help       show this help message and exit
  --input INPUT    specify the (input) pdf file
  --output OUTPUT  specify the (output) txt file
  --yes [YES]      [optional] accept all, skip all queries
  ```

- [song-directory-strip.py](song-directory-strip.py) - Given a directory composed by minimally markuped songs, strip from all the chords.
  ```
  -h, --help       show this help message and exit
  --input INPUT    specify the path of the default song (input) directory
  --output OUTPUT  specify the path of the default song (output) directory
  --yes [YES]      [optional] accept all, skip all queries
  ```
