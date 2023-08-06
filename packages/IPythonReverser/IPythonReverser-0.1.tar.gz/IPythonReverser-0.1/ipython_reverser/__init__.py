from IPython.core.magic import register_line_magic


def load_ipython_extension(ipython):
    @register_line_magic("reverse")
    def lmagic(line):
        "Line magic to reverse a string"
        return line[::-1]
