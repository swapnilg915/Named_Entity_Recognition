from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.chunk import conlltags2tree
from nltk.tree import Tree

class stanfordNer(object):
	
	def __init__(self):
		self.st = StanfordNERTagger('../../stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz','../../stanford-ner-2018-10-16/stanford-ner.jar')
		print("\n loaded models ...")
	
	def stanfordNE2BIO(self, tagged_sent):
		try:
			bio_tagged_sent = []
			prev_tag = "O"
			for token, tag in tagged_sent:
				if tag == "O": #O
					bio_tagged_sent.append((token, tag))
					prev_tag = tag
					continue
				if tag != "O" and prev_tag == "O": # Begin NE
					bio_tagged_sent.append((token, "B-"+tag))
					prev_tag = tag
				elif prev_tag != "O" and prev_tag == tag: # Inside NE
					bio_tagged_sent.append((token, "I-"+tag))
					prev_tag = tag
				elif prev_tag != "O" and prev_tag != tag: # Adjacent NE
					bio_tagged_sent.append((token, "B-"+tag))
					prev_tag = tag

		except Exception as e:			
			print("\n Error in stanfordNE2BIO --- ", e,"\n ",traceback.format_exc())
			pass
		return bio_tagged_sent
	
	
	def stanfordNE2tree(self, bio_tagged_sent):
		
		try:
			try:
				sent_tokens, sent_ne_tags = zip(*bio_tagged_sent)
			except:
				sent_tokens=('NaN')
				sent_ne_tags=("O")
			try:
				sent_pos_tags = [pos for token, pos in pos_tag(sent_tokens)]
			except:
				sent_pos_tags = [pos for token, pos in [('NaN', 'NN')]]
		
			sent_conlltags = [(token, pos, ne) for token, pos, ne in zip(sent_tokens, sent_pos_tags, sent_ne_tags)]
			ne_tree = conlltags2tree(sent_conlltags)

		except Exception as e:			
			print("\n Error in stanfordNE2tree --- ", e,"\n ",traceback.format_exc())
			pass
		return ne_tree
	
	
	def get_entities(self, body):
		ne_in_sent = []
		try:
			ne_tagged_sent = self.st.tag(word_tokenize(str(body)))

			# [('Hi', 'O'), ('Jay', 'PERSON'), ('I', 'O'), ('intend', 'O'), ('to', 'O'), ('reach', 'O'), ('you', 'O'), ('to', 'O'), ('know', 'O'), ('that', 'O'), ('Are', 'O'), ('you', 'O'), ('looking', 'O'), ('for', 'O'), ('this', 'O'), ('opportunity', 'O'), ('which', 'O'), ('need', 'O'), ('to', 'O'), ('fill', 'O'), ('with', 'O'), ('our', 'O'), ('client', 'O'), ('.', 'O'), ('I', 'O'), ('would', 'O'), ('appreciate', 'O'), ('if', 'O'), ('you', 'O'), ('share', 'O'), ('your', 'O'), ('details', 'O'), ('for', 'O'), ('this', 'O'), ('open', 'O'), ('position', 'O'), ('on', 'O'), ('following', 'O'), ('technology', 'O'), ('with', 'O'), ('your', 'O'), ('confirmation', 'O'), ('ASAP', 'ORGANIZATION'), ('Position', 'ORGANIZATION'), ('Location', 'ORGANIZATION'), ('New', 'ORGANIZATION'), ('York', 'ORGANIZATION'), ('NY', 'ORGANIZATION'), ('Duration', 'ORGANIZATION'), ('6', 'O'), ('Month', 'O'), ('Required', 'O'), ('skills', 'O'), ('.', 'O'), ('.', 'O'), ('Hands', 'O'), ('on', 'O'), ('back', 'O'), ('end', 'O'), ('.', 'O'), ('services', 'O'), ('.', 'O'), ('Thanks', 'O')]

			bio_tagged_sent = self.stanfordNE2BIO(ne_tagged_sent)

			# [('Hi', 'O'), ('Jay', 'B-PERSON'), ('I', 'O'), ('intend', 'O'), ('to', 'O'), ('reach', 'O'), ('you', 'O'), ('to', 'O'), ('know', 'O'), ('that', 'O'), ('Are', 'O'), ('you', 'O'), ('looking', 'O'), ('for', 'O'), ('this', 'O'), ('opportunity', 'O'), ('which', 'O'), ('need', 'O'), ('to', 'O'), ('fill', 'O'), ('with', 'O'), ('our', 'O'), ('client', 'O'), ('.', 'O'), ('I', 'O'), ('would', 'O'), ('appreciate', 'O'), ('if', 'O'), ('you', 'O'), ('share', 'O'), ('your', 'O'), ('details', 'O'), ('for', 'O'), ('this', 'O'), ('open', 'O'), ('position', 'O'), ('on', 'O'), ('following', 'O'), ('technology', 'O'), ('with', 'O'), ('your', 'O'), ('confirmation', 'O'), ('ASAP', 'B-ORGANIZATION'), ('Position', 'I-ORGANIZATION'), ('Location', 'I-ORGANIZATION'), ('New', 'I-ORGANIZATION'), ('York', 'I-ORGANIZATION'), ('NY', 'I-ORGANIZATION'), ('Duration', 'I-ORGANIZATION'), ('6', 'O'), ('Month', 'O'), ('Required', 'O'), ('skills', 'O'), ('.', 'O'), ('.', 'O'), ('Hands', 'O'), ('on', 'O'), ('back', 'O'), ('end', 'O'), ('.', 'O'), ('services', 'O'), ('.', 'O'), ('Thanks', 'O')]

			ne_tree = self.stanfordNE2tree(bio_tagged_sent)

			# Tree('S', [('Hi', 'NNP'), Tree('PERSON', [('Jay', 'NNP')]), ('I', 'PRP'), ('intend', 'VBP'), ('to', 'TO'), ('reach', 'VB'), ('you', 'PRP'), ('to', 'TO'), ('know', 'VB'), ('that', 'DT'), ('Are', 'NNP'), ('you', 'PRP'), ('looking', 'VBG'), ('for', 'IN'), ('this', 'DT'), ('opportunity', 'NN'), ('which', 'WDT'), ('need', 'VBP'), ('to', 'TO'), ('fill', 'VB'), ('with', 'IN'), ('our', 'PRP$'), ('client', 'NN'), ('.', '.'), ('I', 'PRP'), ('would', 'MD'), ('appreciate', 'VB'), ('if', 'IN'), ('you', 'PRP'), ('share', 'NN'), ('your', 'PRP$'), ('details', 'NNS'), ('for', 'IN'), ('this', 'DT'), ('open', 'JJ'), ('position', 'NN'), ('on', 'IN'), ('following', 'VBG'), ('technology', 'NN'), ('with', 'IN'), ('your', 'PRP$'), ('confirmation', 'NN'), Tree('ORGANIZATION', [('ASAP', 'NNP'), ('Position', 'NNP'), ('Location', 'NNP'), ('New', 'NNP'), ('York', 'NNP'), ('NY', 'NNP'), ('Duration', 'NNP')]), ('6', 'CD'), ('Month', 'NNP'), ('Required', 'NNP'), ('skills', 'NNS'), ('.', '.'), ('.', '.'), ('Hands', 'VBZ'), ('on', 'IN'), ('back', 'JJ'), ('end', 'NN'), ('.', '.'), ('services', 'NNS'), ('.', '.'), ('Thanks', 'NNS')])
			
			ne_in_sent = [ ( " ".join([token for token, pos in subtree.leaves()]),  subtree.label()) for subtree in ne_tree if type(subtree) == Tree]

			# [('Jay', 'PERSON'), ('ASAP Position Location New York NY Duration', 'ORGANIZATION')]
			ne_in_sent = list(set(ne_in_sent))
			
		except Exception as e:
			print("\n error in stanford ner get_entities --- ", e, "\n ",traceback.format_exc()) 
			pass   
		return ne_in_sent


if __name__ == '__main__':
	obj = stanfordNer()
	text = "It be nice talk with you over the phone . Here , be a JD below . Take a look on it and if you be comfortable with the rate and the techanicalities , please send me your update resume along with rate confirmation for the further process . *Title - Drupal Developer Location - Sunnyvale CA Duration - 6+ months * *Rate - 70 $ /hr on C2C or 1099 . * *Client - Ariba* Need strong Senior PHP/Drupal & CSS/Javascript/HTML5 Developers ( front-end and backend ) for 6+ month contract local to bay area/SF CA . This be an excellent opportunity for an experience PHP web developer to help on our web project which can be extend . *Required Skills* - 4+ years development experience in a LAMP environment ( Linux , Apache MySQL , PHP ) - 2+ years JavasScript and jQuery development experience - 2+ years professional Drupal development experience"
	obj.get_entities(text)
