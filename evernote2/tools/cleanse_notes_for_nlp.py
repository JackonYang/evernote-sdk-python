import os
import json

from optparse import OptionParser

from evernote2.nlp.text_cleansing_pipe.api import clean_long_html_for_nlp

import logging


enex_file_basename = 'index.enex'
meta_file_basename = 'metadata.json'


def main():
    parser = OptionParser()

    parser.add_option('-n', '--note_store_dir', dest='note_store_dir', help='dir of downloaded note_store', default='./notes-exported')

    parser.add_option('-v', '--verbose', dest='verbose', help='show verbose logs', action='store_true', default=False)

    (options, args) = parser.parse_args()

    note_store_dir = options.note_store_dir
    verbose = options.verbose

    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(level=log_level, format="%(asctime)s | %(levelname)s | %(message)s")

    logging.info('cleansing: %s' % (
        note_store_dir
    ))

    clean_notes(note_store_dir)


def clean_notes(note_store_dir):
    input_dir_root = os.path.join(note_store_dir, 'note-enex')
    output_dir_root = os.path.join(note_store_dir, 'note-cleansed')

    for note_dir in os.listdir(input_dir_root):
        input_note_dir = os.path.join(input_dir_root, note_dir)
        output_note_dir = os.path.join(output_dir_root, note_dir)

        clean_one_note(input_note_dir, output_note_dir)


def clean_one_note(input_note_dir, output_note_dir):
    with open(os.path.join(input_note_dir, meta_file_basename), 'r') as fr:
        metadata = json.load(fr)

    title = metadata['title']
    source_url = metadata['attrSourceURL']

    content = clean_long_html_for_nlp(
        read_note_content(input_note_dir))

    if not os.path.exists(output_note_dir):
        os.makedirs(output_note_dir)

    out_file = os.path.join(output_note_dir, 'index.txt')
    with open(out_file, 'w') as fw:
        fw.write(title or '')
        # fw.write("\n")
        # fw.write(source_url or '')
        fw.write("\n")
        fw.write("\n")
        fw.write(content or '')

    logging.info('cleansed_file saved: %s' % out_file)


def read_note_content(note_dir):
    with open(os.path.join(note_dir, 'index.enex'), 'r') as fr:
        return '\n'.join(fr.readlines())


if __name__ == '__main__':
    main()
