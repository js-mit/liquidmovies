# Testing purposes only
from liquid.db import db_session, init_db
from liquid.models import Controller, Liquid, Video, Treatment, User

"""
Initalize DB
This creates the schemas for all the tables
"""
init_db()


"""
Create Videos
"""
v1 = Video(
    url="https://liquidmovies.s3.amazonaws.com/mit_covid_vaccines_lecture.mp4",
    name="mit covid lecture",
    poster_url="//vjs.zencdn.net/v/oceans.png",
    desc="A lecture by xyz about covid at the MIT Media Lab.",
)
v2 = Video(
    url="https://liquidmovies.s3.amazonaws.com/polisci-lecture.mp4",
    name="Introduction to Power and Politics in Today’s World",
    poster_url="https://liquidmovies.s3.amazonaws.com/polisci-lecture_poster_url.png",
    desc="A lecture by xyz about political science at Yale.",
)
v3 = Video(
    url="https://liquidmovies.s3.amazonaws.com/Our+Planet%2C+From+Deserts+to+Grasslands+(Netflix).mp4",
    name="Our Planet - From Deserts to Grasslands (Netflix)",
    poster_url="https://liquidmovies.s3.amazonaws.com/our_planet+poster_url.png",
    desc="Learn about all the animals on our planet. So amaze!",
)
db_session.add_all([v1, v2, v3])


"""
Create Controllers
TODO - should this be here or in the application layer?
"""
c1 = Controller(name="segments")
c2 = Controller(name="diarization")
c3 = Controller(name="markers")
db_session.add_all([c1, c2, c3])


"""
Create Treatments
"""
t1 = Treatment(
    name="text-search",
    desc="ctrl-f with text using speech-to-text",
    controller_id=3,
)
t2 = Treatment(
    name="image-search",
    desc="ctrl-f with images using default rekcognition-provided labels",
    controller_id=3,
)
db_session.add_all([t1, t2])


"""
Create Liquids
"""
instructions = [0] * 46
instructions[1:8] = [1] * 7
instructions[15:22] = [1] * 6
instructions[36:46] = [1] * 9
l1 = Liquid(
    video_id=1,
    instructions=instructions,
    treatment_id=1,
)

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
l2 = Liquid(video_id=2, instructions=instructions, treatment_id=1)

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
l3 = Liquid(video_id=3, instructions=instructions, treatment_id=2)
db_session.add_all([l1, l2, l3])


"""
Create a user
"""
u = User(email="tester1@gmail.com")
u.set_password("viralviral")
u.liquids.append(l1)
u.liquids.append(l2)
u.liquids.append(l3)
db_session.add(u)


db_session.commit()
