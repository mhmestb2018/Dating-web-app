class Member():
    _class_id = 0
    
    def __init__(self):
        self._id = self._class_id
        Member._class_id += 1
        self._name = str(self.id)

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id


if __name__ == "__main__":
    test = Member()
    test2 = Member()
    print(test.id, test2.name)