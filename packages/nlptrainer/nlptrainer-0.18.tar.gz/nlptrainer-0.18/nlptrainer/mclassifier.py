import click
from sklearn.model_selection import train_test_split
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
from datetime import datetime
import bert
from bert import run_classifier
from bert import optimization
from bert import tokenization
import simple_data_feeder as data_feeder
import simple_model_evaluator as evaluator
from tensorflow import keras
import os
import re
import json


@click.command()
@click.option('--dataset', default='data/bot_dataset1', prompt='dataset file', help='Specify a csv file for data')
@click.option('--OUTPUT_DIR', default='OUTPUT_DIR', prompt='OUTPUT_DIR_NAME', help='Specify a directory for output files')
@click.option('--DO_DELETE', default=False, help='delete the output directory before execution?')
@click.option('--MAX_SEQ_LENGTH', default=128, prompt='MAX_SEQ_LENGTH')
@click.option('--BATCH_SIZE', default=32, prompt='BATCH_SIZE')
@click.option('--LEARNING_RATE', default=2e-5, prompt='LEARNING_RATE')
@click.option('--NUM_TRAIN_EPOCHS', default=5.0, prompt='NUM_TRAIN_EPOCHS')
@click.option('--WARMUP_PROPORTION', default=0.1, prompt='WARMUP_PROPORTION')
@click.option('--SAVE_CHECKPOINTS_STEPS', default=500, prompt='SAVE_CHECKPOINTS_STEPS')
@click.option('--SAVE_SUMMARY_STEPS', default=100, prompt='SAVE_SUMMARY_STEPS')
@click.option('--BERT_MODEL_HUB', default='https://tfhub.dev/google/bert_uncased_L-12_H-768_A-12/1', prompt='URL to Bert Model')
@click.option('--TRAIN_TEST_SPLIT', default=0.7, prompt='Train Test split rate')


def run(dataset, output_dir, do_delete, max_seq_length, batch_size, learning_rate, num_train_epochs,warmup_proportion,save_checkpoints_steps,save_summary_steps, bert_model_hub, train_test_split):
#    train, test = data_feeder.getDataSplitted('data/train.csv', 'data/train_label.csv', 'data/test.csv', 'data/test_label.csv' )
    train, test, tag_map= data_feeder.getData(dataset, train_test_split)
    if do_delete:
      try:
        tf.gfile.DeleteRecursively(output_dir)
      except:
        # Doesn't matter if the directory didn't exist
        pass
    tf.gfile.MakeDirs(output_dir)
    print('***** Model output directory: {} *****'.format(output_dir))

    tag_reverse_map = {}
    for k,v in tag_map.items():
        tag_reverse_map[v] = k

    train['tag'] = train['label'].apply(lambda x : tag_map[x])
    test['tag'] = test['label'].apply(lambda x : tag_map[x])

    label_list = test['tag'].unique()

    train_intent_count = getLabelCount(train)
    test_intent_count = getLabelCount(test)

    print('***** Training Data Set: {} *****'.format(json.dumps(train_intent_count)))
    print('***** Testing Data Set: {} *****'.format(json.dumps(test_intent_count)))
    print('***** Labels: {} *****'.format(json.dumps(tag_map)))

    tokenizer = bert.tokenization.FullTokenizer(
      vocab_file='data/vocab.txt', do_lower_case=True)

    train_features, test_features =toFeature(train, test, label_list, max_seq_length, tokenizer)
    # Compute # train and warmup steps from batch size
    num_train_steps = int(len(train_features) / batch_size * num_train_epochs)
    num_warmup_steps = int(num_train_steps * warmup_proportion)

    run_config = tf.estimator.RunConfig(
        model_dir=output_dir,
        save_summary_steps=save_summary_steps,
        save_checkpoints_steps=save_checkpoints_steps)

    model_fn = model_fn_builder(
      bert_model_hub = bert_model_hub,
      num_labels=len(label_list),
      learning_rate=learning_rate,
      num_train_steps=num_train_steps,
      num_warmup_steps=num_warmup_steps)

    estimator = tf.estimator.Estimator(
      model_fn=model_fn,
      config=run_config,
      params={"batch_size": batch_size})

    # Create an input function for training. drop_remainder = True for using TPUs.
    train_input_fn = bert.run_classifier.input_fn_builder(
        features=train_features,
        seq_length=max_seq_length,
        is_training=True,
        drop_remainder=False)

    current_time = datetime.now()
    estimator.train(input_fn=train_input_fn, max_steps=num_train_steps)


    test_input_fn = run_classifier.input_fn_builder(
        features=test_features,
        seq_length=max_seq_length,
        is_training=False,
        drop_remainder=False)

    estimator.evaluate(input_fn=test_input_fn, steps=None)

    pred_sentences = test['text']
    predictions = getPrediction(pred_sentences, label_list, max_seq_length, tokenizer, estimator)
    tp, fp, fn, precision, recall = evaluator.eval(test['tag'] , column(predictions, 2), label_list)

    result = parseResult(tp,fp,fn,precision, recall, tag_reverse_map)

    print(result)

    estimator.export_saved_model('saved_model', serving_input_receiver_fn)

    return json.dumps(result)

