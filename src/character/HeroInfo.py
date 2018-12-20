import time


class BaseInfo:
    def __init__(self, speed, name):
        self.speed = 17 / 1000
        self.name = "hero"
        self.time = time.time()

    def control_walk_speed(self):
        c_time = time.time()
        d_time = c_time - self.time
        if d_time > self.speed:
            self.time = c_time
            return True
        else:
            return False


class WarriorInfo(BaseInfo):
    def __init__(self, name):
        super().__init__(8, name)


class XiangYu(WarriorInfo):
    def __init__(self):
        super().__init__("项羽")
