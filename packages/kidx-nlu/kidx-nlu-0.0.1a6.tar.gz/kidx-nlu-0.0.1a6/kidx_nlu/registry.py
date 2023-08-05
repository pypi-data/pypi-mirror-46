"""This is a somewhat delicate package. It contains all registered components
and preconfigured templates.

Hence, it imports all of the components. To avoid cycles, no component should
import this in module scope."""

import logging
import typing
from typing import Any, Dict, List, Optional, Text, Type

from kidx_nlu import utils
from kidx_nlu.classifiers.fastText_sentiment_classifier import FastTextSentimentClassifier
from kidx_nlu.classifiers.embedding_intent_classifier import \
    EmbeddingIntentClassifier
from kidx_nlu.classifiers.keyword_intent_classifier import \
    KeywordIntentClassifier
from kidx_nlu.classifiers.mitie_intent_classifier import MitieIntentClassifier
from kidx_nlu.classifiers.sklearn_intent_classifier import \
    SklearnIntentClassifier
from kidx_nlu.classifiers.embedding_bert_intent_classifier import \
    EmbeddingBertIntentClassifier
from kidx_nlu.extractors.crf_entity_extractor import CRFEntityExtractor
from kidx_nlu.extractors.duckling_http_extractor import DucklingHTTPExtractor
from kidx_nlu.extractors.entity_synonyms import EntitySynonymMapper
from kidx_nlu.extractors.mitie_entity_extractor import MitieEntityExtractor
from kidx_nlu.extractors.spacy_entity_extractor import SpacyEntityExtractor
from kidx_nlu.featurizers.count_vectors_featurizer import \
    CountVectorsFeaturizer
from kidx_nlu.featurizers.mitie_featurizer import MitieFeaturizer
from kidx_nlu.featurizers.ngram_featurizer import NGramFeaturizer
from kidx_nlu.featurizers.regex_featurizer import RegexFeaturizer
from kidx_nlu.featurizers.spacy_featurizer import SpacyFeaturizer
from kidx_nlu.featurizers.bert_vectors_featurizer import BertVectorsFeaturizer
from kidx_nlu.model import Metadata
from kidx_nlu.tokenizers.jieba_tokenizer import JiebaTokenizer
from kidx_nlu.tokenizers.mitie_tokenizer import MitieTokenizer
from kidx_nlu.tokenizers.spacy_tokenizer import SpacyTokenizer
from kidx_nlu.tokenizers.whitespace_tokenizer import WhitespaceTokenizer
from kidx_nlu.tokenizers.pku_tokenizer import PkuTokenizer
from kidx_nlu.utils.mitie_utils import MitieNLP
from kidx_nlu.utils.spacy_utils import SpacyNLP

from kidx_nlu.extractors.jieba_pseg_extractor import JiebaPsegExtractor
from kidx_nlu.extractors.PyLTP_extractor import PyLTPEntityExtractor
from kidx_nlu.extractors.bilstm_crf_entity_extractor import \
    BilstmCRFEntityExtractor

if typing.TYPE_CHECKING:
    from kidx_nlu.components import Component
    from kidx_nlu.config import KidxNLUModelConfig

logger = logging.getLogger(__name__)


# Classes of all known components. If a new component should be added,
# its class name should be listed here.
component_classes = [
    # utils
    SpacyNLP, MitieNLP,
    # tokenizers
    MitieTokenizer, SpacyTokenizer, WhitespaceTokenizer, JiebaTokenizer, PkuTokenizer,
    # extractors
    SpacyEntityExtractor, MitieEntityExtractor, CRFEntityExtractor,
    DucklingHTTPExtractor, EntitySynonymMapper, JiebaPsegExtractor,
    PyLTPEntityExtractor, BilstmCRFEntityExtractor,
    # featurizers
    SpacyFeaturizer, MitieFeaturizer, NGramFeaturizer, RegexFeaturizer,
    CountVectorsFeaturizer, BertVectorsFeaturizer,
    # classifiers
    SklearnIntentClassifier, MitieIntentClassifier, KeywordIntentClassifier,
    EmbeddingIntentClassifier, EmbeddingBertIntentClassifier, FastTextSentimentClassifier
]

# Mapping from a components name to its class to allow name based lookup.
registered_components = {c.name: c for c in component_classes}

