import json

def add_speaker_segment(speakers, speaker, start, stop):
    start = round(start)
    stop = round(stop)

    if speaker not in speakers:
        speakers[speaker] = [{"start": start, "stop": stop}]
    else:
        speakers[speaker].append({"start": start, "stop": stop})

    return speakers

def create_speaker_segments(lines):
    speakers = {}

    prev_start = 0
    prev_end = 0
    curr_speaker_start = 0
    curr_speaker_end = 0
    curr_speaker = None

    for line in lines:
        l = line.split(" ")
        start = float(l[3])  # Turn Onset
        end = start + float(l[4])  # Turn Onset + Turn Duration
        speaker = l[7]  # speaker name

        if curr_speaker == None:
            curr_speaker = speaker
            curr_speaker_start = start

        if speaker is not curr_speaker:  # speaker changed
            curr_speaker_end = prev_end
            speakers = add_speaker_segment(speakers, curr_speaker, curr_speaker_start, curr_speaker_end)
            curr_speaker_start = start

        prev_start = start
        prev_end = end
        curr_speaker = speaker

    curr_speaker_end = prev_end
    speakers = add_speaker_segment(speakers, curr_speaker, curr_speaker_start, curr_speaker_end)

    return speakers

if __name__=="__main__":
    f = open("../../../scratch/liquid_data/tucker_vs_stewart.rttm", "r")
    lines = f.readlines()

    speakers = create_speaker_segments(lines)

    with open("../../../scratch/liquid_data/tucker_vs_stewart.json", "w") as outfile:
        json.dump(speakers, outfile)
