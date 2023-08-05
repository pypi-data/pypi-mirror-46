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
import itertools


class JiebaPsegExtractor(EntityExtractor):

    provides = ["entities"]

    defaults = {
        # nr：人名，ns：地名，nt：机构名, m: numbers
        "part_of_speech": ['nr']
    }

    def __init__(self, component_config=None):
        # type: (Optional[Dict[Text, Text]]) -> None

        super(JiebaPsegExtractor, self).__init__(component_config)

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData) -> None
        features = self.component_config.get("features", [])

        # self.component_config =
        # config.for_component(self.name, self.defaults)

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None
        print(message)
        extracted = self.add_extractor_name(self.posseg_cut_examples(message))

        message.set("entities", extracted, add_to_output=True)

    def posseg_cut_examples(self, example):
        sorted_entities = example.get("entities", [])
        part_of_speech = self.component_config["part_of_speech"]
        sorted_list = self.posseg(example.text, part_of_speech)
        sorted_entities = []
        for idx, word in enumerate(sorted_list):
            if len(sorted_list) == 1:
                sorted_entities.append({
                                    'start': sorted_list[idx]['start'],
                                    'end': sorted_list[idx]['end'],
                                    'value': sorted_list[idx]['value'],
                                    'entity': sorted_list[idx]['entity']
                                })
            else:
                if idx < (len(sorted_list)-1):
                    if sorted_list[idx]['end'] == sorted_list[idx+1]['start']:
                        sorted_entities.append({
                                        'start': sorted_list[idx]['start'],
                                        'end': sorted_list[idx+1]['end'],
                                        'value': sorted_list[idx]['value'] +
                                        sorted_list[idx+1]['value'],
                                        'entity': sorted_list[idx]['entity']
                                    })
                    else:
                        sorted_entities.append({
                                        'start': sorted_list[idx]['start'],
                                        'end': sorted_list[idx]['end'],
                                        'value': sorted_list[idx]['value'],
                                        'entity': sorted_list[idx]['entity']
                                    })
        print(sorted_list)
        return sorted_entities

    @staticmethod
    def posseg(text, part_of_speech):
        # type: (Text) -> List[Token]

        import jieba
        import jieba.posseg as pseg
        result = []
        for (word, start, end) in jieba.tokenize(text):
            pseg_data = [(w, f) for (w, f) in pseg.cut(word)]
            for pseg_dict in pseg_data:
                if pseg_dict[1] in part_of_speech:
                    result.append({'value': pseg_dict[0],
                                   'entity': pseg_dict[1],
                                   'start': start,
                                   'end': end})
        # print(result)
        return result

    @classmethod
    def load(cls,
             meta: Dict[Text, Any],
             model_dir=None,  # type: Optional[Text]
             model_metadata=None,  # type: Optional[Metadata]
             cached_component=None,  # type: Optional[Component]
             **kwargs  # type:**Any
             ):

        # meta = model_metadata.for_component(cls.name)

        return cls(meta)