class PredResult:
  def __init__(self, tp, fp, fn, precision, recall):
    self.tp = tp
    self.fp = fp
    self.fn = fn
    self.precision = precision
    self.recall = recall

def parseResult(tp, fp, fn, precision, recall, map):
    result = {}
    for k,v in map.items():
        result[v] = PredResult(tp[k], fp[k], fn[k], precision[k], recall[k]).__dict__
    return result


def column(matrix, i):
    return [row[i] for row in matrix]

def analyzePredictions(predictions, class2id, id2class ):
    print(predictions)

def toFeature(train, test, label_list, max_seq_length, tokenizer):
    # Use the InputExample class from BERT's run_classifier code to create examples from the data
    train_InputExamples = train.apply(lambda x: bert.run_classifier.InputExample(guid=None, # Globally unique ID for bookkeeping, unused in this example
                                                                       text_a = x['text'],
                                                                       text_b = None,
                                                                       label = x['tag']), axis = 1)

    test_InputExamples = test.apply(lambda x: bert.run_classifier.InputExample(guid=None,
                                                                       text_a = x['text'],
                                                                       text_b = None,
                                                                       label = x['tag']), axis = 1)
    train_features = bert.run_classifier.convert_examples_to_features(train_InputExamples, label_list, max_seq_length, tokenizer)
    test_features = bert.run_classifier.convert_examples_to_features(test_InputExamples, label_list, max_seq_length, tokenizer)
    return (train_features, test_features)

def create_tokenizer_from_hub_module(bert_model_hub = "https://tfhub.dev/google/bert_uncased_L-12_H-768_A-12/1"):
    print(bert_model_hub)
    """Get the vocab file and casing info from the Hub module."""
    with tf.Graph().as_default():
        bert_module = hub.Module(bert_model_hub)
        tokenization_info = bert_module(signature="tokenization_info", as_dict=True)
    with tf.Session() as sess:
        vocab_file, do_lower_case = sess.run([tokenization_info["vocab_file"],
                                            tokenization_info["do_lower_case"]])

    return bert.tokenization.FullTokenizer(
      vocab_file=vocab_file, do_lower_case=do_lower_case)


def getTagMap(test):
    tag_set = set()
    for row in test['label'] :
        tag_set.add(row)
    tag_map = dict()
    i=0
    for tag in tag_set :
        tag_map[tag] = i
        i=i+1
    return tag_map

def getLabelCount(dataset):
    tag_map = getTagMap(dataset)
    intent_count = {}

    for key in tag_map:
        intent_count[key] =0

    for intent in dataset['label'] :
        intent_count[intent]+=1

    return intent_count


def create_model(bert_model_hub, is_predicting, input_ids, input_mask, segment_ids, labels,
                 num_labels):
  """Creates a classification model."""

  bert_module = hub.Module(
      bert_model_hub,
      trainable=True)
  bert_inputs = dict(
      input_ids=input_ids,
      input_mask=input_mask,
      segment_ids=segment_ids)
  bert_outputs = bert_module(
      inputs=bert_inputs,
      signature="tokens",
      as_dict=True)

  # Use "pooled_output" for classification tasks on an entire sentence.
  # Use "sequence_outputs" for token-level output.
  output_layer = bert_outputs["pooled_output"]

  hidden_size = output_layer.shape[-1].value

  # Create our own layer to tune for politeness data.
  output_weights = tf.get_variable(
      "output_weights", [num_labels, hidden_size],
      initializer=tf.truncated_normal_initializer(stddev=0.02))

  output_bias = tf.get_variable(
      "output_bias", [num_labels], initializer=tf.zeros_initializer())

  with tf.variable_scope("loss"):

    # Dropout helps prevent overfitting
    output_layer = tf.nn.dropout(output_layer, keep_prob=0.9)

    logits = tf.matmul(output_layer, output_weights, transpose_b=True)
    logits = tf.nn.bias_add(logits, output_bias)
    log_probs = tf.nn.log_softmax(logits, axis=-1)

    # Convert labels into one-hot encoding
    one_hot_labels = tf.one_hot(labels, depth=num_labels, dtype=tf.float32)

    predicted_labels = tf.squeeze(tf.argmax(log_probs, axis=-1, output_type=tf.int32))
    # If we're predicting, we want predicted labels and the probabiltiies.
    if is_predicting:
      return (predicted_labels, log_probs)

    # If we're train/eval, compute loss between predicted and actual label
    per_example_loss = -tf.reduce_sum(one_hot_labels * log_probs, axis=-1)
    loss = tf.reduce_mean(per_example_loss)
    return (loss, predicted_labels, log_probs)

