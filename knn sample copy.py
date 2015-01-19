import csv
import random
import operator

def load_dataset(filename, split, nvar):
    training_set=[]
    test_set=[]
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
	for line in lines:
	   if len(line) == nvar:
	       for i in range(nvar - 1):
	           line[i] = float(line[i])
	       training_set.append(line) if random.random() < split else test_set.append(line)
   	else:
   	    return (training_set, test_set)
	            

def euclid_dist(point1, point2, l):
    squared_diffs = map(lambda x,y : (x-y)**2, point1[:l], point2[:l])
    return reduce(lambda x,y : x+y, squared_diffs)
    

"""tSet = [[2, 2, 2, 'a'], [6, 6, 6, 'c'], [4, 4, 4, 'b']]
tSet.sort(key=operator.itemgetter(0))"""

def get_neighbors(train_set, test_inst, k):
    distances = [(x, euclid_dist(test_inst, x, len(test_inst)-1)) for x in train_set]
    distances.sort(key = operator.itemgetter(1))
    neighbors = [distances[x][0] for x in range(k)]
    return neighbors

"""train_set = [[2, 2, 2, 'a'], [4, 4, 4, 'b']]
test_instance = [5, 5, 5]
k = 1
neighbors = get_neighbors(train_set, test_instance, 1)
print(neighbors)"""

def get_response(neighbors):
    allvotes = {}
    for x in neighbors:
	response = x[-1]
	allvotes[response] = allvotes[response] + 1 if response in allvotes else 1 
    sorted_votes = sorted(allvotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_votes[0][0]

"""neighbors = [[1,1,1,'a'], [2,2,2,'a'], [3,3,3,'b']]
response = get_response(neighbors)
print(response)"""

def get_accuracy(test_set, predictions):
    correct = 0
    for i, ts in enumerate(test_set):
	if ts[-1] == predictions[i]:
	   correct += 1
    return (correct/float(len(test_set))) * 100.0

train, test = load_dataset("/Users/Chandru/Documents/projects/Kaggle scikit learn/train_data.csv", .66, 41)

for k in range(1,16):
    predictions = [get_response(get_neighbors(train, inst, k)) for inst in test]
    print k, get_accuracy(test, predictions)
