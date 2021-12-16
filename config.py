from pydantic import BaseSettings


class Settings(BaseSettings):
    SANDBOX: bool

    EVERNOTE_SANDBOX_DEVELOPER_TOKEN: str
    EVERNOTE_PRODUCTION_DEVELOPER_TOKEN: str

    JOURNAL_TEMPLATE_NOTE_GUID: str
    JOURNAL_NOTEBOOK_GUID: str

    INBOX_NOTEBOOK_GUID: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
