import Utils

signal=[2,1,0,-1,-2]
response=[1,0.5,0,-0.5,-1]
signal=Utils.normalize(signal)
print(signal==response)
