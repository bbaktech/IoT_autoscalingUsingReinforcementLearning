import random
import numpy as np
import pandas as pd

# Create a DataFrame
df = pd.DataFrame(columns=['resources', 'jobs', 'action'])

for i in range(150):
	jobs =  random.randint(50,100)
	clsters =  random.randint(3,9)
	capacity  = clsters * 10	
	action = 2 #NO CHANGE
	if jobs > capacity + 2:
		action = 0 # UP
	elif jobs < capacity - 8 :
		action = 1 # DOWN
	else:
		action = 3 #BALANCE
	df.loc[i] = [clsters,jobs,action]

# Write the DataFrame to a CSV file
df.to_csv('RL_dataSet.csv', index=False)



