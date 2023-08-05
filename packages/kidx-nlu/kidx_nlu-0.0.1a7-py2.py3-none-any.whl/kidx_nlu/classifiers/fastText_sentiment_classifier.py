from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import typing
from typing import List, Text, Any, Optional, Dict

from kidx_nlu.components import Component
from kidx_nlu.model import Metadata
from kidx_nlu.training_data import Message
try:
    import fastText
except ImportError:
    fastText = None

logger = logging.getLogger(__name__)


class FastTextSentimentClassifier(Component):
    provides = ["sentiment_score"]

    requires = ["tokens"]

    defaults = {
        "model_path": None,
    }

    def __init__(self, component_config=None):
        # type: (Optional[Dict[Text, Text]]) -> None
        super(FastTextSentimentClassifier, self).__init__(component_config)
        model_path = self.component_config.get('model_path')
        self.fastText_model = fastText.load_model(model_path)

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["fastText"]

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None
        sentiment_score = self.get_sentiment_score(message)

        message.set("intent",
                    dict(message.get("intent", {}), 
                        **{"sentiment_score": sentiment_score}),
                    add_to_output=True)

    def get_sentiment_score(self, message):
        # type: (Message) -> List[Dict[Text, Any]]
        sentence = message.text
        label = self.fastText_model.predict(sentence)[0][0]
        if label == '__label__positive':
            sentiment_score = 2
        elif label == '__label__neutral':
            sentiment_score = 1
        elif label == '__label__negative':
            sentiment_score = 0

        return sentiment_score

    @classmethod
    def load(cls,
             meta: Dict[Text, Any],
             model_dir=None,  # type: Optional[Text]
             model_metadata=None,  # type: Optional[Metadata]
             cached_component=None,  # type: Optional[Component]
             **kwargs  # type: **Any
             ):

        return cls(meta)
