import pickle

with open('weights.pickle', 'rb') as w_file:
	weights = pickle.load(w_file)
	print weights

# with open('weights.pickle','wb') as w_file:
# 	pickle.dump(weights, w_file)
