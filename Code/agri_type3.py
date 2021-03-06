from common_methodsArticles import read_file, tokenize_stem_file, remove_stopWords, get_frequency, read_csvDictionary, dict_sum, db, splitLexisNexis
from common_methodsArticles import articleDb, splitLexisNexis_AG, absoluteFilePaths, state_map
import re,numpy as np
from collections import Counter
#import thread, time, sys
import psycopg2

#Regular expression for corruption in states
def read_data(fp):
	#for each article
	articles = splitLexisNexis_AG(fp)
	states = read_csvDictionary('/home/team3/Data/Dictionaries/us_states1.csv')
	states_short = read_csvDictionary('/home/team3/Data/Dictionaries/us_states_shortname.csv')
	agriculture = read_csvDictionary('/home/team3/Data/Dictionaries/agriculture.csv')
	crops = read_csvDictionary('/home/team3/Data/Dictionaries/crops.csv')
	
	result_type1 = {}
	result_type2 = {}
	
	for currentArticle in articles:
		#For full forms
		re_states = re.findall(r"(?=("+'|'.join(states)+r"))",currentArticle)
		for each_state in re_states:
			#replacing short forms
			if each_state in states:
				i = states.index(each_state)
				a = states_short[i]
			ag_count = len(re.findall(r"(?=("+'|'.join(agriculture)+r"))",currentArticle))
			if ag_count > 0:
				ag = re.findall(r"(?=("+'|'.join(crops)+r"))",currentArticle)
				result_type1[a] = ag
			
			else:
				continue
				
		#For short forms
		re_states_short = re.findall(r"(?=("+'|'.join(states_short)+r"))",currentArticle)
		for each_state_short in re_states_short:
			ag_count_short = len(re.findall(r"(?=("+'|'.join(agriculture)+r"))",currentArticle))
			if ag_count_short > 0:
				ag_short = re.findall(r"(?=("+'|'.join(crops)+r"))",currentArticle)
				result_type2[each_state_short] = ag_short
				
			else:
				continue
				
	'''result = {}
	for key in (result_type1.keys() | result_type2.keys()):
		if key in result_type1: result.setdefault(key, []).append(result_type1[key])
		if key in result_type2: result.setdefault(key, []).append(result_type2[key])'''
		
	'''for k, v in result_type1.items():
		print(k, v[0])
		
	for k, v in result_type2.items():
		print(k, v)
		
	return result_type1, result_type2'''
			



#Inserting data into database
	try:
		conn = psycopg2.connect("dbname='team3' user='team3' host='localhost' password='Toowie3a'")
		cur = conn.cursor()
		for k, v in result_type1.items():
			if len(v) != 0:
				for i in v:
					query = "INSERT into ftm.cropType values(%s,%s)"
					data = (k,i)
					cur.execute(query, data)
		conn.commit()
		conn.close()
		
	except:
		print("error")

#3
read_data('/home/team3/Data/Unstructed_Data/corruption/tax_evasion_01.TXT')
read_data('/home/team3/Data/Unstructed_Data/corruption/tax_evasion_02.TXT')
read_data('/home/team3/Data/Unstructed_Data/corruption/bribe_01.TXT')
read_data('/home/team3/Data/Unstructed_Data/corruption/bribe_02.TXT')
read_data('/home/team3/Data/Unstructed_Data/corruption/black_money_01.TXT')
read_data('/home/team3/Data/Unstructed_Data/corruption/black_money_02.TXT')
read_data('/home/team3/Data/Unstructed_Data/corruption/misconduct_01.TXT')
read_data('/home/team3/Data/Unstructed_Data/corruption/misconduct_02.TXT')
read_data('/home/team3/Data/Unstructed_Data/corruption/wrongdoing_01.TXT')
read_data('/home/team3/Data/Unstructed_Data/corruption/wrongdoing_02.TXT')
	
