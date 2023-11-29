import hashlib

from shipit.data import *

from contextlib import contextmanager


def get_model(model_cls, model_id):
    session = get_session()
    model = session.get(model_cls, model_id)
    return model


def delete_model(model_cls, model_id):
    session = get_session()
    model = session.get(model_cls, model_id)
    if model:
        session.delete(model)

        session.commit()


def add_model(model):
    session = get_session()  # Assuming you have a function to get a database session
    try:
        session.add(model)  # Add the provided model to the session
        session.commit()  # Commit changes on success
        session.refresh(model)  # Refresh the provided model

    except Exception as e:
        session.rollback()  # Rollback changes on failure
        raise e
    finally:
        session.close()


@contextmanager
def update_model(model_cls, model_id):
    session = get_session()  # Assuming you have a function to get a database session
    try:
        existing_model = session.query(model_cls).get(model_id)
        if existing_model is None:
            raise ValueError(f"{model_cls.__name__} with ID {model_id} not found")

        yield existing_model

        doc_id = hashlib.sha256(str(model_id).encode()).hexdigest()[:20]

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
