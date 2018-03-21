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
	data1= ["2000000000",
			"0101111111",
			"0100000000",
			"0101111111",
			"0101000001",
			"0101010110",
			"0101010000",
			"0100011110",
			"0011111110",
			"1011111110",
			"1011111111",
			"1000000003"]
	gold_df1 = ["5444444444",
				"5141111111",
				"5144444444",
				"5141111111",
				"5141444441",
				"5141414114",
				"5141414444",
				"5144411114",
				"5511111114",
				"1511111114",
				"1511111111",
				"1555555555"]
					 
	gold_bf1 = ["5444444444",
				"5141111111",
				"5144444444",
				"5141111111",
				"5141444441",
				"5141414110",
				"5141414440",
				"5144411110",
				"5511111110",
				"1511111110",
				"1511111111",
				"1555555555"]
	student_bf1 = sc.bfs(init_map(data1))
	if check_map_equal(student_bf1, init_map(gold_bf1)):
		print "Pass bfs for map1"
	else:
		print "Fail bfs for map1"
		exit(1)
	exit(0)

if __name__== "__main__":
	main()