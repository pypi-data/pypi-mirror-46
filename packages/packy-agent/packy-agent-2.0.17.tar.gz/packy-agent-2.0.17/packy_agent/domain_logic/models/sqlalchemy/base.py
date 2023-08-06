import sys
import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session as SQLAlchemySession, make_transient


logger = logging.getLogger(__name__)


class Session(SQLAlchemySession):

    def __init__(self, bind=None, **kwargs):
        kwargs.setdefault('autocommit', False)
        # `expire_on_commit` is needed to avoid db queries when accessing model instance
        # attributes after session commit
        kwargs.setdefault('expire_on_commit', False)
        super(Session, self).__init__(bind=bind, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close_commit_or_rollback(exc_type, exc_value, exc_traceback)

    def close_commit_or_rollback(self, exc_type=None, exc_value=None, exc_traceback=None):
        session_objects = list(self)

        commit_exc_type = None
        commit_exc_value = None
        commit_exc_traceback = None
        if exc_type:
            logger.exception('Rolling back after exception:',
                             exc_info=(exc_type, exc_value, exc_traceback))
            self.expunge_all()  # Remove all objects from session (must be called before rollback)
            self.rollback()
            # No need to raise exception explicitly it will be "reraised" implicitly
            # on return from __exit__()
        else:
            try:
                self.commit()
            except:
                commit_exc_type, commit_exc_value, commit_exc_traceback = sys.exc_info()
                try:
                    logger.exception('Error while committing, rolling back',
                                     exc_info=(commit_exc_type, commit_exc_value,
                                               commit_exc_traceback))
                    self.expunge_all()
                    self.rollback()
                except:
                    commit_exc_type, commit_exc_value, commit_exc_traceback = sys.exc_info()
                    logger.exception('Error while rolling back after error while committing '
                                     '(we did our best to recover)',
                                     exc_info=(commit_exc_type, commit_exc_value,
                                               commit_exc_traceback))

        # Disconnect session objects from session completely (stronger than `expunge()`)
        for obj in session_objects:
            make_transient(obj)

        self.close()

        if commit_exc_type:
            raise commit_exc_value.with_traceback(commit_exc_traceback)


ModelBase = declarative_base()
