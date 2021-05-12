# set up docker
```
sudo docker run --name diarization -d -v /"$(pwd)":/home -v ~/scratch:/scratch --shm-size=2gb --interactive --tty --rm pytorch/pytorch bash
sudo docker exec -it diarization bash
```

add this line to docker file to fix gcc problem # check if this is still valid
```
apt-get -y update && apt-get install -y libzbar-dev
apt-get install libsndfile1 
```

install pip
```
pip install -r requirements.txt
```

# Convert mp4 to wav to rttm to json
run the following in the docker container
```
ffmpeg -i <input.mp4> -ac 2 -f wav <output.wav>
python run.py <input.wav> <output.rttm> # this step can take a long time
python submit.py <input.rttm> <output.json>
```

# RTTM
Rich Transcription Time Marked (RTTM) files are space-delimited text files
containing one turn per line, each line containing ten fields:

- ``Type``  --  segment type; should always by ``SPEAKER``
- ``File ID``  --  file name; basename of the recording minus extension (e.g.,
  ``rec1_a``)
- ``Channel ID``  --  channel (1-indexed) that turn is on; should always be
  ``1``
- ``Turn Onset``  --  onset of turn in seconds from beginning of recording
- ``Turn Duration``  -- duration of turn in seconds
- ``Orthography Field`` --  should always by ``<NA>``
- ``Speaker Type``  --  should always be ``<NA>``
- ``Speaker Name``  --  name of speaker of turn; should be unique within scope
  of each file
- ``Confidence Score``  --  system confidence (probability) that information
  is correct; should always be ``<NA>``
- ``Signal Lookahead Time``  --  should always be ``<NA>``

For instance:

    SPEAKER CMU_20020319-1400_d01_NONE 1 130.430000 2.350 <NA> <NA> juliet <NA> <NA>
    SPEAKER CMU_20020319-1400_d01_NONE 1 157.610000 3.060 <NA> <NA> tbc <NA> <NA>
    SPEAKER CMU_20020319-1400_d01_NONE 1 130.490000 0.450 <NA> <NA> chek <NA> <NA>
