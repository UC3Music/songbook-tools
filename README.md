# songbook-tools

Tools for minimally markuped songs, like LaTeX songbook generation and chord transposition.

- [examples/](examples/) - Directory with minimally markuped song examples.

- [song-directory-to-songbook.py](song-directory-to-songbook.py)
   Given a directory composed by minimally markuped songs, generate a pdf songbook via LaTeX. Parameters (in addition to CLI):
   ```
   --input INPUT        specify the path of the default song (input) directory
   --output OUTPUT      specify the (output) pdf file (without extension)
   --template TEMPLATE  specify the template file
   --manifest MANIFEST  (optional) specify the path of a file-avoiding manifest file
   --yes [YES]          (optional) accept all, skip all queries
   ```

- [song-directory-transpose.py](song-directory-transpose.py) - Given a directory composed by minimally markuped songs, create a new directory with transposed chords (by number of semitones and/or capo/drop removal).

- [extra-tools/](extra-tools/) - Directory with extra tools.


## Install dependencies

```bash
pip install -r requirements.txt --user
```
