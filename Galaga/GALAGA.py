import pico2d
import framework
import state_Logo


# open_canvas 하고 이미지 로드해야한다
pico2d.open_canvas(framework.CLIENT_WIDTH, framework.CLIENT_HEIGHT)

framework.run(state_Logo)

pico2d.close_canvas()