import logging
import os
import typing
from typing import Any, Dict, List, Optional, Text

from kidx_nlu.components import Component
from kidx_nlu.config import KidxNLUModelConfig
from kidx_nlu.tokenizers import Token, Tokenizer
from kidx_nlu.training_data import Message, TrainingData

import pkuseg

logger = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    from kidx_nlu.model import Metadata

class PkuTokenizer(Tokenizer, Component):
    provides = ["tokens", "entities"]

    language_list = ["zh"]

    defaults = {
        "model_path": None,
        "dictionary_path": None,  # default don't load custom dictionary
        "part_of_speech": ['nr'],
        "rename_to_entity": ['username']  # rename 'nr' to 'username'
    }

    def __init__(self, component_config: Dict[Text, Any]=None) -> None:
        super(PkuTokenizer, self).__init__(component_config)
        self.model_path = self.component_config.get('model_path')
        self.dictionary_path = self.component_config.get('dictionary_path')

        if self.model_path is None:
            if self.dictionary_path is None:
                self.seg = pkuseg.pkuseg(postag=True)
            else:
                self.seg = pkuseg.pkuseg(user_dict=self.dictionary_path,postag=True)
        else:
            if self.dictionary_path is None:
                self.seg = pkuseg.pkuseg(model_name=self.model_path, postag=True)
            else:
                self.seg = pkuseg.pkuseg(model_name=self.model_path, user_dict=self.dictionary_path, postag=True)
    
    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["pkuseg"]

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None
        message.set("tokens", self.tokenize(message.text))
        extracted = self.extract_entities(message)
        message.set("entities", extracted, add_to_output=True)

    def train(self,
              training_data: TrainingData,
              config: KidxNLUModelConfig,
              **kwargs: Any) -> None:
        for example in training_data.training_examples:
            example.set("tokens", self.tokenize(example.text))

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
                concat_result, isconcat = concat_name(temp_result[searchindex], temp_result[searchindex + 1])
                if isconcat:
                    raw_entities.extend(concat_result)
                    searchindex += 2
                else:
                    raw_entities.append(temp_result[searchindex])
                    searchindex += 1

        return raw_entities

    def cut_tokenize_pos(self, text: Text):
        tokenized = self.seg.cut(text)
        result, start = [], 0
        for (word, pos) in tokenized:
            width = len(word)
            result.append((word, start, start+width, pos))
            start += width
        return result

    def tokenize(self, text: Text) -> List[Token]:
        tokenized = self.seg.cut(text)
        tokens, start = [], 0
        for (word, _) in tokenized:
            width = len(word)
            tokens.append(Token(word, start))
            start += width
        return tokens

    @classmethod
    def load(cls,
             meta: Dict[Text, Any],
             model_dir: Optional[Text]=None,
             model_metadata: Optional['Metadata']=None,
             cached_component: Optional[Component]=None,
             **kwargs: Any
             ) -> 'PkuTokenizer':

        return cls(meta)
