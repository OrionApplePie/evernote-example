#!/usr/bin/env python 
from evernote.api.client import EvernoteClient

from config import Settings


if __name__ == '__main__':
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
    note_store = client.get_note_store()
    notebooks = note_store.listNotebooks()

    for notebook in notebooks:
        print(f'{notebook.guid} - {notebook.name}')
