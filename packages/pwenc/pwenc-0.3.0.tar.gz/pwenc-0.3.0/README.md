# pwenc.py

## ABOUT
This is a simple cli program that will encrypt and manage a file, mainly for
use in keeping whatever data (passwords, random stuff, etc.) safe.

## INSTALL
This is pretty straightforward.  You can use either `pip` or `easy_install` to
install, or the classic `python setup.py install` after downloading from
github: http://github.com/crustymonkey/pwenc

## ENCRYPTED FILE
By default, this will act upon the file `$HOME/.pwenc/encrypted`.  You
can manually change this on the command-line to override this.

## COMMANDS
The following gives a brief description of the commands available.  Complete
help is available via `pwenc.py -h`.

### show
The show command will dump the unencrypted content to a pager (less, for
example).

```
usage: pwenc.py show [-h] [-i INFILE] [-p PAGER]

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        The file to show [default: /home/jay/.pwenc/encrypted]
  -p PAGER, --pager PAGER
                        Override the PAGER you have set in your environment
                        and pipe the output to a different program [default:
                        less]
```

### edit
The edit command will decrypt your file, allow you to edit it, and re-encrypt
it.

```
usage: pwenc.py edit [-h] [-i INFILE] [-e EDITOR]

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        The file to edit [default: /home/jay/.pwenc/encrypted]
  -e EDITOR, --editor EDITOR
                        Override the EDITOR you have set in your environment
                        and use this specified program to edit the file
                        [default: vim]
```

### dump
The dump command will just dump the unencrypted content a file, or stdout.

```
usage: pwenc.py dump [-h] [-i INFILE] [-o OUTFILE]

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        The file to dump [default: /home/jay/.pwenc/encrypted]
  -o OUTFILE, --outfile OUTFILE
                        Dump the contents of the encrypted file to this file
                        [default: STDOUT]
```

### enc
The enc command will encrypt a file or stdin and write to an outfile.

```
usage: pwenc.py enc [-h] [-o OUTFILE] [-i FILE]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        The file to write to [default:
                        /home/jay/.pwenc/encrypted]
  -i FILE, --infile FILE
                        Encrypt the given file [default: STDIN]
```

### upd_pass
Update the password for the given file

```
usage: pwenc.py upd_pass [-h] [-i INFILE]

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        The file to change the password for [default:
                        /home/jay/.pwenc/encrypted]
```
