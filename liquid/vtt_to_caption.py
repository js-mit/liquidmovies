import webvtt

for caption in webvtt.read('captions.vtt'):
    print(caption.start)
    print(caption.end)
    print(caption.text)