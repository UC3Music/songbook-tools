# songbook-tools

Tools for minimally markuped songs, like LaTeX songbook generation and chord transposition. See the [example](example) directory for an example of the markup.

- [song-directory-to-songbook.py](song-directory-to-songbook.py) - Given a directory composed by minimally markuped songs, generate a LaTeX songbook.

- [song-directory-transpose.py](song-directory-transpose.py) - Given a directory composed by minimally markuped songs, transpose all the chords.

- [extra-tools/songbook-dump-index.py](extra-tools/songbook-dump-index.py) - Given a generated LaTeX songbook, dump the index of the PDF to a manifest file for blacklisting and avoiding duplicates.

## Install dependencies

```bash
sudo pip install -r requirements.txt
```
