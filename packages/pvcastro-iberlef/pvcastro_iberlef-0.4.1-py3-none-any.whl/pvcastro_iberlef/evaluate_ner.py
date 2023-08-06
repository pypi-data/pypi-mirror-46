# coding: utf-8

from allennlp.predictors.predictor import Predictor
from allennlp.models.archival import load_archive
from allennlp.common.util import lazy_groups_of
from typing import List, Iterator
from allennlp.data import Instance
import logging, os, fire
from pathlib import Path

log = logging.getLogger('allennlp')


def evaluate(model_path, document_path, cuda_device=-1, batch_size=64, predictions_file='predictions',
             scores_file='scores'):
    model_path = Path(model_path)

    # model_path = '/media/discoD/models/elmo/ner_elmo_harem_pt/'
    # model_path = '/media/discoD/models/elmo/ner_elmo_harem_no_validation/'
    # document_path = '/home/pedro/repositorios/entidades/dataset/harem/harem_test_selective_conll2003.txt'

    def get_instance_data(document_path) -> Iterator[Instance]:
        yield from predictor._dataset_reader.read(document_path)

    def predict_instances(batch_data: List[Instance]) -> Iterator[str]:
        yield predictor.predict_batch_instance(batch_data)

    archive = load_archive(archive_file=model_path / 'model.tar.gz', cuda_device=cuda_device,
                           overrides='{model:{verbose_metrics:true},dataset_reader:{type:"conll2003"}}')
    predictor = Predictor.from_archive(archive)

    count = 0

    predictions_file = predictions_file + '.txt'
    scores_file = scores_file + '.txt'

    with open(predictions_file, mode='w', encoding='utf8') as out_file:
        for batch in lazy_groups_of(get_instance_data(document_path), batch_size):
            for _, results in zip(batch, predict_instances(batch)):
                for idx, result in enumerate(results):
                    count += 1
                    real_sentence = batch[idx]
                    real_tags = real_sentence.fields['tags'].labels
                    words = result['words']
                    predicted_labels = result['tags']
                    for word_idx, (word, tag) in enumerate(zip(words, predicted_labels)):
                        out_file.write(' '.join([word, real_tags[word_idx], tag]) + '\n')
                    out_file.write('\n')
                    if count % 200 == 0:
                        log.info('Predicted %d sentences' % count)
                out_file.write('\n')
    out_file.close()
    log.info('Finished predicting %d sentences' % count)
    os.system("./%s -l < %s > %s" % ('conlleval.perl', predictions_file, scores_file))
    print(open(scores_file, mode='r', encoding='utf8').read())


if __name__ == '__main__': fire.Fire(evaluate)
