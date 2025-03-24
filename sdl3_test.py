import src as pl

window = pl.Window(600, 800)

window2 = pl.Window(300, 200)

while True:
    pl.event_handler()
    
    if pl.Window.is_active(window):
        # print(type(window._window))
        window.update()