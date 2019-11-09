import pico2d
import framework
import state_Start


# open_canvas 하고 이미지 로드해야한다
pico2d.open_canvas(framework.CLIENT_WIDTH, framework.CLIENT_HEIGHT)

framework.run(state_Start)

pico2d.close_canvas()