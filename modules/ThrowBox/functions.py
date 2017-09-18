import os
import time

def ReadPath(path):
	LOCAL_PATH=os.path.dirname(os.path.realpath(__file__))
	REPO=os.path.join(LOCAL_PATH, "REPO")


	REQUESTED_PATH=os.path.join(REPO,path)

	if not os.path.exists(REQUESTED_PATH):
		print("Doesnt exist.")
		return None

	try:
		stuff=next(os.walk(REQUESTED_PATH))
		folders=stuff[1]
		files=stuff[2]
		return folders,files
	except StopIteration:
		print("empty.")
		return 0

def IsFile(path):
	LOCAL_PATH=os.path.dirname(os.path.realpath(__file__))
	REPO=os.path.join(LOCAL_PATH, "REPO")
	FINAL_PATH=os.path.join(REPO,path)

	if os.path.isdir(FINAL_PATH):
		return False
	else:
		return True

def RepoPath(path):
	LOCAL_PATH=os.path.dirname(os.path.realpath(__file__))
	REPO=os.path.join(LOCAL_PATH, "REPO")
	FINAL_PATH=os.path.join(REPO,path)

	return FINAL_PATH


def RemoveHiddenObjects(_list):
	_list2=list() # List that contains only visible,
				  # non-hidden objects.
	for element in _list:
		if element[0]!=".":
			_list2.append(element)

	return _list2


def log(message, file="log.txt"):
	"""A barebones function that logs messages."""
	line="[{} >>> {}]\n\t{}\n\n".format(time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"),message)
	file=open(file, "a")
	file.write(line)
	file.close()




