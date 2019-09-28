from ..utils.error import Error


class CircularReference(object):

    def __init__(self, model):
        self.model = model
        self.viewed = set()
        self.circular_reference = []

    def find(self):
        for cls in self.model.classes:
            self.viewed = set()
            self._wave(cls, cls)

        if self.circular_reference:
            self.circular_reference.append(self.circular_reference[0])
            Error.exit(Error.CIRCULAR_REFERENCE, '->'.join(self.circular_reference))

    def _wave(self, base_class, root_class):
        if root_class.name in self.viewed:
            return
        self.viewed.add(root_class.name)

        for member in root_class.members:
            if isinstance(member.type, str) and member.type == base_class.name and root_class.name != base_class.name:
                self.circular_reference.append(root_class.name)
            if self.model.has_class(member.type):
                cls = self.model.get_class(member.type)
                self._wave(base_class, cls)
