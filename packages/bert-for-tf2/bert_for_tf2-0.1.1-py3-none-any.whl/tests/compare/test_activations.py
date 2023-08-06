# coding=utf-8
#
# created by kpe on 23.May.2019 at 17:10
#

from __future__ import absolute_import, division, print_function

import os
import string
import unittest
import tempfile

import tensorflow as tf

from bert.loader import StockBertConfig, map_stock_config_to_params


class MiniBertFactory:

    def create_mini_bert_weights(self):
        bert_tokens = ["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"]
        bert_config = StockBertConfig(
            attention_probs_dropout_prob = 0.1,
            hidden_act                   = "gelu",
            hidden_dropout_prob          = 0.1,
            hidden_size                  = 8,
            initializer_range            = 0.02,
            intermediate_size            = 32,
            max_position_embeddings      = 16,
            num_attention_heads          = 2,
            num_hidden_layers            = 2,
            type_vocab_size              = 2,
            vocab_size                   = len(string.ascii_lowercase) + len(bert_tokens)
        )

        model_dir = tempfile.TemporaryDirectory()
        print("creating mini BERT at:", model_dir)

        bert_config_file = os.path.join(model_dir.name, "bert_config.json")
        bert_vocab_file  = os.path.join(model_dir.name, "vocab.txt")

        with open(bert_config_file, "w") as f:
            f.write(bert_config.to_json_string())
        with open(bert_vocab_file, "w") as f:
            f.write("\n".join(list(string.ascii_lowercase) + bert_tokens))

        (stock_bert, pl_input_ids, pl_mask, pl_token_type_ids) = self.create_stock_bert_graph(bert_config_file, 16)


    def create_stock_bert_graph(self, bert_config_file, max_seq_len):
        from tests.ext.tokenization import FullTokenizer
        from tests.ext.modeling import BertModel, BertConfig, get_assignment_map_from_checkpoint

        tf_placeholder = tf.compat.v1.placeholder

        pl_input_ids      = tf_placeholder(tf.int32, shape=(1, max_seq_len))
        pl_mask           = tf_placeholder(tf.int32, shape=(1, max_seq_len))
        pl_token_type_ids = tf_placeholder(tf.int32, shape=(1, max_seq_len))

        bert_config = BertConfig.from_json_file(bert_config_file)
        s_model = BertModel(config=bert_config,
                            is_training=False,
                            input_ids=pl_input_ids,
                            input_mask=pl_mask,
                            token_type_ids=pl_token_type_ids,
                            use_one_hot_embeddings=False)

        return s_model, pl_input_ids, pl_mask, pl_token_type_ids


class TestBertActivations(unittest.TestCase):

    def predict_on_stock_model(self, input_ids, input_mask, token_type_ids):
        from tests.ext.tokenization import FullTokenizer
        from tests.ext.modeling import BertModel, BertConfig, get_assignment_map_from_checkpoint

        tf_placeholder = tf.compat.v1.placeholder

        max_seq_len       = input_ids.shape[-1]
        pl_input_ids      = tf_placeholder(tf.int32, shape=(1, max_seq_len))
        pl_mask           = tf_placeholder(tf.int32, shape=(1, max_seq_len))
        pl_token_type_ids = tf_placeholder(tf.int32, shape=(1, max_seq_len))

        bert_config = BertConfig.from_json_file(self.bert_config_file)
        tokenizer = FullTokenizer(vocab_file=os.path.join(self.bert_ckpt_dir, "vocab.txt"))

        s_model = BertModel(config=bert_config,
                               is_training=False,
                               input_ids=pl_input_ids,
                               input_mask=pl_mask,
                               token_type_ids=pl_token_type_ids,
                               use_one_hot_embeddings=False)

        tvars = tf.trainable_variables()
        (assignment_map, initialized_var_names) = get_assignment_map_from_checkpoint(tvars, self.bert_ckpt_file)
        tf.train.init_from_checkpoint(self.bert_ckpt_file, assignment_map)

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            s_res = sess.run(
                s_model.get_sequence_output(),
                feed_dict={pl_input_ids:      input_ids,
                           pl_token_type_ids: token_type_ids,
                           pl_mask:           input_mask,
                           })
        return s_res

    def test_compare(self):
        bert_1 = None
        bert_2 = None
