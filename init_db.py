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
# v1 = Video(
#     url="https://liquidmovies.s3.amazonaws.com/dev/videos/lecture/video.mp4",
#     name="Introduction to Power and Politics in Today’s World",
#     poster_url="https://liquidmovies.s3.amazonaws.com/dev/videos/lecture/poster.png",
#     desc="A lecture by xyz about political science at Yale.",
# )
# v2 = Video(
#     url="https://liquidmovies.s3.amazonaws.com/dev/videos/our-planet/video.mp4",
#     name="Our Planet - From Deserts to Grasslands (Netflix)",
#     poster_url="https://liquidmovies.s3.amazonaws.com/dev/videos/our-planet/poster.png",
#     desc="Learn about the animals on our planet. So amaze!",
# )
# db_session.add_all([v1, v2])


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
# l1 = Liquid(
#     video_id=1,
#     url="https://liquidmovies.s3.amazonaws.com/dev/videos/lecture/liquids/1/data.json",
#     treatment_id=1,
# )
# l2 = Liquid(
#     video_id=2,
#     url="https://liquidmovies.s3.amazonaws.com/dev/videos/our-planet/liquids/2/data.json",
#     treatment_id=2,
# )
# db_session.add_all([l1, l2])


"""
Create a user
"""
u = User(email="tester1@gmail.com")
u.set_password("viralviral")
# u.liquids.append(l1)
# u.liquids.append(l2)
db_session.add(u)


db_session.commit()
