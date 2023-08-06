import uuid
import string
import random


class Action():
    js = []

    def do(self, js):
        self.js.append(js)

    def dump(self):
        return " ".join(self.js)


class FakeScript():
    text = ""


class Mutable():
    style = {}

    def __init__(self):
        self._id = uuid.uuid1()

    def _get_element(self, id):
        return "document.getElementById('{}')".format(id)

    def _get_new_variable_name(self):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(10))

    def toggle(self, display="block"):
        var_name = self._get_new_variable_name()
        element = "let {} = {};".format(var_name, self._get_element(self._id))
        if_else = "({}.style.display != 'none' ? {}.style.display = 'none' : {}.style.display = '{}'); ".format(
            var_name, var_name, var_name, display)

        return element + if_else

    def destroy(self):
        var_name = str(uuid.uuid1()).replace("-", "")
        element = "let {} = {};".format(
            var_name, self._get_element(self._id))
        parent_remove = "{}.parentNode.removeChild({});".format(
            var_name, var_name)

        return element + parent_remove

    def create(self, container):
        scripts_tag = self._get_element("arcane_scripts")
        new_scripts = FakeScript()
        var_name = str(uuid.uuid1()).replace("-", "")

        create_element = "let {} = document.createElement('{}');".format(
            var_name, self.tag)
        set_tag = "{}.setAttribute('id', '{}');".format(var_name, self._id)
        inner_html = "{}.innerHTML = `".format(
            var_name) + self._build(new_scripts) + "`;"
        append = "{}.appendChild({});".format(self._get_element(container._id),
                                              var_name)

        return create_element + set_tag + inner_html + append

    def change_style(self, key, value):
        return "{}.style.{} = '{}';".format(self._get_element(self._id), key, value)


class Interactive(Mutable):
    def __init__(self):
        Mutable.__init__(self)

    def click(self, func):
        raw = "document.getElementById('{}').addEventListener('click', function()"
        action = Action()
        func(action)

        self.js += raw.format(self._id) + "{" + action.dump() + "});"


class Console():
    @staticmethod
    def log(log):
        return "console.log('{}')".format(log)
