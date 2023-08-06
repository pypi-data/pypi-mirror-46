from flask import Flask

app = Flask(__name__)

@app.route("/")

'''
def index('/'):
	return <h1>Hello boy</h1>
'''

#Python program to display fibonnaci series

def recur_fibo(n):
	"""Recursive function to print fibonacci sequence"""

	if n <= 1:
		return n
	else:
		return(recur_fibo(n-1) + recur_fibo(n-2))

#Changing the value for a different results

nterms = 10

nterms = int(input("How many terms?"))

#CHecking if the number of terms is valid
if nterms <= 0:
	print("Please enter a positive integer")
else:
	print("Fiboncci Sequence:")

	for i in range(nterms):
		print(recur_fibo(i))
'''
#print ("{name} wrote {book}".format(name='Swaroop',book='A Byte of Python'))'''