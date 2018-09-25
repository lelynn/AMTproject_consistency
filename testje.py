import expyriment as xpy
import subprocess
import pandas as pd

exp = xpy.design.Experiment(name="First Experiment")

xpy.control.initialize(exp)

xpy.control.stop_audiosystem()

xpy.control.start()

cmd = ['xrandr']
cmd2 = ['grep', '*']
p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
p.stdout.close()

resolution_string, junk = p2.communicate()
resolution = resolution_string.split()[0]
screen_width, screen_height = resolution.split('x')

screen_width = int(screen_width)
screen_height = int(screen_height)
# screen_width = 1440
# screen_height = 900
print 'height' , screen_height
print 'width', screen_width


left_key = 119
dontknow_key = 101
right_key = 114

allkeys = [left_key, dontknow_key, right_key]

personalities = ["Friendly", "Authentic", "Organized", "Comfortable", "Imaginative", "Intervieuw"]
heightscale = 3.5
position_left = (0 - (screen_width / 3), 0 - (screen_height / heightscale))
position_dontknow = (0, 0 - (screen_height / heightscale))
position_right = (0 + (screen_width / 3), 0 - (screen_height / heightscale))

position_task = (0, 0 + (screen_height / heightscale))

# exp = xpy.design.Experiment(name="First Experiment")
# xpy.control.initialize(exp)
# xpy.control.start(skip_ready_screen=True)


def key2result(key_code):
    if key_code == left_key:
        return "LEFT"

    elif key_code == dontknow_key:
        return "DON'T KNOW"

    elif key_code == right_key:
        return "RIGHT"


DF100 = pd.read_csv('DF100.csv')

# result_df = pd.DataFrame()
result_file = "my_results/results_{}.csv".format(exp.subject)
pd.DataFrame(columns=["videoLeft","videoRight","videoPair"] + personalities).to_csv(result_file)

for pair in range(len(DF100)):



    pair = DF100.iloc[pair]

    video_pair = pair['videoPair']

    my_video = xpy.stimuli.Video(video_pair )

    personality_index = 0
    personality_text = xpy.stimuli.TextLine("", position_task)

    left_text = xpy.stimuli.TextLine('Left', position_left)

    dontknow_text = xpy.stimuli.TextLine('Don\'t know', position_dontknow)

    right_text = xpy.stimuli.TextLine('Right', position_right)


    # my_video.preload()
    # personality_text.preload()
    # left_text.preload()
    # dontknow_text.preload()
    # right_text.preload()

    # exp.clock.wait(3000)

    my_video.play()
    # xpy.io.Screen.clear()
    # exp.screen.clear()
    # my_video.present()
    # my_video.wait_frame(75)

    sample_result = pd.Series(pair[["videoLeft","videoRight","videoPair"]],name=pair.name)
    start_time = exp.clock.time
    answer_bool = False
    while personality_index < len(personalities):
        while not my_video.new_frame_available or my_video.time == 0.0:
            key = exp.keyboard.check()
            if key in allkeys and answer_bool:
                sample_result[personalities[personality_index]] = key2result(key)

                personality_index += 1
                if personality_index == len(personalities):
                    personality_text = xpy.stimuli.TextLine("",
                                                            position_task,
                                                            background_colour=(204,255,153),
                                                            text_size = 50,
                                                            text_colour= (0,0,0),
                                                            text_font='freemono')

                    # my_video.wait_frame(my_video.frame+1)
                    break
                else:
                    personality_text = xpy.stimuli.TextLine(personalities[personality_index],
                                                            position_task - (0, 5),
                                                            background_colour=(204, 255, 153),
                                                            text_size = 50,
                                                            text_colour= (0,0,0),
                                                            text_font='courier')
                    break

        personality_text.present(update=False, clear=True)
        if answer_bool:
            pass
        elif exp.clock.time-start_time > 3000:
            personality_text = xpy.stimuli.TextLine(personalities[personality_index],
                                                    position_task,
                                                    background_colour=(204, 255, 153),
                                                    text_size=50,
                                                    text_colour=(0, 0, 0),
                                                    text_font = 'courier'
                                                    )
            answer_bool = True

        if my_video.time > 0.0:             # if video is not done yet
            left_text.present(update=False, clear=False)
            if key_code == left_key:

                if personality_index >= 1:
                    for index in len(range(personality_index)):

                        personality_text = xpy.stimuli.TextLine(personality_text[personality_index],
                                                                position_left - (index*(0, 5)),
                                                                background_colour=(204,255,153),
                                                                text_size = 50,
                                                                text_colour= (0,0,0),
                                                                text_font='freemono')

                else:
                        personality_text = xpy.stimuli.TextLine(personality_text[personality_index],
                                                                position_left - (index*(0, 5)),
                                                                background_colour=(204,255,153),
                                                                text_size = 50,
                                                                text_colour= (0,0,0),
                                                                text_font='freemono')


                        personality_text.present()


            dontknow_text.present(update=False, clear=False)

            right_text.present(clear=False, update=False)

            my_video.present()

        else:
            left_text.present(update=False, clear=False)
            dontknow_text.present(update=False, clear=False)
            right_text.present(clear=False)
        # my_video.update()


        # personality_text.present(update=False, clear=False)
        # left_text.present(update=False, clear=False)
        # dontknow_text.present(update=False, clear=False)
        # right_text.present(clear=False, update=False)


        #my_video.present()



    # print "my_video1.frame:",my_video.frame

    my_video.stop()
    my_video.unload()
    # result_df = result_df.append(sample_result)
    sample_result.to_frame().transpose().to_csv(result_file, mode="a",header=False)
    # xpy.stimuli.BlankScreen().present()
    # exp.screen.clear()
    # my_video.present()

    #right_text.plot(my_video)

xpy.control.end()
# result_df.to_csv("my_results/results_df.csv")
