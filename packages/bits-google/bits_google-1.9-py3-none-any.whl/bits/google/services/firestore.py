"""Google Firestore API client."""

from bits.google.services.base import Base
from bits.helpers import chunks
from google.cloud import firestore


class Firestore(Base):
    """Firestore class."""

    def __init__(self, project, credentials=None):
        """Initialize a class instance."""
        # uses application default credentials.
        self.db = firestore.Client(project, credentials=credentials)
        self.firestore = firestore

    def get_docs(self, collection):
        """Return a list of docs in a collection."""
        ref = self.db.collection(collection)
        return list(ref.get())

    def get_docs_dict(self, collection):
        """Return a dict of docs in a collection."""
        docs = {}
        for doc in self.get_docs(collection):
            docs[doc.id] = doc
        return docs

    def _get_docs_to_add(self, data, docs):
        """Return a dict of docs to add."""
        add = {}
        for key in data:
            if key not in docs:
                add[key] = data[key]
        return add

    def _get_docs_to_delete(self, data, docs):
        """Return a dict of docs to delete."""
        delete = {}
        for key in docs:
            if key not in data:
                delete[key] = docs[key]
        return delete

    def _get_docs_to_update(self, data, docs):
        """Return a dict of docs to add."""
        update = {}
        for key in docs:
            if key not in data:
                continue
            # get new and old doc
            new = data[key]
            old = docs[key].to_dict()
            # check for diff
            if new != old:
                update[key] = new
        return update

    #
    # Perform Individual Updates
    #
    def _perform_adds(self, collection, add):
        """Perform additions."""
        for key in add:
            data = add[key]
            # add doc
            print('[%s] Add: %s' % (collection, key))
            self.db.collection(collection).document(key).set(data)

    def _perform_deletes(self, collection, delete):
        """Perform deletions."""
        for key in delete:
            # delete doc
            print('[%s] Delete: %s' % (collection, key))
            self.db.collection(collection).document(key).delete()

    def _perform_updates(self, collection, update):
        """Perform updates."""
        for key in update:
            data = update[key]
            # update doc
            print('[%s] Update: %s' % (collection, key))
            self.db.collection(collection).document(key).set(data)

    #
    # Perform Chunked Updates
    #
    def _perform_add_chunks(self, collection, add):
        """Perform chunks of additions."""
        for chunk in chunks(list(add), 500):
            batch = self.db.batch()
            for key in chunk:
                ref = self.db.collection(collection).document(key)
                batch.set(ref, add[key])
            batch.commit()
            print('[%s] Added: %s' % (collection, len(chunk)))

    def _perform_delete_chunks(self, collection, delete):
        """Perform deletions."""
        for chunk in chunks(list(delete), 500):
            batch = self.db.batch()
            for key in chunk:
                ref = self.db.collection(collection).document(key)
                batch.delete(ref)
            batch.commit()
            print('[%s] Deleted: %s' % (collection, len(chunk)))

    def _perform_update_chunks(self, collection, update):
        """Perform updates."""
        for chunk in chunks(list(update), 500):
            batch = self.db.batch()
            for key in chunk:
                ref = self.db.collection(collection).document(key)
                batch.set(ref, update[key])
            batch.commit()
            print('[%s] Updated: %s' % (collection, len(chunk)))

    def update_collection(self, collection, data, docs=None, delete_docs=False):
        """Update docs in a Firestore collection."""
        if not docs:
            docs = self.get_docs_dict(collection)

        # create get adds/deletes updates
        add = self._get_docs_to_add(data, docs)
        delete = self._get_docs_to_delete(data, docs)
        update = self._get_docs_to_update(data, docs)

        # find docs to add
        self._perform_adds(collection, add)
        self._perform_deletes(collection, delete)
        self._perform_updates(collection, update)

        # create output
        output = '[%s] Added: %s, deleted: %s, updated: %s' % (
            collection,
            len(add),
            len(delete),
            len(update),
        )

        return output

    def update_collection_batch(self, collection, data, docs=None, delete_docs=False):
        """Update docs in a Firestore collection."""
        if not docs:
            docs = self.get_docs_dict(collection)

        # create get adds/deletes updates
        add = self._get_docs_to_add(data, docs)
        delete = self._get_docs_to_delete(data, docs)
        update = self._get_docs_to_update(data, docs)

        # find docs to add
        self._perform_add_chunks(collection, add)
        self._perform_delete_chunks(collection, delete)
        self._perform_update_chunks(collection, update)

        # create output
        output = '[%s] Added: %s, deleted: %s, updated: %s' % (
            collection,
            len(add),
            len(delete),
            len(update),
        )

        return output
