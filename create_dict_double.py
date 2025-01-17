from __future__ import absolute_import
import numpy as np
import pandas as pd
from sklearn import preprocessing
from fm.utils import save_obj, load_obj

try:
   import cPickle as pickle
except:
   import pickle

n_entity = 14951
n_relation = 1345

negative_sample_time = 1


# label encoding with regard to entity2id & relation2id
name = ['entity', 'id']
entity_id = pd.read_table('./FB15k/entity2id.txt', sep='\t', header=None, names=name, engine='python')
entity = entity_id['entity'].values.tolist()
le_entity = preprocessing.LabelEncoder()
le_entity.fit(entity)

name = ['relation', 'id']
relation_id = pd.read_table('./FB15k/relation2id.txt', sep='\t', header=None, names=name, engine='python')
relation = relation_id['relation'].values.tolist()
le_relation = preprocessing.LabelEncoder()
le_relation.fit(relation)


#################################### reading training data ###########################################
name = ['subject', 'object', 'relation']
data = pd.read_table('./FB15k/train.txt', sep='\t', header=None, names=name, engine='python')
print 'Loading training data...'

s = data['subject'].values.tolist()
o = data['object'].values.tolist()
r = data['relation'].values.tolist()

# string list to int array
subjects = np.array(le_entity.transform(s))
objects = np.array(le_entity.transform(o))
relations = np.array(le_relation.transform(r))
del s, o, r

name = ['subject', 'object', 'relation']
data = pd.read_table('./FB15k/valid.txt', sep='\t', header=None, names=name, engine='python')
print 'Loading validation data...'

s = data['subject'].values.tolist()
o = data['object'].values.tolist()
r = data['relation'].values.tolist()

# string list to int array
subjects = np.concatenate([subjects, np.array(le_entity.transform(s))])
objects = np.concatenate([objects, np.array(le_entity.transform(o))])
relations = np.concatenate([relations, np.array(le_relation.transform(r))])
del s, o, r

print 'Creating dictionary...'

sr_dict = {}
ro_dict = {}
for (s, r, o) in zip(subjects, relations, objects):
    if (s, r) in sr_dict:
        sr_dict[(s, r)] += [o]
    else:
        sr_dict[(s, r)] = [o]

    if (r, o) in ro_dict:
        ro_dict[(r, o)] += [s]
    else:
        ro_dict[(r, o)] = [s]

save_obj(sr_dict, 'sr_dict_double')
save_obj(ro_dict, 'ro_dict_double')
print 'Saved.'

print sr_dict[(3920, 791)]



