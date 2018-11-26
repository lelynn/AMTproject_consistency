import expyriment as xpy
import subprocess
import pandas as pd
import numpy as np

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


font = 'gill sans'
# left_key = 119
# dontknow_key = 101
# right_key = 114

left_key = 115
dontknow_key = 100
right_key = 102

allkeys = [left_key, dontknow_key, right_key]

personalities = ["Friendly", "Authentic", "Organized", "Comfortable", "Imaginative", "Interview"]
pers_questions = ["1. Friendly (vs. reserved)",
                  "2. Authentic (vs. self-interested)",
                  "3. Organized (vs. sloppy)",
                  "4. Comfortable (vs. uneasy)",
                  "5. Imaginative (vs. practical)",
                  "6. Who would you rather invite for a job interview?",
                  ]

heightscale = 4

position_left = (0 - (screen_width / 3), 0 - (screen_height / heightscale))
position_dontknow = (0, 0 - (screen_height / heightscale))
position_right = (0 + (screen_width / 3), 0 - (screen_height / heightscale))

position_task = (0, 0 + (screen_height / 2.5))

personality_text_kwargs = dict(position=position_task,
                                # background_colour=(43, 43, 43),
                                text_size = 50,
                                text_bold=False,
                                text_colour=(255, 255, 255),
                                text_font= font)

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

def key2personality_text(key_code, index, index1, index2, index3):

    if key_code == left_key:

        new_position = map(sum, zip(position_left, (np.dot((index1+1),(0, -30)))))
        index1 += 1

    elif key_code == right_key:
        new_position = map(sum, zip(position_right, (np.dot((index2+1), (0, -30)))))
        index2 += 1
    else:
        new_position = map(sum, zip(position_dontknow, (np.dot((index3+1), (0, -30)))))
        index3 += 1
    return xpy.stimuli.TextLine(" "+str(index+1)+'. ' + personalities[index] + ' ',
                                (new_position),
                                            background_colour=(43, 43, 43),
                                            text_size=19,
                                #text_bold= True,
                                text_colour=(255, 255, 255),
                                            text_font=font), index1, index2, index3



DF100 = pd.read_csv('DF100.csv')

# result_df = pd.DataFrame()
result_file = "my_results/results_{}.csv".format(exp.subject)
# import os
# if os.path.exists(result_file):
#

pd.DataFrame(columns=["videoLeft","videoRight","videoPair"] + personalities).to_csv(result_file)

for pair in range(len(DF100)):

    pair = DF100.iloc[pair]

    video_pair = pair['videoPair']

    my_video = xpy.stimuli.Video(video_pair)

    personality_index = 0

    list_index1 = 0
    list_index2 = 0
    list_index3 = 0

    personality_text = xpy.stimuli.TextLine("", position_task)

    left_text = xpy.stimuli.TextLine('Left [s]',
                                     position_left,

                                     #text_bold= True,
                                     text_font= font
                                     )

    dontknow_text = xpy.stimuli.TextLine('Don\'t know [d]',
                                         position_dontknow,
                                         #text_bold=True,
                                         text_font= font,
                                         )

    right_text = xpy.stimuli.TextLine('Right [f]',
                                      position_right,
                                      #text_bold=True,
                                      text_font= font,
                                      )

    # exp.clock.wait(3000)

    my_video.play()

    sample_result = pd.Series(pair[["videoLeft","videoRight","videoPair"]],name=pair.name)
    start_time = exp.clock.time
    answer_bool = False
    selected_personalities = []

#to start the counter for each list under the movie


    while personality_index < len(personalities):
        while not my_video.new_frame_available and my_video.is_playing:
            key = exp.keyboard.check()
            if key in allkeys and answer_bool:
                sample_result[personalities[personality_index]] = key2result(key)

                Textline, list_index1, list_index2, list_index3 = key2personality_text(key, personality_index, list_index1, list_index2, list_index3)

                selected_personalities.append(Textline)


                personality_index += 1
                if personality_index == len(personalities):
                    personality_text = xpy.stimuli.TextLine("",
                                                            **personality_text_kwargs)
                                                            # position_task,
                                                            # # background_colour=(43,43,43),
                                                            # text_size = 50,
                                                            # text_bold=False,
                                                            # text_colour= (255,255,255),
                                                            # text_font= font)

                    # my_video.wait_frame(my_video.frame+1)
                    break
                else:
                    personality_text = xpy.stimuli.TextLine(' ' + pers_questions[personality_index] + ' ',
                                                            **personality_text_kwargs)
                    break
            elif key == 8 and personality_index > 0:
                personality_index -= 1
                selected_personalities.pop(personality_index)
                prev_answer = sample_result[personalities[personality_index]]
                if prev_answer == "LEFT":
                    list_index1 -= 1
                elif prev_answer == "RIGHT":
                    list_index2 -= 1
                elif prev_answer == "DON'T KNOW":
                    list_index3 -= 1
                personality_text = xpy.stimuli.TextLine(' ' + pers_questions[personality_index] + ' ',
                                                        **personality_text_kwargs)
                                                        # position_task,
                                                        # # background_colour=(43, 43, 43),
                                                        # text_size=50,
                                                        # text_bold=False,
                                                        # text_colour=(255, 255, 255),
                                                        # text_font=font
                                                        #)
            elif key is not None:
                print "key:", key


        personality_text.present(update=False, clear=True)
        if answer_bool:
            pass
        elif my_video.time > 3:
            personality_text = xpy.stimuli.TextLine(' '+ pers_questions[personality_index]+ ' ',
                                                    **personality_text_kwargs)
                                                    # position_task,
                                                    # # background_colour=(43, 43, 43),
                                                    # text_size=50,
                                                    # text_bold= False,
                                                    # text_colour=(255, 255, 255),
                                                    # text_font= font
                                                    #)
            answer_bool = True

        left_text.present(update=False, clear=False)
        dontknow_text.present(update=False, clear=False)

        for selected_personality in selected_personalities:
            selected_personality.present(clear=False, update=False)

        # if my_video.time > 0.0:             # if video is not done yet
        #     right_text.present(clear=False, update=False)
        #     my_video.present()
        # else:
        #     right_text.present(clear=False)
        if not my_video.is_playing:
            print "not playing"

            my_video.stop()
            my_video.unload()
            my_video.play()

        right_text.present(clear=False, update=False)
        my_video.present()


    my_video.stop()
    my_video.unload()
    sample_result.to_frame().transpose().to_csv(result_file, mode="a",header=False)

xpy.control.end()
