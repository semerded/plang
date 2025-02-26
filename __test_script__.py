import src as pl
import time
import sdl2

pl.enable_debugging()

window = pl.Window(800, 600, fps=-1)
button = pl.Button(window, 50, 50, 200, 50, pl.Color.BEIGE, 8)
fps_counter = pl.FPScounterWidget(window, pl.corner.top_right)


while True:
    window.event_handler()
    # window.clear(pl.Color.RED)
    # print(True)
    # print()
    fps_counter.draw()
    # window.draw.rectangle(100, 100, 50, 200, pl.Color.BLUE, (0, 25, 25, 0))
    # window.draw.circle(300, 300, 50, pl.Color.RED)
    # window.draw.polygon([(0, 0), (200, 0), (100, 100), (0, 100)], pl.Color.GREEN)
    if button.is_double_clicked():
        print(True)
        
    
    # window.draw.line(200, 30, 300, 50, pl.Color.AQUAMARINE)
    button.draw()
    # print(window.sc.vw(100), window.sc.vh(100))
    