# DEPRECATED ensures compatibility, will be remove in future versions
old_style_names = {
    "nlp_spacy": "SpacyNLP",
    "nlp_mitie": "MitieNLP",
    "ner_spacy": "SpacyEntityExtractor",
    "ner_mitie": "MitieEntityExtractor",
    "ner_crf": "CRFEntityExtractor",
    "ner_duckling_http": "DucklingHTTPExtractor",
    "ner_bilstm_crf": "BilstmCRFEntityExtractor",
    "ner_jieba_pseg": "JiebaPsegExtractor",
    "ner_pyltp": "PyLTPEntityExtractor",
    "ner_synonyms": "EntitySynonymMapper",
    "intent_featurizer_spacy": "SpacyFeaturizer",
    "bert_vectors_featurizer": "BertVectorsFeaturizer",
    "intent_featurizer_mitie": "MitieFeaturizer",
    "intent_featurizer_ngrams": "NGramFeaturizer",
    "intent_entity_featurizer_regex": "RegexFeaturizer",
    "intent_featurizer_count_vectors": "CountVectorsFeaturizer",
    "tokenizer_mitie": "MitieTokenizer",
    "tokenizer_spacy": "SpacyTokenizer",
    "tokenizer_whitespace": "WhitespaceTokenizer",
    "tokenizer_jieba": "JiebaTokenizer",
    "pku_tokenizer": "PkuTokenizer",
    "intent_classifier_sklearn": "SklearnIntentClassifier",
    "intent_classifier_mitie": "MitieIntentClassifier",
    "intent_classifier_keyword": "KeywordIntentClassifier",
    "intent_classifier_tensorflow_embedding": "EmbeddingIntentClassifier",
    "fastText_sentiment_classifier": "FastTextSentimentClassifier",
    "intent_classifier_tensorflow_embedding_bert":
        "EmbeddingBertIntentClassifier"
}

# To simplify usage, there are a couple of model templates, that already add
# necessary components in the right order. They also implement
# the preexisting `backends`.
registered_pipeline_templates = {
    "pretrained_embeddings_spacy": [
        "SpacyNLP",
        "SpacyTokenizer",
        "SpacyFeaturizer",
        "RegexFeaturizer",
        "CRFEntityExtractor",
        "EntitySynonymMapper",
        "SklearnIntentClassifier",
    ],
    "keyword": [
        "KeywordIntentClassifier",
    ],
    "supervised_embeddings": [
        "WhitespaceTokenizer",
        "RegexFeaturizer",
        "CRFEntityExtractor",
        "EntitySynonymMapper",
        "CountVectorsFeaturizer",
        "EmbeddingIntentClassifier"
    ]
}


def pipeline_template(s: Text) -> Optional[List[Dict[Text, Text]]]:
    components = registered_pipeline_templates.get(s)

    if components:
        # converts the list of components in the configuration
        # format expected (one json object per component)
        return [{"name": c} for c in components]

    else:
        return None


def get_component_class(component_name: Text) -> Type['Component']:
    """Resolve component name to a registered components class."""

    if component_name not in registered_components:
        if component_name not in old_style_names:
            try:
                return utils.class_from_module_path(component_name)
            except Exception:
                raise Exception(
                    "Failed to find component class for '{}'. Unknown "
                    "component name. Check your configured pipeline and make "
                    "sure the mentioned component is not misspelled. If you "
                    "are creating your own component, make sure it is either "
                    "listed as part of the `component_classes` in "
                    "`kidx_nlu.registry.py` or is a proper name of a class "
                    "in a module.".format(component_name))
        else:
            # DEPRECATED ensures compatibility, remove in future versions
            logger.warning("DEPRECATION warning: your nlu config file "
                           "contains old style component name `{}`, "
                           "you should change it to its class name: `{}`."
                           "".format(component_name,
                                     old_style_names[component_name]))
            component_name = old_style_names[component_name]

    return registered_components[component_name]


def load_component_by_meta(component_meta: Dict[Text, Any],
                           model_dir: Text,
                           metadata: Metadata,
                           cached_component: Optional['Component'],
                           **kwargs: Any
                           ) -> Optional['Component']:
    """Resolves a component and calls its load method.

    Inits it based on a previously persisted model.
    """

    # try to get class name first, else create by name
    component_name = component_meta.get('class', component_meta['name'])
    component_class = get_component_class(component_name)
    return component_class.load(component_meta, model_dir, metadata,
                                cached_component, **kwargs)


def create_component_by_config(component_config: Dict[Text, Any],
                               config: 'KidxNLUModelConfig'
                               ) -> Optional['Component']:
    """Resolves a component and calls it's create method.

    Inits it based on a previously persisted model.
    """

    # try to get class name first, else create by name
    component_name = component_config.get('class', component_config['name'])
    component_class = get_component_class(component_name)

    return component_class.create(component_config, config)
