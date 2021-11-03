inp = [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1]
out = [[1,5], [11, 20], [22, 22], [24, 24], [30, 31]]

start = 0
end = 0
pos = False
segments = []
for (i, e) in enumerate(inp):
    if e==1:
        if pos==False:
            pos = True
            start = i
    if e==0:
        if pos==True:
            pos = False
            end = i - 1
            segments.append([start, end])
if pos==True:
    end = len(inp)
    segments.append([start, end])
print(segments)
