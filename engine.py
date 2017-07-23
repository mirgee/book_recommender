import heapq
import similarities


def recommend(user_id, k, explicit_ratings, similarity=similarities.pearson_similarity):
	scores = [(similarity(user_id, other_user_id, explicit_ratings), other_user_id) for other_user_id, group in \
	          explicit_ratings.groupby('User-ID') if other_user_id != user_id]

	heapq.nlargest(k, scores)

	print(scores)

	recomms = {}

	grouped_ratings = explicit_ratings.groupby('User-ID')

	user_ranked = grouped_ratings.get_group(user_id)
	for sim, other_user_id in scores:
		# Here we need to loop over all the books other user ranked
		other_ranked = grouped_ratings.get_group(other_user_id)

		for row, index in other_ranked:
			if row['ISBN'] not in user_ranked['ISBN']:
				weight = sim * row['Book-Rating']

				if row['ISBN'] in recomms:
					s, weights = recomms[row['ISBN']]
					recomms[row['ISBN']] = (s + sim, weights + [weight])
				else:
					recomms[row['ISBN']] = (sim, [weight])

	for r in recomms:
		sim, item = recomms[r]
		recomms[r] = sum(item) / sim

	return recomms