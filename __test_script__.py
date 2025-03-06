import src as pl
import time

pl.enable_debugging()

window = pl.Window(800, 600, fps=144)
button = pl.Button(window, 50, 50, 200, 50, pl.Color.RED, 8)
button.set_text("hi this is ", pl.Font(pl.fonts.ARIAL, 22), position=(pl.xPos.right, 20))
button2 = pl.Button(window, 300, 50, 400, 50, pl.Color.BEIGE, 32)
fps_counter = pl.FPScounterWidget(window, pl.corner.top_right)


while True:
    window.event_handler()
    # window.clear(pl.Color.RED)
    # print(True)
    # print()
    fps_counter.draw()
    window.draw.rectangle(100, 100, 50, 200, pl.Color.BLUE, (0, 25, 25, 0))
    window.draw.circle(300, 300, 50, pl.Color.RED)
    window.draw.circle_with_border(500, 500, 50, 20, pl.Color.BITTERSWEET, pl.Color.OLIVE_GREEN)
    window.draw.polygon([(0, 0), (200, 0), (100, 100), (0, 100)], pl.Color.GREEN)
    if button.is_double_clicked():
        print(True)
        
    window.draw.polygon_with_border([(500, 300), (200, 300), (100, 100), (500, 100)], 20, pl.Color.GREEN, pl.Color.LESS_WHITE)
        
        
    
    window.draw.line(200, 30, 300, 50, pl.Color.AQUAMARINE)
    window.draw.triangle_with_border((900, 500), (800, 540 ), (750, 600), 4,  pl.Color.YELLOW, pl.Color.BLUE)
    button.draw()
    # button2.draw()
    # print(window.sc.vw(100), window.sc.vh(100))
        