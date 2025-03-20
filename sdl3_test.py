import src as pl

window = pl.Window(600, 800)

window2 = pl.Window(100, 100)

while True:
    pl.event_handler()
    window.update()