import csv
import random
import operator
import sys

def load_dataset(filename, nvar):
    dataset = []
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
	for line in lines:
	   if len(line) == nvar:
	       dpoint = [float(line[i]) for i in range(nvar)]
	       dataset.append(dpoint)
   	else:
   	    return dataset
   	    
def euclid_dist(point1, point2, l):
    squared_diffs = map(lambda x,y : (x-y)**2, point1[:l], point2[:l])
    return reduce(lambda x,y : x+y, squared_diffs)

def get_neighbors(train_set, test_inst, k):
    distances = [(train_inst, euclid_dist(test_inst, train_inst, len(test_inst))) 
                    for train_inst in train_set]
    distances.sort(key = operator.itemgetter(1))
    neighbors = [distances[i][0] for i in range(k)]
    return neighbors

def get_response(neighbors):
    allvotes = {}
    for x in neighbors:
	response = x[-1]
	allvotes[response] = allvotes[response] + 1 if response in allvotes else 1 
    sorted_votes = sorted(allvotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return int(sorted_votes[0][0])

def main():
    #Initialising training and test data
    train_file, test_file = sys.argv[1], sys.argv[2]
    train = load_dataset(train_file, 41)
    test = load_dataset(test_file, 40)

    for i, test_inst in enumerate(test):
        response = get_response(get_neighbors(train, test_inst, 3))
        print "{0},{1}".format(i, response)

if __name__ == "__main__":
    main()
