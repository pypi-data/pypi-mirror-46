from seisnn.tensorflow.workflow import Workflow as Tensorflow


class Picker:
    def __init__(self, weight_dir=None):
        self.weight_dir = weight_dir
        self.backend = Tensorflow()
        self.model = self.backend.model

    def pretrain(self, pkl_list, *args, **kwargs):
        self.backend.pretrain(self.model, pkl_list, self.weight_dir, *args, **kwargs)

    def train(self, pkl_list, previous_weight=None, *args, **kwargs):
        self.backend.train(self.model, pkl_list, self.weight_dir, previous_weight=previous_weight, *args, **kwargs)

    def predict(self, pkl_dir, *args, **kwargs):
        self.backend.predict(self.model, pkl_dir, self.weight_dir, *args, **kwargs)

    def use_tensorflow(self):
        self.backend = Tensorflow()
