SleepTime = 85

idx_1 = SleepTime%256
SleepTimeBytes = [(SleepTime-idx_1)/256, idx_1]

print(SleepTimeBytes)