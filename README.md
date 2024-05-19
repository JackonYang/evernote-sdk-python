Evernote2 -- another Evernote SDK for Python
============================================

## Why Evernote2?

[The official Evernote SDK for Python](https://github.com/Evernote/evernote-sdk-python3) is not that good - it has bugs.

evernote2 Features:

1. improved sdk with example code. python 3.x supported
2. Command Line Tools

- Backup ALL notes. download all notes content(index.enex), metadata(metadata.json) and resources(images/video)

## Quick Start

tested in Python 3.7.7

#### Install

pypi page: [https://pypi.org/project/evernote2/](https://pypi.org/project/evernote2/)

```bash
pip install evernote2
```

#### SDK API usage

example code: [evernote2/sample](evernote2/sample)

## Command Line Tools

#### Backup ALL notes

first,  get a *TEMP* Developer Token from [https://app.yinxiang.com/api/DeveloperToken.action](https://app.yinxiang.com/api/DeveloperToken.action)

then, run

```bash
python -m evernote2.tools.export_notes --china --token=<your-token>
```

the downloaded file structure is designed to be used by other tools easily.
such as sync with wordpress, feed to a NLP engine.

example:

```bash
$ ls notes-exported/
note_book_meta.csv  note-enex  note_meta.csv

$ tree notes-exported/note-enex/
notes-exported/note-enex/
├── note-00453956-54a2-4a72-b979-5dec0fd20174
│   ├── index.enex
│   ├── metadata.json
│   └── resources
│       ├── 0ee254e6498301cfb04213eda2c391d3.png
│       ├── 1093bc62fa171eecf345eb2eb20805af.jpg
│       ├── 11f25744e00d852ab3f6002147ac3629.png
│       ├── 21eba20903eea2d34f0e08083806afa5.gif
│       ├── 2cdae07424ed63a9fc5a9e03f069b839.jpg
│       ├── 39d7b05f5d7978fc276da98437d8b024.gif
│       ├── 442a8e6cefb5f81fdda3233cd60fdfc2.png
│       ├── 4dcd4123c3b59ce12bf4b2a7ef058197.png
│       ├── 64ee0f1c779d105353808954acce0a64.png
│       ├── 6896d894a2fb332cc1f2d908958f32a8.png
│       ├── 6a1a971805988f2ffd48dbd7eaa76d1e.png
│       ├── 6da3ff1e412275c7bdd450a4700d3c51.png
│       ├── 75ee364d944169e3cd016d5b814b1750.png
│       ├── 7ff6e6855db4574a2f73a609b47967da.gif
│       ├── 870da51a79421031a3a41bfa468c4015.png
│       ├── 8f9881485feebfca5a2cdf2a127f747c.png
│       ├── 9dd85cd8f8d623cf75742f66743b22c7.jpg
│       ├── abffe8ebc4d0dfdc1e0b4bf4d43de5d2.gif
│       ├── acd19b05f5b3e1b4013dcf58b2691f55.png
│       ├── adc828b756a58e1749ebd13b574f3cef.gif
│       ├── ba77c68da6df66831d53fb4d9a1f868d.png
│       ├── bff7ed858712ea906ce5d8979ee7c0e3.jpg
│       ├── c4ee3fbcd059ad3f698b81686c40da84.png
│       ├── cfadbad6d778b644e319210f5baebd9f.png
│       ├── e069f5750520c9da5e0ac0cd64a1a250.png
│       ├── e4728222450d86227ca3d44067849755.png
│       └── ffbcfe8da6f9775912f54e232210c49b.png
├── note-008fb159-05d5-4ae2-a9a0-70886990e10d
│   ├── index.enex
│   ├── metadata.json
│   └── resources
│       ├── 0cf728535587661ec69e6c784992d01b.png
│       ├── 1114357aa22ca38788c7633a90f71feb.png
│       ├── 1ca06683a873bf109872e40df3637dfb.jpg
│       ├── 2353fec8a29e8823b23de9e33af8aa08.png
│       ├── 7a3bbb4919deb07bf213c8767392c684.jpg
│       ├── 9014dcc411af4444b286b4451ef5821f.jpg
│       ├── a364ff721f2bcce78a67ec8041735d89.jpg
│       ├── adc29c405b88d01edb2bc158ba47163a.jpg
│       ├── b5b307207947a88a24f8e0b6b4259ef2.jpg
```

Usage:

```bash
$ python -m evernote2.tools.export_notes --help
Usage: export_notes.py [options]

Options:
  -h, --help            show this help message and exit
  -t TOKEN, --token=TOKEN
                        evernote_api_token
  -o OUTPUT_DIR, --output_dir=OUTPUT_DIR
                        dir to save notes
  -s, --sandbox         use sandbox
  -c, --china           use yinxiang.com instead of evernote.com
  -f, --force-delete    delete output_dir if exists
  -m MAX_NOTES_COUNT, --max-notes-count=MAX_NOTES_COUNT
                        max notes count to download
```
