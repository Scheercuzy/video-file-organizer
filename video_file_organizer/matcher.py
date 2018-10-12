import queue
import logging
import difflib

from video_file_organizer.obj.file_system_entry \
    import FileSystemEntry


def matcher(app) -> queue.Queue:

    logging.debug("Running Matcher")
    match_queue: queue.Queue = queue.Queue()

    scan_queue = app.scan_queue

    while True:
        # scan_queue is empty, break
        if scan_queue.qsize() == 0:
            logging.debug("end of fse queue")
            break

        # Get FSE object from scan_queue
        fse = scan_queue.get()

        match_fse(app, fse)
        if not fse.valid:
            continue

        match_queue.put(fse)

    return match_queue


def match_fse(app, fse: FileSystemEntry) -> None:
    app.event.before_match(fse)
    _match_fse(app, fse)
    app.event.after_match(fse)


def _match_fse(app, fse: FileSystemEntry) -> None:
    INDEX = {
        'episode': app.series_index
    }
    index = INDEX.get(fse.type)
    if index:
        return index
    else:
        fse.valid = False
        return None

    index_match = difflib.get_close_matches(
        fse.title, index.keys(), n=1, cutoff=0.6)

    if not index_match:
        logging.warning("NO MATCH")
        fse.valid = False
    else:
        fse.matched_dir_path = index.dict[index_match[0]].path
        fse.matched_dir_name = index_match[0]
        fse.matched_dir_entry = index.dict[index_match[0]]
