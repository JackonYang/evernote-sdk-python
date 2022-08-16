import os
import shutil
import csv
import math
import time
import json
import copy
import mimetypes

from optparse import OptionParser

from evernote2.api.client import EvernoteClient
from evernote2.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
from evernote2.edam.type.ttypes import NoteSortOrder
from evernote2.edam.error.ttypes import EDAMSystemException, EDAMErrorCode, EDAMUserException

import logging


enex_file_basename = 'index.enex'
meta_file_basename = 'metadata.json'
token_url = 'https://app.yinxiang.com/api/DeveloperToken.action'


def main():
    parser = OptionParser()

    parser.add_option('-t', '--token', dest='token', help='evernote_api_token')
    parser.add_option('-o', '--output_dir', dest='output_dir', help='dir to save notes', default='./notes-exported')
    parser.add_option('-s', '--sandbox', dest='is_sandbox', help='use sandbox', action='store_true', default=False)
    parser.add_option('-c', '--china', dest='is_china', help='use yinxiang.com instead of evernote.com', action='store_true', default=False)
    parser.add_option('-f', '--force-delete', dest='is_force_delete', help='delete output_dir if exists', action='store_true', default=False)
    parser.add_option('-m', '--max-notes-count', dest='max_notes_count', help='max notes count to download', default='10000')
    parser.add_option('-v', '--verbose', dest='verbose', help='show verbose logs', action='store_true', default=False)

    (options, args) = parser.parse_args()

    token = options.token
    output_dir = options.output_dir
    is_sandbox = options.is_sandbox
    is_china = options.is_china
    is_force_delete = options.is_force_delete
    max_notes_count = int(options.max_notes_count)
    verbose = options.verbose

    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(level=log_level, format="%(asctime)s | %(levelname)s | %(message)s")

    if token is None:
        logging.error('error! token is None')
        parser.print_help()
        exit(1)

    logging.info('sandbox: %s, china: %s, output_dir: %s' % (
        is_sandbox, is_china, output_dir
    ))

    init_output_dir(output_dir, is_force_delete)
    download_notes(token=token, sandbox=is_sandbox, china=is_china, output_dir=output_dir, max_notes_count=max_notes_count)


