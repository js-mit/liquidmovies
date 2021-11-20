# Testing purposes only
import json
from pathlib import Path
from liquid.db import db_session, init_db
from liquid.models import Controller, Liquid, Video, User

init_db()

# id = 1
v = Video(
    url="https://liquidmovies.s3.amazonaws.com/mit_covid_vaccines_lecture.mp4",
    name="mit covid lecture",
    poster="//vjs.zencdn.net/v/oceans.png",
)
db_session.add(v)
# id = 2
v = Video(
    url="https://liquidmovies.s3.amazonaws.com/polisci-lecture.mp4",
    name="Introduction to Power and Politics in Today’s World",
    poster="https://liquidmovies.s3.amazonaws.com/polisci-lecture_poster.png",
)
db_session.add(v)
# id = 3
v = Video(
    url="https://liquidmovies.s3.amazonaws.com/Our+Planet%2C+From+Deserts+to+Grasslands+(Netflix).mp4",
    name="Our Planet - From Deserts to Grasslands (Netflix)",
    poster="https://liquidmovies.s3.amazonaws.com/our_planet+poster.png",
)
db_session.add(v)


# Controllers
c = Controller(name="segments")
db_session.add(c)
c = Controller(name="diarization")
db_session.add(c)
c = Controller(name="markers")
db_session.add(c)

instructions = [0] * 46
instructions[1:8] = [1] * 7
instructions[15:22] = [1] * 6
instructions[36:46] = [1] * 9
l = Liquid(
    video_id=1,
    liquid=instructions,
    controller_id=1,
    desc="fake bookmarks",
)
db_session.add(l)

# liquids
instructions = [[""]] * 3374
instructions[10] = ["cold war", "america"]
instructions[20] = ["cold war", "ussr"]
instructions[1200] = ["government"]
instructions[1208] = ["government"]
instructions[1228] = ["government"]
instructions[1272] = ["government"]
instructions[1288] = ["government"]
instructions[1294] = ["government"]
instructions[2200] = ["cold war", "floor"]
instructions[2500] = ["cold war", "floor", "america"]
instructions[2503] = ["america"]
instructions[2509] = ["america"]
instructions[2510] = ["america", "politics"]
instructions[2519] = ["america"]
instructions[2555] = ["politics"]
instructions[2810] = ["government"]
instructions[2820] = ["government"]
instructions[2848] = ["government"]
instructions[2877] = ["government"]
instructions[2888] = ["government"]
instructions[2910] = ["government", "america"]
instructions[2978] = ["america", "politics"]
instructions[3118] = ["cold war", "floor", "america"]
instructions[3200] = ["cold war", "floor", "america", "ussr"]
l = Liquid(video_id=2, liquid=instructions, controller_id=3, desc="Polisci lecture")
db_session.add(l)

instructions = [[""]] * 3054
instructions[958] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/elephant_01.png"
]
instructions[961] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/elephant_02.png"
]
instructions[963] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/elephant_03.png"
]
instructions[974] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/elephant_04.png"
]
instructions[987] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/elephant_05.png"
]
instructions[989] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/elephant_06.png"
]
instructions[994] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/elephant_07.png"
]
instructions[1002] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/elephant_08.png"
]
instructions[1013] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/elephant_09.png"
]
instructions[1054] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/elephant_10.png"
]
instructions[1075] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/elephant_11.png"
]
instructions[1092] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/elephant_12.png"
]
instructions[1169] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/elephant_13.png"
]
instructions[1190] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/elephant_14.png"
]
instructions[1213] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/elephant_15.png"
]
instructions[1236] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/elephant_16.png"
]
instructions[2624] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/elephant_17.png"
]
instructions[1983] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/butterfly_01.png"
]
instructions[1989] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/butterfly_02.png"
]
instructions[1993] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/butterfly_03.png"
]
instructions[1999] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/butterfly_04.png"
]
instructions[2001] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/butterfly_05.png"
]
instructions[2008] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/butterfly_06.png"
]
instructions[2012] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/butterfly_07.png"
]
instructions[2019] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/butterfly_08.png"
]
instructions[2023] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/butterfly_09.png"
]
instructions[2031] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/butterfly_10.png"
]
instructions[2033] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/butterfly_11.png"
]
instructions[2034] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/butterfly_12.png"
]
instructions[2039] = [
    "https://liquidmovies.s3.amazonaws.com/ctrlf_imgs+(our_planet)/butterfly_13.png"
]
l = Liquid(
    video_id=3, liquid=instructions, controller_id=3, desc="Our Planet ctrlf im search"
)
db_session.add(l)

db_session.commit()
