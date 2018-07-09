import heapq
import similarities

##
def recommend(user_id, explicit_ratings, k = 5, similarity=similarities.pearson_similarity):
	# This is very inefficient - maybe cluster users, or first find a list of users that rated similar items?
	scores = [(similarity(user_id, other_user_id, explicit_ratings), other_user_id) for other_user_id, group in \
	          explicit_ratings.groupby('User-ID') if other_user_id != user_id]

	heapq.nlargest(k, scores)

	# Key: a book to be recommended, Value: (sum of s_xy for y in N, vector of s_xy*r_yi) -> r_xi
	recomms = {}

	grouped_ratings = explicit_ratings.groupby('User-ID')

	user_ranked = grouped_ratings.get_group(user_id)
	# For all users in neighbourhood
	for sim, other_user_id in scores[:k]:
		# Here we need to loop over all the books other user ranked
		other_ranked = grouped_ratings.get_group(other_user_id)
		for row, index in other_ranked:
			# We don't need to predict ratings for books already rated
			if row['ISBN'] not in user_ranked['ISBN']:
				weight = sim * row['Book-Rating']

				if row['ISBN'] in recomms:
					s, weights = recomms[row['ISBN']]
					recomms[row['ISBN']] = (s + sim, weights + [weight])
				else:
					recomms[row['ISBN']] = (sim, [weight])
	# Then we calculate the weighted average rating
	for r in recomms:
		sim, item = recomms[r]
		recomms[r] = sum(item) / sim

	return recomms