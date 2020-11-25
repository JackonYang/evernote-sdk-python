Evernote2 -- another Evernote SDK for Python
============================================

## Why Evernote2?


the official evernote sdk for python is not that good.


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

first,  a *TEMP* Developer Token from [https://app.yinxiang.com/api/DeveloperToken.action](https://app.yinxiang.com/api/DeveloperToken.action)]

then, run

```bash
python -m evernote2.tools.export_notes --china --token=<your-token>
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
