import json

with open('./game_play_activity.csv', 'w') as out:
	with open('./game_play_activity.json') as fp:
		data = json.load(fp)
		for row in data['rows']['Activity']:
			str_row = map(str, row)
			out.write(','.join(str_row) + '\n')
