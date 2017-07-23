import math
import pandas as pd

# Compute euclidean similarity
def euclidean_similarity(user_id1, user_id2, explicit_ratings):
	# Get the items both users ranked
	ranked1 = explicit_ratings.groupby('User-ID').get_group(user_id1)
	ranked2 = explicit_ratings.groupby('User-ID').get_group(user_id2)

	common_ranked_items = pd.merge(ranked1, ranked2, how='inner', on='ISBN').dropna(inplace=True)

	if pd.isnull(common_ranked_items):
		return 0

	rankings = [(row['Book-Rating_x'], row['Book-Rating_y']) for row, index in common_ranked_items]
	distance = [pow(rank[0] - rank[1], 2) for rank in rankings]

	return 1 / (1 + sum(distance))

# Compute pearson correlation coefficient
def pearson_similarity(user_id1, user_id2, explicit_ratings):
	# Get the items both users ranked
	ranked1 = explicit_ratings.groupby('User-ID').get_group(user_id1)
	ranked2 = explicit_ratings.groupby('User-ID').get_group(user_id2)

	common_ranked_items = pd.merge(ranked1, ranked2, how='inner', on='ISBN').dropna(inplace=True)

	if pd.isnull(common_ranked_items):
		return 0

	n = len(common_ranked_items)

	# Sums, squared sums and sum of products
	s1 = sum([row['Book-Rating_x'] for row, index in common_ranked_items])
	s2 = sum([row['Book-Rating_y'] for row, index in common_ranked_items])

	ss1 = sum([pow(row['Book-Rating_x'], 2) for row, index in common_ranked_items])
	ss2 = sum([pow(row['Book-Rating_y'], 2) for row, index in common_ranked_items])

	ps = sum([row['Book-Rating_x'] * row['Book-Rating_y'] for row, index in common_ranked_items])

	num = n * ps - (s1 * s2)

	den = math.sqrt((n * ss1 - math.pow(s1, 2)) * (n * ss2 - math.pow(s2, 2)))

	return (num / den) if den != 0 else 0
