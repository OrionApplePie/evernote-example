#!/usr/bin/env python 
import argparse
import json
from datetime import date, datetime, timedelta

from evernote.api.client import EvernoteClient

from config import Settings


WEEK_DAYS = {
    1: 'понедельник',
    2: 'вторник',
    3: 'среда',
    4: 'четверг',
    5: 'пятница',
    6: 'суббота',
    7: 'воскресенье',
}


def is_valid_date(text):
    text = text.strip()
    if (
        text.startswith('-')
        or text.startswith('+')
        or text.isdigit()
    ):
        return date.today() + timedelta(days=int(text))

    try:
        return datetime.strptime(text, '%Y-%m-%d').date()
    except ValueError:
        msg = f'Not a valid date: "{text}".'
        raise argparse.ArgumentTypeError(msg)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Adds note to notebook "Дневник", uses template note'
    )
    parser.add_argument('-date',
                        nargs='?',
                        type=is_valid_date,
                        help='date in format "YYYY-MM-DD"')

    parser.add_argument('-message',
                        type=str,
                        help='Text message for note.')

    args = parser.parse_args()

    config = Settings()
    dev_token = (
        config.EVERNOTE_SANDBOX_DEVELOPER_TOKEN
        if config.SANDBOX
        else config.EVERNOTE_PRODUCTION_DEVELOPER_TOKEN
    )

    client = EvernoteClient(
        token=dev_token,
        sandbox=config.SANDBOX,
    )
    noteStore = client.get_note_store()

    day = args.date or date.today()
    context = {
        'date': day.isoformat(),
        'dow': WEEK_DAYS[day.isoweekday()],
    }
    print('Title Context is:')
    print(json.dumps(context, ensure_ascii=False, indent=4))

    new_note = noteStore.copyNote(
        config.JOURNAL_TEMPLATE_NOTE_GUID,
        config.JOURNAL_NOTEBOOK_GUID
    )

    utitle_without_comment = new_note.title.split('#', 1)[0]
    utitle = utitle_without_comment.strip().format(**context)
    new_note.title = utitle

    text = args.message
    new_note.content = '<?xml version="1.0" encoding="UTF-8"?>'
    new_note.content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    new_note.content += '<en-note>'
    new_note.content += f'<div>{text}</div>'
    new_note.content += '</en-note>'

    noteStore.updateNote(new_note)

    print(f'Note created: {utitle}')
    print('Done')
