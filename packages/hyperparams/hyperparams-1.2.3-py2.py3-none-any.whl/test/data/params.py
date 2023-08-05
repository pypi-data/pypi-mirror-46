from hyperparams import HyperParams

class TemplateParams(HyperParams):
    def __init__(self):
        super().__init__()
        self.win_home = "%HOME%"

class Params(TemplateParams):
    def __init__(self):
        super().__init__()
        self.linux_home = "$HOME"

class ParamsSuperSpecific(Params):
    def __init__(self):
        super().__init__()
        self.specific = True

class FakeParams(object):
    def __init__(self):
        print("Hello World!")
