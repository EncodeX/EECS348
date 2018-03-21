import student_code as sc


def init_map(map_array):
	testmap = []
	for ms in map_array:
		ms_arr = []
		for c in ms:
			ms_arr.append(int(c))
		testmap.append(ms_arr)
	return testmap

def print_map (testmap):
	for lst in testmap:
		print lst
		print '\n'

def check_map_equal (map1, map2):
	flag = True
	for i in range(len(map1)):
		for j in range(len(map1[0])):
			if map1[i][j] != map2[i][j]:
				flag = False
	return flag

def check_score_equal(score1, score2):
	flag = True
	keys1 = score1.keys()
	keys2 = score2.keys()
	if set(keys1) == set(keys2):
		for k in keys1:
			if score1[k] != score2[k]:
				flag = False
	else:
		flag = False
	return flag


def main():
	dis_map = {'Campus': {'Campus': 0, 'Whole_Food': 3, 'Beach': 5, 'Cinema': 5, 'Lighthouse': 1, 'Ryan Field': 2, 'YWCA':12},
				'Whole_Food': {'Campus': 3,  'Whole_Food': 0, 'Beach': 3, 'Cinema': 3, 'Lighthouse': 4, 'Ryan Field': 5, 'YWCA':8},
				'Beach': {'Campus': 5,  'Whole_Food': 3, 'Beach': 0, 'Cinema': 8, 'Lighthouse': 5, 'Ryan Field': 7, 'YWCA':12,},
				'Cinema': {'Campus': 5,  'Whole_Food': 3, 'Beach': 8, 'Cinema': 0, 'Lighthouse': 7, 'Ryan Field': 7, 'YWCA':2},
				'Lighthouse': {'Campus': 1, 'Whole_Food': 4, 'Beach': 5, 'Cinema': 7, 'Lighthouse': 0, 'Ryan Field': 1, 'YWCA':15},
				'Ryan Field': {'Campus': 2, 'Whole_Food': 5, 'Beach': 7, 'Cinema': 7, 'Lighthouse': 1, 'Ryan Field': 0, 'YWCA':12},
				'YWCA': {'Campus': 12, 'Whole_Food': 8, 'Beach': 12, 'Cinema': 2, 'Lighthouse': 15, 'Ryan Field': 12, 'YWCA':0}}
	time_map1 = {'Campus': {'Campus': None, 'Whole_Food': 4, 'Beach': 3, 'Cinema': None, 'Lighthouse': 1, 'Ryan Field': None, 'YWCA': None},
				'Whole_Food': {'Campus': 4,  'Whole_Food': None, 'Beach': 4, 'Cinema': 3, 'Lighthouse': None, 'Ryan Field': None, 'YWCA': None},
				'Beach': {'Campus': 4,  'Whole_Food': 4, 'Beach': None, 'Cinema': None, 'Lighthouse': None, 'Ryan Field': None, 'YWCA': None},
				'Cinema': {'Campus': None,  'Whole_Food': 4, 'Beach': None, 'Cinema': None, 'Lighthouse': None, 'Ryan Field': None, 'YWCA': 2},
				'Lighthouse': {'Campus': 1, 'Whole_Food': None, 'Beach': None, 'Cinema': None, 'Lighthouse': None, 'Ryan Field': 1, 'YWCA': None},
				'Ryan Field': {'Campus': None, 'Whole_Food': None, 'Beach': None, 'Cinema': None, 'Lighthouse': 2, 'Ryan Field': None, 'YWCA': 5},
				'YWCA': {'Campus': None, 'Whole_Food': None, 'Beach': None, 'Cinema': 3, 'Lighthouse': None, 'Ryan Field': 5, 'YWCA': None}}
	student_score1 = sc.a_star_search(dis_map,time_map1, 'Campus', 'Cinema')
	gold_score1 = {'Whole_Food': {'Beach': 16, 'Campus': 13, 'Cinema': 7}, 'Campus': {'Lighthouse': 8, 'Beach': 11, 'Whole_Food': 7}}
	if check_score_equal(student_score1,gold_score1):
		print "pass A* search for time map1"
	else:
		print "Fail A* search for time map1"
		exit(1)
	exit(0)

if __name__== "__main__":
	main()




