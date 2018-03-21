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
	data2= ["0000000000",
			"1111110101",
			"0300010101",
			"1111010101",
			"0001010101",
			"0100010101",
			"1111010101",
			"0000000101",
			"0111111100",
			"0000000101",
			"0111111120",
			"0000000010"]
				  
	gold_df2 = ["0000005554",
				"1111115151",
				"0555515151",
				"1111515151",
				"4441515151",
				"4144515151",
				"1111515151",
				"4444555151",
				"4111111154",
				"4444444151",
				"4111111154",
				"4444444414"]
					 
	gold_bf2 = ["4444445554",
				"1111115151",
				"0555515151",
				"1111515151",
				"4441515151",
				"4144515151",
				"1111515151",
				"4444555151",
				"4111111154",
				"4440000151",
				"4111111154",
				"4000000014"]
	student_bf2 = sc.bfs(init_map(data2))
	if check_map_equal(student_bf2, init_map(gold_bf2)):
		print "Pass bfs for map2"
	else:
		print "Fail bfs for map2"
		exit(1)
	exit(0)

if __name__== "__main__":
	main()