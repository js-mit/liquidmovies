import json
from liquid.database import db_session, init_db
from liquid.models import LiquidMethod, Liquid, Video

# set up database
init_db()

v = Video(
    name="flower video",
    url="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
)
db_session.add(v)
v = Video(
    url="https://vjs.zencdn.net/v/oceans.mp4",
    name="ocean",
    poster="//vjs.zencdn.net/v/oceans.png",
)
db_session.add(v)
v = Video(
    url="https://liquidmovies.s3.amazonaws.com/mit_covid_vaccines_lecture.mp4",
    name="mit covid lecture",
    poster="//vjs.zencdn.net/v/oceans.png",
)
db_session.add(v)
v = Video(
    url="https://liquidmovies.s3.amazonaws.com/friendss3.mp4",
    name="friends tv show",
    poster="//vjs.zencdn.net/v/oceans.png",
)
db_session.add(v)

m = LiquidMethod(name="bookmark")
db_session.add(m)
m = LiquidMethod(name="diarization")
db_session.add(m)
m = LiquidMethod(name="other")
db_session.add(m)

l = Liquid(
    video_id=2,
    liquid="[{start: 3, stop: 5}, {start: 20, stop: 23}, {start: 35, stop: 38}]",
    method_id=1,
    desc="fake bookmarks",
)
db_session.add(l)
l = Liquid(
    video_id=2,
    liquid="[{start: 5, stop: 10}]",
    method_id=1,
    desc="another fake bookmark",
)
db_session.add(l)
with open("diarization/79m.json") as json_file:
    data = json.load(json_file)
    l = Liquid(video_id=3, liquid=data, method_id=2, desc="diarization")
    db_session.add(l)
with open("diarization/friendss3.json") as json_file:
    data = json.load(json_file)
    l = Liquid(video_id=4, liquid=data, method_id=2, desc="diarization")
    db_session.add(l)

db_session.commit()
