import numpy as np


def createVector(filename,vecsz):
	vec=np.random.rand(vecsz)
	np.savez(filename, vec)


if __name__ == "__main__":
	for i in range(8):
		# createVector("labVec"+str(i),200*1000*1000)
		createVector("labVec"+str(i),20*100*100)