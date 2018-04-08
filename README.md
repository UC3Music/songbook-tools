# songbook-tools

Tools for minimally markuped songs, like LaTeX songbook generation and chord transposition.

- [examples/](examples/) - Directory with minimally markuped song examples.

- [song-directory-to-songbook.py](song-directory-to-songbook.py) - Given a directory composed by minimally markuped songs, generate a pdf songbook via LaTeX. Parameters (all optional, complementary to CLI queries):
   ```
   -h, --help           show this help message and exit
   --input INPUT        specify the path of the default song (input) directory
   --output OUTPUT      specify the (output) pdf file [without extension]
   --template TEMPLATE  specify the LaTeX template file [specifies language, etc]
   --manifest MANIFEST  [optional] specify the path of a file-avoiding manifest file
   --yes [YES]          [optional] accept all, skip all queries
   ```

- [song-directory-transpose.py](song-directory-transpose.py) - Given a directory composed by minimally markuped songs, create a new directory with transposed chords (by number of semitones and/or capo/drop removal). Parameters (all optional, complementary to CLI queries):
   ```
   -h, --help            show this help message and exit
   --input INPUT         specify the path of the default song (input) directory
   --output OUTPUT       specify the path of the default song (output) directory
  --transpose TRANSPOSE  specify half tones of transposition
  --disableCapoDropCorrection [DISABLECAPODROPCORRECTION] specify if automatic capo/drop correction should be disabled
   --yes [YES]           accept all, skip all queries
   ```

- [extra-tools/](extra-tools/) - Directory with extra tools.


## Install dependencies

```bash
pip install -r requirements.txt --user
```
