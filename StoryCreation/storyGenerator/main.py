import random

class Concept(object):
	name=""
	def __init__(self,name):
		self.name=name

class God(object):
	name=""
	concept_list=[]

	_names=["Hekreus","Ogdur","Hejun","Alo","Doione","Qhemjir","Erasil","Davnir","Aenar","Ykeyr","Tenir","Uanh","Pharros","Ixzotl","Sovphin","Yesis","Zinos","Makdes","Sumis","Osus","Istar","Nitarin","Yzerin","Phyxara","Phydion","Quzbris","Bylir","Agtis","Dhesohr","Uaris"]
	
	@staticmethod	
	def create_domain(ratios,concepts):
		domain=[]
		domain_number=random.choice(ratios)
		for i in range(domain_number):
			concept=random.choice(concepts)
			while concept in domain: 
				concept=random.choice(concepts)
			domain.append(concept)
		return tuple(domain)

	@staticmethod
	def theogenesis(concepts,n=10):
		gods=[]
		used_names=set()
		used_domains=set()
		for i in range(n):

			domain_ratios=[0,1,1,1,1,1,2,2]

			name=random.choice(God._names)
			while name in used_names:
				name=random.choice(God._names)

			domain=God.create_domain(domain_ratios,concepts)
			while domain in used_domains:
				domain=God.create_domain(domain_ratios,concepts)

			god=God(name,domain)

			gods.append(god)
			used_names.add(name)
			used_domains.add(domain)

		return gods

	def __init__(self,name,concept_list):
		self.name=name
		self.concept_list=concept_list

	def __repr__(self):

		to_add=self.name+", god of "

		if len(self.concept_list)==0:
			to_add+="no domain"

		for i, concept in enumerate(self.concept_list):
			if i==len(self.concept_list)-1 and i!=0:
				to_add+=", and "+concept.name
			elif i!=0:
				to_add+=", "+concept.name
			else:
				to_add+=concept.name

		return to_add

class Action(object):
	name=""
	concept_list=[]

	def __init__(self,name,concept_list):
		self.name=name
		self.concept_list=concept_list

class URAction(object):
	name=""
	action_list=[]
	concept_list=[]

	def __init__(self,name,action_list,concept_list):
		self.name=name
		self.action_list=action_list
		self.concept_list=concept_list

class Item (object):
	name=""
	ur_action_list=[]
	concept_list=[]

	def __init__(self,name,ur_action_list,concept_list):
		self.name=name
		self.ur_action_list
		self.concept_list=concept_list

DEATH = Concept("DEATH")
FIRE = Concept("FIRE")
DECAY = Concept("DECAY")
RESTORATION = Concept("RESTORATION")
KNOWLEDGE = Concept("KNOWLEDGE")
MAGIC = Concept("MAGIC")
HOLY = Concept("HOLY")
LIFE = Concept("LIFE")
WEALTH = Concept("WEALTH")

ALL_CONCEPTS=[DEATH,FIRE,DECAY,RESTORATION,KNOWLEDGE,MAGIC,HOLY,LIFE,WEALTH]

print(God.theogenesis(ALL_CONCEPTS,12))