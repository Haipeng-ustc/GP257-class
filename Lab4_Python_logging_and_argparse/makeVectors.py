import numpy as np


def createVector(filename,vecsz):
	vec=np.random.rand(vecsz)
	vec.savez(filename)


if __name__ == "__main__":
	for i in range(8):
		createVector("labVec"+str(i),200*1000*1000)