# model_fn_builder actually creates our model function
# using the passed parameters for num_labels, learning_rate, etc.
def model_fn_builder(bert_model_hub, num_labels, learning_rate, num_train_steps,
                     num_warmup_steps):
  """Returns `model_fn` closure for TPUEstimator."""
  def model_fn(features, labels, mode, params):  # pylint: disable=unused-argument
    """The `model_fn` for TPUEstimator."""

    input_ids = features["input_ids"]
    input_mask = features["input_mask"]
    segment_ids = features["segment_ids"]
    label_ids = features["label_ids"]

    is_predicting = (mode == tf.estimator.ModeKeys.PREDICT)

    # TRAIN and EVAL
    if not is_predicting:

      (loss, predicted_labels, log_probs) = create_model(bert_model_hub,
        is_predicting, input_ids, input_mask, segment_ids, label_ids, num_labels)

      train_op = bert.optimization.create_optimizer(
          loss, learning_rate, num_train_steps, num_warmup_steps, use_tpu=False)

      # Calculate evaluation metrics.
      def metric_fn(label_ids, predicted_labels):
        accuracy = tf.metrics.accuracy(label_ids, predicted_labels)
        return {
            "eval_accuracy": accuracy,
        }

      eval_metrics = metric_fn(label_ids, predicted_labels)

      if mode == tf.estimator.ModeKeys.TRAIN:
        return tf.estimator.EstimatorSpec(mode=mode,
          loss=loss,
          train_op=train_op)
      else:
          return tf.estimator.EstimatorSpec(mode=mode,
            loss=loss,
            eval_metric_ops=eval_metrics)
    else:
      (predicted_labels, log_probs) = create_model(bert_model_hub,
        is_predicting, input_ids, input_mask, segment_ids, label_ids, num_labels)

      predictions = {
          'probabilities': log_probs,
          'labels': predicted_labels
      }
      return tf.estimator.EstimatorSpec(mode, predictions=predictions)

  # Return the actual model function in the closure
  return model_fn



def serving_input_receiver_fn():
    """Serving input_fn that builds features from placeholders

    Returns
    -------
    tf.estimator.export.ServingInputReceiver
    """
    input_ids = tf.placeholder(dtype=tf.int32, shape=[None, 128], name='input_ids')
    input_mask = tf.placeholder(dtype=tf.int32, shape=[None, 128], name='input_mask')
    segment_ids = tf.placeholder(dtype=tf.int32, shape=[None, 128], name='segment_ids')
    label_ids = tf.placeholder(dtype=tf.int32, shape=[None], name='label_ids')

    receiver_tensors = {'input_ids': input_ids, 'input_mask': input_mask,'segment_ids': segment_ids, 'label_ids': label_ids}
    return tf.estimator.export.ServingInputReceiver(receiver_tensors, receiver_tensors)



def getPrediction(in_sentences, labels, max_seq_length, tokenizer, estimator):
  input_examples = [run_classifier.InputExample(guid="", text_a = x, text_b = None, label = 0) for x in in_sentences] # here, "" is just a dummy label
  input_features = run_classifier.convert_examples_to_features(input_examples, labels, max_seq_length, tokenizer)

  predict_input_fn = run_classifier.input_fn_builder(features=input_features, seq_length=max_seq_length, is_training=False, drop_remainder=False)
  predictions = estimator.predict(predict_input_fn)
  return [(sentence, prediction['probabilities'], labels[prediction['labels']]) for sentence, prediction in zip(in_sentences, predictions)]

if __name__ == '__main__':
    run()
