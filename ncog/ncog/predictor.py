import scipy
from scipy.stats import norm
import unirest

FEAMALE = 1
MALE = 0;

love_weights = [(2/3), (1/6), (1/6)]

average_female_msg_length = 58
std_female_msg_length = 48
average_male_msg_length = 47
std_male_msg_length =  44
average_female_res_rate = 392
std_female_res_rate = 156
average_male_res_rate = 392
std_male_res_rate = 156

female_msg_len_dist = norm(loc=average_female_msg_length, scale=std_female_msg_length)
male_msg_len_dist = norm(loc=average_male_msg_length, scale=std_male_msg_length)

female_res_rate_dist = norm(loc=average_female_res_rate, scale=std_female_res_rate)
male_res_rate_dist = norm(loc=average_male_res_rate, scale=std_male_res_rate)


def calculate_scores(messages, messages_to, messages_from, user_id, other_id):
	print 'CALCULATING SCORES'
	from_me = calculate_score_one_side(messages_to)
	to_me = calculate_score_one_side(messages_from)
	response_rate = calculate_response_rate(messages)

	user_score = love_weights[0]*from_me['pos'] + love_weights[1]*from_me['len'] + love_weights[2]*response_rate['user']
	other_score = love_weights[0]*to_me['pos'] + love_weights[1]*to_me['len'] + love_weights[2]*response_rate['other']

	conversation_score = {
		"user_id" : user_id,
		"other_id" : other_id,
		"user_score" : user_score,
		"other_score" : other_score,
		"user_avg_resp_rate" : response_rate['user'],
		"other_avg_resp_rate" : response_rate['other'],
		"user_avg_message_size" : from_me['len'],
		"other_avg_message_size" : to_me['len'],
		"user_num_messages" : len(messages_from),
		"other_num_messages" : len(messages_to),
		"user_avg_sentiment" : from_me['pos'],
		"user_avg_sentiment" : to_me['pos']
	}
	
	return conversation_score

def calculate_score_one_side(messages, gender=MALE):

	total_pos_score = 0
	total_len_score = 0

	for message in messages:
		try:
			if message['message']:
				print "IM PRINTING THIS: ", message['message']
				classification = Unirest.post("https://japerk-text-processing.p.mashape.com/sentiment/",
				  headers={"X-Mashape-Key": "PKPHwy5CTDmshw6wMcXOfPCMnNoGp1zre5QjsnHCyoRSG61gYa"},
				  params={"language": "english", "text": message['message']}
				)

				pos_score =  classification['probability']['pos']
				total_pos_score = total_pos_score + pos_score

				len_score = calculate_length_score(msg.length)
				total_len_score = total_len_score + len_score

		except:
			print 'fail!'
			pass

		previousMessage = message

	avg_pos_score = total_pos_score / len(messages)
	avg_len_score = total_len_score / len(messages)

	return {
		"pos": avg_pos_score,
		"len": avg_len_score
	}


def calculate_response_rate(messages):

	diff = 0

	user_total_diff = 0
	user_total_switch = 0

	other_total_diff = 0
	other_total_switch = 0

	user_last_date = 0
	other_last_date = 0

	to_me = False
	first = True

	print 'In Calculate Response Rate:  Messages length: ' + str(len(messages))
	print " First message: " + str(messages[0]) 

	for message in messages:
		if message and len(message):
			if first:
				to_me = message['to_me']
				if to_me:
					other_last_time = message['date']
				else:
					user_last_date = message['date']
				first = False
			else:
				if message['to_me'] != to_me:
					if to_me:
						diff = (message['date'] - user_last_date).total_seconds()
						other_last_date = message['date']
						other_total_diff = other_total_diff + diff
						other_total_switch = other_total_switch + 1
					else:
						diff = (message['date'] - other_last_date).total_seconds
						user_last_date = message['date']
						user_total_diff = user_total_diff + diff
						user_total_switch = user_total_switch + 1
					to_me = message['to_me']
				else:
					if to_me:
						other_last_date = message['date']
						other_total_diff = other_total_diff + diff
						other_total_switch = other_total_switch + 1
					else:
						user_last_date = message['date']
						user_total_diff = user_total_diff + diff
						user_total_switch = user_total_switch + 1
	
	user_total = 0
	if user_total_switch:
		user_total = (user_total_diff / user_total_switch)

	other_total = 0
	if other_total_switch:
		other_total = (other_total_diff / other_total_switch)
	return {
		"user" : user_total,
		"other" : other_total
	}






def calculate_length_score(user_msg_length):
	return male_msg_len_dist.cdf(user_msg_length)

def calculate_res_rate_score(user_res_rate):
	return 1.0 - male_res_rate_dist.cdf(user_res_rate)


