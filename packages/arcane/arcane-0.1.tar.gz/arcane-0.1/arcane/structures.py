from .components import Container, Paragraph


class Page():
    title = ""
    css = ""
    js = ""

    def construct(self):
        return ""

    @staticmethod
    def load_scripts(elements):
        return " ".join([element._load_events() for element in elements])

    @classmethod
    def build(cls):
        html = Container(tag="html")

        title = Paragraph("Hello World", tag="title")
        head = Container(title, tag="head")

        script = Paragraph(tag="script")
        script._id = "arcane_scripts"

        body = Container(cls.construct(), tag="body", style="margin:0;")

        html.append_childs([head, body, script])

        return html._build(script)
