import src as pl

window = pl.Window(600, 800)
# window2 = pl.Window(100, 100)

while True:
    window.event_handeler()
    # window2.event_handeler()
    window.fill(pl.Color.BITTERSWEET)
    window.update()