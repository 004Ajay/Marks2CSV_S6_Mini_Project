matrix = [[28, 52, 14, 5, 11, 43, 77, 10, 25, 54, 73, 17],
          [39, 44, 56, 45, 87, 78, 48, 51, 37, 66, 16, 25],
          [88, 0, 33, 31, 6, 100, 27, 40, 39, 42, 71, 40]]

num_columns = len(matrix[0])
num_rows = len(matrix)

for j in range(num_columns):
    for i in range(num_rows):
        print(matrix[i][j], end=' ')
    print()