import requests
import emojis
import sys

def main():
	try:
		tokenFile = open("/gitlabtoken.txt" , "r")
		usernameFile = open("/gitlabusername.txt" , "r")
		token = tokenFile.read()
		username = usernameFile.read()
	except IOError:
		print ("Authenticate first using \"glstatus auth\"\n")

	if(len(sys.argv) == 1):
		help()
	elif(sys.argv[1] == "get"):
		get(username)
	elif(sys.argv[1] == 'auth'):
		auth()
	elif(sys.argv[1] == 'set'):
		set(username, token)

def get(username):
	endpoint = 'https://gitlab.com/api/v4/users/' + username + '/status'
	response = requests.get(endpoint, verify = True)
	data = response.json()

	if data['message']:
		print("Current status: " + emojis.encode(":" + data['emoji'] + ":") + " " + data['message'])
	else:
		print('No Status')

def set(username, token):
	endpoint = 'https://gitlab.com/api/v4/user/status'
	
	if(len(sys.argv) < 3):
		print("Usage: \nglstatus set Shipping\nglstatus set unicorn Shipping")
		sys.exit()
	elif(len(sys.argv) == 4):
		PARAMS = { 'emoji' : sys.argv[2], 'message': sys.argv[3] }
	else:
		PARAMS = { 'message': sys.argv[2] }
	response = requests.put(endpoint, verify = True, params = PARAMS, headers = { "PRIVATE-TOKEN" : token })
	data = response.json()

	if(data['message']):
		print("Status set Successful! " + emojis.encode(":" + data['emoji'] + ":") + " " + data['message'])
	else:
		print("Something went wrong!")

def auth():
	username = input("Enter your GitLab Username: ")
	token = input("Enter your GitLab Personal Token: ")
	
	tokenFile = open("/gitlabtoken.txt" , "w")
	usernameFile = open("/gitlabusername.txt" , "w")
	
	tokenFile.write(token)
	usernameFile.write(username)
	
	tokenFile.close()
	usernameFile.close()
	
	print("\nAuth Successful")

def help():
	print("GitLab Status")
	print("\nUsage:")
	print("glstatus get")
	print("glstatus set")
	print("glstatus auth")
