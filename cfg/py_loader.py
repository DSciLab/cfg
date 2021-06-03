class PYLoader(object):
    def load_py(self, file_path: str) -> dict:
        self.file_path = file_path
        with open(file_path, 'r') as f:
            data = self.exec_py(f.read())
        return data

    @staticmethod
    def exec_py(__content: str) -> dict:
        exec(__content)
        __data = locals()
        del __data['_PYLoader__content']
        return __data
