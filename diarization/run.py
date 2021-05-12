# load pipeline
import torch

if __name__=="__main__":
    audio_file_path = "../../../scratch/liquid_data/tucker_vs_stewart.wav"

    pipeline = torch.hub.load("pyannote/pyannote-audio", "dia")

    # apply diarization pipeline on your audio file
    diarization = pipeline({"audio": audio_file_path})

    # dump result to disk using RTTM format
    with open("../../../scratch/liquid_data/tucker_vs_stewart.rttm", "w") as f:
        diarization.write_rttm(f)
