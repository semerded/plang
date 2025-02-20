import src as pl

window = pl.Window(800, 600)


while True:
    window.event_handler()
    window.clear((255, 0, 0))
    window.update()