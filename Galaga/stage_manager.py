import stage1


class Stage:
    def __init__(self, stage):
        self.enter = stage.enter
        self.exit = stage.exit


stages = [stage1]
current_stage_number = 0

# 현재 스테이지가 뭔지 알아내서 다음 스테이지로 넘어간다
def change_stage():
    global current_stage_number
    stages[current_stage_number].exit()
    current_stage_number += 1
    stages[current_stage_number].enter()