def init_output_dir(output_dir, is_force_delete):
    # do not raise exception if output_dir exists
    # if os.path.exists(output_dir):
    #     if not is_force_delete and len(os.listdir(output_dir)) > 0:
    #         raise Exception('%s exists and not exmpty' % output_dir)

    if is_force_delete and os.path.exists(output_dir):
        logging.warning('drop dir: %s' % output_dir)
        shutil.rmtree(output_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def download_notes(token, sandbox, china, output_dir, max_notes_count):
    try:
        client = EvernoteClient(token=token, sandbox=sandbox, china=china)
        note_store = client.get_note_store()
    except EDAMUserException:
        logger.exception('invalid token')
        logger.info('get a new token from: %s' % token_url)
        return

    note_books = note_store.listNotebooks()
    save_notebooks(note_books, output_dir)

    note_books_map = {n.guid: n.name for n in note_books}

    note_metas = download_metadata(note_store, max_notes_count, note_books_map)
    save_notemetas(note_metas, output_dir)

    enex_root = os.path.join(
        output_dir, 'note-enex',
    )
    if not os.path.exists(enex_root):
        os.makedirs(enex_root)

    download_all_note_enex(note_store, enex_root, note_metas)
    # total_cnt_notebooks = len(note_books)
    # for nb_idx, notebook in enumerate(note_books):
    #     nb_seq = nb_idx + 1

    #     logging.info('download notebook: (%s/%s) %s' % (nb_seq, total_cnt_notebooks, notebook.name))


def save_notebooks(note_books, output_dir):
    fn = os.path.join(output_dir, 'note_book_meta.csv')

    header = [
        'guid',
        'name',
        'stack',
        'contact',
    ]

    with open(fn, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow(header)
        for notebook in note_books:
            record = [getattr(notebook, i) for i in header]
            csvwriter.writerow(record)

    logging.info('%s notebook meta saved in %s' % (len(note_books), fn))


def download_metadata(note_store, max_count, note_books_map):
    batch_cnt = 100
    max_count = max_count or 10000  # ensure valuable default

    loops = math.ceil(max_count / batch_cnt)
    metas = []

    for i in range(loops):
        offset = i * batch_cnt
        result_list = download_metadata_batch(note_store, offset, batch_cnt)

        for idx, note in enumerate(result_list.notes):
            note_meta = {
                # 'idx': offset + idx + 1,
                'guid': note.guid,
                'title': note.title,
                'contentLength': note.contentLength,
                'created': note.created,
                'updated': note.updated,
                'updateSequenceNum': note.updateSequenceNum,
                'tagGuids': note.tagGuids,
                'notebookGuid': note.notebookGuid,
                'notebookName': note_books_map[note.notebookGuid],
                'attrAuthor': note.attributes.author,
                'attrSource': note.attributes.source,
                'attrSourceURL': note.attributes.sourceURL,
                'attrSourceApplication': note.attributes.sourceApplication,
                'attrShareDate': note.attributes.shareDate,
                # 'attributes': note.attributes,
                # 'largestResourceMime': note.largestResourceMime,
                # 'largestResourceSize': note.largestResourceSize,
            }
            metas.append(note_meta)

        if len(result_list.notes) < 100:
            break

    return metas[:max_count]


def download_metadata_batch(note_store, offset=0, batch_cnt=100):
    # note is an instance of NoteMetadata
    # result_list is an instance of NotesMetadataList

    updated_filter = NoteFilter(order=NoteSortOrder.UPDATED)
    result_spec = NotesMetadataResultSpec(
        includeTitle=True,
        includeContentLength=True,
        includeCreated=True,
        includeUpdated=True,
        includeUpdateSequenceNum=True,
        includeNotebookGuid=True,
        includeTagGuids=True,
        includeAttributes=True,
        # includeLargestResourceMime=True,
        # includeLargestResourceSize=True,
    )

    result_list = note_store.findNotesMetadata(updated_filter, offset, batch_cnt, result_spec)

    return result_list


def save_notemetas(note_metas, output_dir):
    fn = os.path.join(output_dir, 'note_meta.csv')

    fieldnames = [
        'guid',
        'title',
        'contentLength',
        'created',
        'updated',
        'updateSequenceNum',
        'tagGuids',
        'notebookGuid',
        'notebookName',
        'attrAuthor',
        'attrSource',
        'attrSourceURL',
        'attrSourceApplication',
        'attrShareDate',
    ]

    with open(fn, 'w') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        for record in note_metas:
            csvwriter.writerow(record)

    logging.info('%s note metas saved in %s' % (len(note_metas), fn))


def download_all_note_enex(note_store, enex_root, note_metas):
    total_cnt = len(note_metas)

    new_cnt = 0

    for idx, meta in enumerate(note_metas):
        title = meta['title']
        guid = meta['guid']
        note_dir = os.path.join(
            enex_root, 'note-%s' % guid)

        text_file = os.path.join(note_dir, enex_file_basename)

        if os.path.exists(text_file):
            logging.debug('(%s/%s) skip download since exists: %s, %s' % (
                idx + 1, total_cnt, text_file, title))
            continue

        # download if not exists
        downloaded = False
        while not downloaded:
            try:
                download_one_note_enex(note_store, note_dir, guid, note_meta=meta)
            except EDAMSystemException as e:
                if e.errorCode == EDAMErrorCode.RATE_LIMIT_REACHED:
                    duration = e.rateLimitDuration
                    logging.info('Rate limit reacheded, sleep %s seconds and retry' % duration)
                    time.sleep(duration)
            else:
                downloaded = True
                logging.info('(%s/%s) saved: %s, %s' % (idx + 1, total_cnt, note_dir, title))

        new_cnt += 1

    logging.info('%s new notes downloaded' % new_cnt)


def download_one_note_enex(note_store, note_dir, note_guid, note_meta):
    """

    notes:

        save `enex_file_basename` at the end of all,
        so that we can check this file to know if the cache is good when resume running
    """
    note = note_store.getNote(
        note_guid,
        True,  # withContent=True,
        True,  # withResourcesData=True,
        False,  # withResourcesRecognition=False,
        False,  # withResourcesAlternateData=False,
    )

    content = note.content  # string
    contentHash = note.contentHash  # string
    contentHashHex = bytes.hex(contentHash)
    contentLength = note.contentLength  # i32
    # notebookGuid = note.notebookGuid
    # tagGuids = note.tagGuids  # list<Guid>
    tagNames = note.tagNames  # List<string>
    resources = note.resources  # list<Resource>

    # build metadata structure
    metadata = copy.deepcopy(note_meta)
    metadata['contentHashHex'] = contentHashHex
    metadata['contentLength'] = contentLength
    # metadata['notebookGuid'] = notebookGuid
    # metadata['tagGuids'] = tagGuids
    metadata['tagNames'] = tagNames
    # metadata['resourcesCount'] = len(resources)

    # save resources
    note_resource_dir = os.path.join(note_dir, 'resources')
    if not os.path.exists(note_resource_dir):
        os.makedirs(note_resource_dir)

    resource_metas = []

    for r in resources or []:
        r_meta = save_resources(r, note_resource_dir)
        resource_metas.append(r_meta)

    metadata['resourceMetas'] = resource_metas

    # print(metadata)
    # save metadata
    meta_filename = os.path.join(note_dir, meta_file_basename)
    with open(meta_filename, 'w') as fw:
        json.dump(metadata, fw, indent=4, ensure_ascii=False)

    # save enex file
    text_file = os.path.join(note_dir, enex_file_basename)
    with open(text_file, 'w') as f_enex:
        f_enex.write(content)


def save_resources(resource, note_resource_dir):

    body = resource.data.body
    bodyHash = resource.data.bodyHash  # bytes
    bodyHashHex = bytes.hex(bodyHash)
    bodySize = resource.data.size

    width = resource.width
    height = resource.height
    duration = resource.duration

    updateSequenceNum = resource.updateSequenceNum

    mime = resource.mime
    sourceURL = resource.attributes.sourceURL
    originalName = resource.attributes.fileName
    isAttachment = resource.attributes.attachment

    res_meta = {
        'bodyHashHex': bodyHashHex,
        'bodySize': bodySize,

        'width': width,
        'height': height,
        'duration': duration,

        'updateSequenceNum': updateSequenceNum,

        'mime': mime,
        'sourceURL': sourceURL,
        'originalName': originalName,
        'isAttachment': isAttachment,
    }

    ext = mimetypes.guess_extension(mime) or '.binary'
    filename = os.path.join(note_resource_dir, '%s%s' % (bodyHashHex, ext))
    with open(filename, 'wb') as fw:
        fw.write(body)

    return res_meta


if __name__ == '__main__':
    main()
