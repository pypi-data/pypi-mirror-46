from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import warnings

from builtins import str
from typing import Any
from typing import Dict
from typing import Optional
from typing import Text

from kidx_nlu import utils
from kidx_nlu.extractors import EntityExtractor
from kidx_nlu.model import Metadata
from kidx_nlu.training_data import Message
from kidx_nlu.training_data import TrainingData
from kidx_nlu.utils import write_json_to_file
from pyltp import Segmentor, Postagger


class PyLTPEntityExtractor(EntityExtractor):

    provides = ["entities"]

    requires = ['tokens']

    defaults = {
        "model_path": None,  # Nh: name Ni: organization Ns: place
        "part_of_speech": ['nh'],
        "rename_to_entity": ['username'],  # rename 'nh' to 'username'
        "dictionary_path": None  # customize dictionary
    }

    def __init__(self, component_config=None):
        # type: (Optional[Dict[Text, Text]]) -> None

        super(PyLTPEntityExtractor, self).__init__(component_config)
        self.model_path = self.component_config.get('model_path')
        self.dictionary_path = self.component_config.get('dictionary_path')

        self.segmentor = Segmentor()
        self.postagger = Postagger()
        if self.dictionary_path is None:
            self.segmentor.load(self.model_path + "/cws.model")
            self.postagger.load(self.model_path+"/pos.model")
        else:
            self.segmentor.load_with_lexicon(
                self.model_path + "/cws.model", self.dictionary_path)
            self.postagger.load_with_lexicon(
                self.model_path+"/pos.model", self.dictionary_path)

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["pyltp"]

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None
        extracted = self.extract_entities(message)
        message.set("entities", extracted, add_to_output=True)

    def extract_entities(self, message):
        # type: (Message) -> List[Dict[Text, Any]]
        # Set your own model path
        sentence = message.text
        result = self.cut_tokenize_pos(sentence)

        raw_entities = message.get("entities", [])
        temp_result = []

        for word, start, end, postag in result:
            part_of_speech = self.component_config["part_of_speech"]
            rename_to_entity = self.component_config["rename_to_entity"]

            if postag in part_of_speech:
                entity_index = part_of_speech.index(postag)
                rename_entity = rename_to_entity[entity_index] or postag

                temp_result.append({
                    'start': start,
                    'end': end,
                    'value': word,
                    'entity': rename_entity,
                    'extractor': self.name
                })

        def concat_name(first, second):
            result, isconcat = [], False
            if first['end'] == second['start']:
                result.append({
                    'start': first['start'],
                    'end': second['end'],
                    'value': first['value']+second['value'],
                    'entity': first['entity'],
                    'extractor': self.name
                })
                isconcat = True
            return result, isconcat

        searchindex = 0
        raw_entities = []
        while searchindex < len(temp_result):
            if searchindex + 1 >= len(temp_result):
                raw_entities.append(temp_result[searchindex])
                searchindex += 1
            else:
                concat_result, isconcat = concat_name(
                    temp_result[searchindex], temp_result[searchindex + 1])
                if isconcat:
                    raw_entities.extend(concat_result)
                    searchindex += 2
                else:
                    raw_entities.append(temp_result[searchindex])
                    searchindex += 1

        return raw_entities

    def cut_tokenize_pos(self, text: Text):
        words = self.segmentor.segment(text)
        postags = self.postagger.postag(words)
        tokenized = zip(words, postags)

        result, start = [], 0
        for (word, pos) in tokenized:
            width = len(word)
            result.append((word, start, start+width, pos))
            start += width
        return result

    @classmethod
    def load(cls,
             meta: Dict[Text, Any],
             model_dir=None,  # type: Optional[Text]
             model_metadata=None,  # type: Optional[Metadata]
             cached_component=None,  # type: Optional[Component]
             **kwargs  # type: **Any
             ):

        # meta = model_metadata.for_component(cls.name)
        return cls(meta)
