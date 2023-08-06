#!/usr/bin/python3
#    QASDAD, the quick and simple data analysis and documentation program
#    Copyright (C) 2018 Volker Weißmann . Contact: volker.weissmann@gmx.de

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import shutil
import sys
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("source", help="Path of the source dirctory.")
parser.add_argument("--uselocal", help="Path of a directory with a qasdad installation. If you leave this option out, the qasdad version installation installed with pip is used.")
parser.add_argument("--notexplot", help="Disables the use of tex in rendering of plots. Use this if your tex installation is faulty.", action="store_true")
parser.add_argument("--nosavefig", help="Disables the matplotlib.savefig command. Faster, but you won't get any plots.", action="store_true")
args = parser.parse_args()
#print(args.source)
#print(args.uselocal)
#print(args.notexplot)
#print(args.nosavefig)

SOURCE_PATH = args.source
if not os.path.isfile(SOURCE_PATH) and not os.path.isdir(SOURCE_PATH):
	print("source does not exist: ", SOURCE_PATH)
	exit(2)
sps = list(os.path.split(SOURCE_PATH))
if sps[-1] == "": #This if is neccessary because the user can run qasdad.py dirA/ dirB or qasdad.py dirA dirB
	sps = sps[:-1]
sps[-1] += "_qasdad_output"
OUT_PATH=os.path.join(*sps)
try:
	shutil.rmtree(OUT_PATH)
except:
	pass
os.makedirs(OUT_PATH)
DATA_PATH = os.path.join(OUT_PATH, "qasdad_out")
os.makedirs(DATA_PATH)
extracted = {}
def readFile(sourcepath, latexout):
	source = open(sourcepath, "r")
	latexFile = open(latexout, "w")
	lineNum = 0
	num = None
	for line in source:
		lineNum += 1
		if num is None and line.startswith("\\iffalse BEGIN QASDAD"):
			try:
				num = int(line[21:])
			except:
				print("aborting: unable to parse this line:", line)
				exit(3)
			if num in extracted:
				print("aborting: multiple sections with the number", num)
				exit(3)
			path = os.path.join(DATA_PATH,str(num) + ".tex")
			#extracted[num] = "_TEX_FILE_ = open(\"" + path + "\",'w')\n_LATEX_PATH_=\"" + latexout + "\"\n" #TODO muss man hier die " in path und in latexout scapen?
			extracted[num] = "setTexFile(open(\""+ path  +"\",'w'))\nsetLatexPath(\""+latexout+"\")\n"
			path = os.path.relpath(path,start=os.path.dirname(latexout))
			latexFile.write("\\input{" + path + "}\n")
			continue
		elif num is not None and line.startswith("\\iffalse BEGIN QASDAD"):
			print("aborting: unexpected line ", line)
			exit(3)
		elif num is not None and line.startswith("END QASDAD \\fi"):
			num = None
			continue
		elif num is None and line.startswith("END QASDAD \\fi"):
			print("aborting: unexpected line ", line)
			exit(3)
		if num is None:
			latexFile.write(line)
		else:
			extracted[num] += line
if os.path.isfile(SOURCE_PATH):
	readFile(SOURCE_PATH, os.path.join(OUT_PATH,os.path.basename(SOURCE_PATH)))
elif os.path.isdir(SOURCE_PATH):
	for subdir, dirs, files in os.walk(SOURCE_PATH):
		for file in files:
			if(file.endswith(".tex")):
				sourcepath = os.path.join(subdir, file)
				rel = os.path.relpath(sourcepath,start=SOURCE_PATH)
				latexout = os.path.join(OUT_PATH,rel)
				readFile(sourcepath,latexout)
else:
	print("the source argument:", SOURCE_PATH, "is neither a file nor a directory") #This case should never trigger cause we check this above
	exit(2)

#def filesInOneFile(outfile, infiles):
#	shutil.copy2(infiles[0], outfile)
#	for i in range(1, len(infiles)):
#		outf = open(outfile, "a")
#		inf = open(infiles[i], "r")
#		for line in inf:
#			outf.write(line)
#		outf.close()
#shutil.copy(os.path.join(os.path.dirname(__file__), "src","qasdad.py"), os.path.join(DATA_PATH, "qasdad.py"))
#shutil.copy(os.path.join(os.path.dirname(__file__), "src","constants.py"), os.path.join(DATA_PATH, "constants.py"))
#shutil.copy(os.path.join(os.path.dirname(__file__), "src","units.py"), os.path.join(DATA_PATH, "units.py"))
#shutil.copy(os.path.join(os.path.dirname(__file__), "src","equation.py"), os.path.join(DATA_PATH, "equation.py"))
#shutil.copy(os.path.join(os.path.dirname(__file__), "src","table.py"), os.path.join(DATA_PATH, "table.py"))
#shutil.copy(os.path.join(os.path.dirname(__file__), "src","plot.py"), os.path.join(DATA_PATH, "plot.py"))
#shutil.copy(os.path.join(os.path.dirname(__file__), "src","main.py"), os.path.join(DATA_PATH, "main.py"))
#shutil.copy(os.path.join(os.path.dirname(__file__), "src","calcColumn.py"), os.path.join(DATA_PATH, "calcColumn.py"))

if args.uselocal is not None:
	try:
		shutil.copytree(os.path.join(args.uselocal), os.path.join(DATA_PATH, "qasdad"))
	except:
		print("unable to copy", os.path.join(args.uselocal))
		exit(2)
	#files = ["qasdad.py", "constants.py", "units.py", "equation.py", "table.py", "plot.py", "main.py", "calcColumn.py"]
	#for f in files:
	#	try:
	#		shutil.copy(os.path.join(args.uselocal,f), os.path.join(DATA_PATH, f))
	#	except:
	#		print("unable to copy", os.path.join(args.uselocal,f))
	#		exit(2)

pythonPath = os.path.join(DATA_PATH, "python.py")
pythonFile = open(pythonPath, "w")
pythonFile.write("from qasdad import *\n")
pythonFile.write("setDataPath(\"" + DATA_PATH.replace("\\","\\\\").replace("\"","\\\"")  + "\")\nsetNoTexPlot("+ str(args.notexplot) +")\nsetNoSaveFig("+ str(args.nosavefig) +")\n")
for key in sorted(extracted.keys()):
	pythonFile.write(extracted[key])
pythonFile.close()
print("running the python script...")
ret = os.system("python \"" + pythonPath.replace("\"", "\\\"")  + "\"")
if ret != 0:
	print("error in python.py. Exit code:")
	print(ret)
	exit(4)
