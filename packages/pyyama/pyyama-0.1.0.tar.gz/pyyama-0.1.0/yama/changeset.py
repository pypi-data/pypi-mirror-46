import copy


class ChangeSets:
    """ChangeSets class.

    ChangeSets class is used to handle YAMA ChangeSets through a
    ChangeSets object. This object is a collection of ChangeSet-s with
    methods to handle group of changesets.

    Args:
        changesets (dict): A dictionary of changesets with the specified YAMA
        changeset syntax.

    Returns:
        ChangeSets (object): Expandable ChangeSets object is returned.
    """
    def __init__(self, changesets_dict):
        if isinstance(changesets_dict, dict):
            self._raw_changesets = copy.deepcopy(changesets_dict)
            self.__bool__ = True
            changesets = []
            for change_id, changeset in changesets:
                single_changeset = ChangeSet(changeset)
                changesets.append(single_changeset)
            self._changesets = copy.deepcopy(changeset)

    def raw_changesets(self):
        return self._raw_changesets

    def changesets(self):
        return self._changesets


class ChangeSet:
    """ChangeSet class.

    ChangeSet class is used to handle a single YAMA ChangeSet through a
    ChangeSet object. This object is a single ChangeSet with
    methods to handle a group of changes with changeset specific metadata
    such as version, date.

    Args:
        changeset (dict): A dictionary of changeset with the specified YAMA
        changeset syntax.

    Returns:
        ChangeSet (object): Expandable ChangeSet object is returned.
    """
    def __init__(self, changeset):
        if isinstance(changeset, dict):
            self._raw_changeset = copy.deepcopy(changeset)
            self.__bool__ = True

    def raw_changeset(self):
        return self._raw_changeset
