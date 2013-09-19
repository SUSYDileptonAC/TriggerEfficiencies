#!/usr/bin/env python

def main():
	from sys import argv
	effEE = float(argv[1])
	effMM = float(argv[2])
	effEMu = float(argv[3])
	err = float(argv[4])
	
	print (effEE*effMM)**0.5/effEMu, (err**2/(2*effEE*effMM)**2+ err**2/(2*effEE*effMM)**2 + err**2/(effEMu)**2)**0.5
	
main()
