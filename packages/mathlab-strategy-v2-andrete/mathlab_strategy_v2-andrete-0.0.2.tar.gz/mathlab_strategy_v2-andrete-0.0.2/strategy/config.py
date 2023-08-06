from .singleton import Singleton


class Config(Singleton):
    def __init__(self):
        self.lazy_eval_enabled = False

    def setLazyEval(self, option: bool):
        self.lazy_eval_enabled = option

    def isLazyEval(self):
        return self.lazy_eval_enabled
