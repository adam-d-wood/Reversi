c = 3*10**8

t = input("t: ")
v = input("v: ")

def time_dilate(t, v):
	gamma = 1/(1-((v**2)/c**2))
	return t * gamma

print(time_dilate(t, v))

