import expyriment as xpy

exp = xpy.design.Experiment(name="First Experiment")
xpy.control.initialize(exp)

r1 = xpy.stimuli.Rectangle((640, 360), line_width=1, position=(360, 0))
r1.preload()

r2 = xpy.stimuli.Rectangle((640, 360), line_width=1, position=(-360, 0))
r2.preload()

xpy.control.start()

r1.present(clear=False, update=False)
r2.present(clear=False, update=True)
exp.clock.wait(1000)


xpy.control.end()