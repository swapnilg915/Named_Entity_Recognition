# -*- coding: utf-8 -*-
import json, traceback
import regex as re
import spacy
nlp = spacy.load('en_core_web_md')
from stanford_ner import stanfordNer

class Ner(object):
	
	def __init__(self):
		self.debug = 1
		self.stanford_ner_obj = stanfordNer()

	""" clean the text data """
	def cleanText(self, text):
		text = str(text)
		text = re.sub(r"[^a-zA-Z0-9]", " ", text)
		text = re.sub("\s+" , " ", text)
		return text	

	""" Named entity recognition using spacy NER Tagger """
	def spacyNerTagger(self, text):
		entities = []
		try:
			doc = nlp(text)
			entities = [(entity.label_, entity.text) for entity in doc.ents]
		except Exception as e:
			print('\n Error in spacyNerTagger --- ',e,'\n ',traceback.format_exc())
			pass
		return entities

	def stanfordNerTagger(self, text):
		entities = []
		try:
			stanford_output = self.stanford_ner_obj.get_entities(text)
		except Exception as e:
			print('\n Error in stanfordNerTagger --- ',e,'\n ',traceback.format_exc())
			pass
		return stanford_output

	def getEntities(self, text):
		try:
			print("\n input text --- ", text)
			final_output = {"PERSON":[], "LOCATION":[], "ORGANIZATION":[], 'MONEY':[], 'TIME':[], "DATE":[]}

			#================================ #3. extract STANFORD entities ===================================
			stanford_output = self.stanfordNerTagger(text)
			if self.debug: print("\n stanford corenlp model output --- ", stanford_output)

			for i in range(0, len(stanford_output)):
				if 'org' in stanford_output[i][1].lower() and stanford_output[i][0].lower().strip() not in ['organization', 'inc']: final_output['ORGANIZATION'].append(stanford_output[i][0].title())
				elif stanford_output[i][1] in ['LOCATION', 'GPE', 'FAC']: final_output['LOCATION'].append(stanford_output[i][0].title())
				elif stanford_output[i][1] == 'PERSON': final_output['PERSON'].append(stanford_output[i][0].title())
				elif stanford_output[i][1] == 'MONEY': final_output['MONEY'].append(stanford_output[i][0].title())
				elif stanford_output[i][1] == 'TIME': final_output['TIME'].append(stanford_output[i][0].title())
				elif stanford_output[i][1] == 'DATE': final_output['DATE'].append(stanford_output[i][0].title())

			#=============================== #4. extract SPACY entities ====================================
			spacy_output = self.spacyNerTagger(text)
			spacy_output = [ (tpl[1], tpl[0]) for tpl in spacy_output]
			spacy_output = list(set(spacy_output))
			if self.debug: print("\n spacy md model output --- ",spacy_output)

			for i in range(0, len(spacy_output)):
				if spacy_output[i][1] in ['LOC']: final_output['LOCATION'].append(spacy_output[i][0].title())
				# elif spacy_output[i][1] == 'PERSON': self.final_output['PERSON'].append(spacy_output[i][0].title())
				elif spacy_output[i][1] == 'MONEY': final_output['MONEY'].append(spacy_output[i][0].title())
				elif spacy_output[i][1] == 'TIME': final_output['TIME'].append(spacy_output[i][0].title())
				elif spacy_output[i][1] == 'DATE': final_output['DATE'].append(spacy_output[i][0].title())

			#================================= Final Entity SET ==========================================
			final_output_unique = {"PERSON":[], "LOCATION":[], "ORGANIZATION":[], 'MONEY':[], 'TIME':[], "DATE":[]}
			for k,v in final_output.items():
				final_output_unique[k].extend(list(set(v)))

		except Exception as e:
			print("\n Erro in getEntities --- ",e,"\n",traceback.format_exc())
		return final_output_unique

			
	def main(self, text):
		try:
			extracted_entities = self.getEntities(text)
		except Exception as e:
			print("\n Error in ner main --- ",e,"\n",traceback.format_exc())
	
	
if __name__ == '__main__':
	obj = Ner()
	text = "Thanks, CAT Technology Inc jobs@catamerica.com. CAT - New Jersey 377 Route 17 South Suite # 208, Hasbrouck Heights, NJ 07604, USA, 201-255-0319 x 155. For more jobs please visit our website www.catamerica.com."
	obj.main(text)