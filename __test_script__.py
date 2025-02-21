import src as pl
import time

window = pl.Window(800, 600)

clk = pl.Clock(60)
pl.enable_debugging()
clk.sleep()
time.sleep(2)
clk.sleep()
while True:
    window.event_handler()
    window.clear((255, 0, 0))
    window.update()