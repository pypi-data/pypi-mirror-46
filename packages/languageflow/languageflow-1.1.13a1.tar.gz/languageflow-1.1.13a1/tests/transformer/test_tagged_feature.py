# -*- coding: utf-8 -*-
from unittest import TestCase
from languageflow.transformer.tagged import TaggedTransformer

templates = [
        "T[0].lower", "T[-1].lower", "T[1].lower",
        "T[0].istitle", "T[-1].istitle", "T[1].istitle",
        "T[-2]", "T[-1]", "T[0]", "T[1]", "T[2]",  # unigram
        "T[-2,-1]", "T[-1,0]", "T[0,1]", "T[1,2]",  # bigram
        "T[-1][1]", "T[-2][1]", "T[-3][1]",  # dynamic feature
        "T[-3,-2][1]", "T[-2,-1][1]",
        "T[-3,-1][1]"
    ]


class TestTaggedFeature(TestCase):
    def setUp(self):
        self.tagged_transformer = TaggedTransformer(templates)

    def test_word2features(self):
        sent = [["người", "N", "B-NP"], ["nghèo", "A", "I-NP"]]
        actual = self.tagged_transformer.transform([sent])[0][0][0]
        expected = "T[0].lower=người"
        self.assertEqual(expected, actual)

