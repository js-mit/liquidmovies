from liquid.database import db_session, init_db
from liquid.models import LiquidMethod, Liquid, Video

# set up database
init_db()

v = Video(
    url="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
)
db_session.add(v)
v = Video(url="https://vjs.zencdn.net/v/oceans.mp4")
db_session.add(v)
v = Video(url="http://localhost:9004/mit_test.mp4")
db_session.add(v)

m = LiquidMethod(name="bookmark")
db_session.add(m)
m = LiquidMethod(name="other")
db_session.add(m)

l = Liquid(
    video=2,
    liquid="[{start: 3, stop: 5}, {start: 20, stop: 23}, {start: 35, stop: 38}]",
    method=1,
    desc="fake bookmarks",
)
db_session.add(l)
l = Liquid(
    video=2, liquid="[{start: 5, stop: 10}]", method=1, desc="another fake bookmark"
)
db_session.add(l)

db_session.commit()
