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
	data1= ["0000000000",
			"0010111111",
			"0210100000",
			"1110101110",
			"0000101010",
			"0010101010",
			"0010001010",
			"0011111010",
			"0000000010",
			"0011111110",
			"0010001031",
			"1000101001"]

	gold_df1 = ["4444444444",
				"4414111111",
				"4414144444",
				"1114141114",
				"4444141414",
				"4414141414",
				"4414441414",
				"4411111414",
				"4444444414",
				"4411111114",
				"4414441031",
				"1444141001"]
					 
	gold_bf1 = ["4444444444",
				"4414111111",
				"4414144444",
				"1114141114",
				"4444141414",
				"4414141414",
				"4414441414",
				"4411111414",
				"4444444414",
				"4411111114",
				"4414441031",
				"1444141001"]

	student_df1 = sc.dfs(init_map(data1))
	if check_map_equal(student_df1, init_map(gold_df1)):
		print "Pass dfs for map1"
	else:
		print "Fail dfs for map1"
		exit(1)
	exit(0)

if __name__== "__main__":
	main()