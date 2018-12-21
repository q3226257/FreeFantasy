import time


class BaseInfo:
    def __init__(self, speed, name):
        self.speed = 200/1000
        self.name = "hero"
        self.time = time.time()


class WarriorInfo(BaseInfo):
    def __init__(self, name):
        super().__init__(8, name)


class XiangYu(WarriorInfo):
    def __init__(self):
        super().__init__("项羽")
