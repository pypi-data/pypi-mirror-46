# coding: utf-8

from allennlp.predictors.predictor import Predictor
from allennlp.models.archival import load_archive
from allennlp.common.util import lazy_groups_of
from typing import List, Iterator
from allennlp.data import Instance
from datetime import datetime
import fire
from pvcastro_iberlef.iberlef_ner_input_reader import IberLEFNERDatasetReader
from pvcastro_iberlef.tagging_scheme import convert_tag_scheme
from pathlib import Path


def log(message):
    print(datetime.now(), '-', message)


def predict(document_path, out_path, batch_size=16):

    def get_instance_data(document_path) -> Iterator[Instance]:
        yield from dataset_reader.read(Path(document_path))

    def predict_instances(batch_data: List[Instance]) -> Iterator[str]:
        yield predictor.predict_batch_instance(batch_data)

    model_path = 'https://s3.amazonaws.com/datalawyer-models/iberlef/iberlef-multiple.tar.gz'

    log('Loading model from %s' % model_path)
    archive = load_archive(archive_file=model_path,
                           overrides='{"model":{"verbose_metrics":true},"dataset_reader":{"type":"conll2003"}}')
    predictor = Predictor.from_archive(archive)
    dataset_reader = IberLEFNERDatasetReader(predictor._dataset_reader._token_indexers)

    count = 0

    with open(out_path, mode='w', encoding='utf-8') as out_file:
        log('Loading batches from %s for prediction' % document_path)
        for batch in lazy_groups_of(get_instance_data(document_path), batch_size):
            for _, results in zip(batch, predict_instances(batch)):
                convert_tag_scheme(results)
                for idx, result in enumerate(results):
                    count += 1
                    words = result['words']
                    predicted_labels = result['tags']
                    for word_idx, (word, predicted_tag) in enumerate(zip(words, predicted_labels)):
                        out_file.write(' '.join([word, predicted_tag]) + '\n')
                    out_file.write('\n')
                    if count % 100 == 0:
                        log('Predicted %d sentences' % count)
                out_file.write('\n')
    out_file.close()
    log('Finished predicting %d sentences' % count)
    log('Results saved in %s' % Path(out_path).absolute())


if __name__ == '__main__': fire.Fire(predict)
