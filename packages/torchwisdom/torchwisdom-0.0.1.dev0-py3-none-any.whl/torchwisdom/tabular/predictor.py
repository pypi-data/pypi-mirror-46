from torchwisdom.core.predictor import _Predictor
from .utils import *
from typing import *
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchwisdom.core.utils import DatasetCollector
import pandas as pd


__all__ = ['TabularClassifierPredictor']


class TabularSupervisedPredictor(_Predictor):
    def __init__(self, model: nn.Module, data: DatasetCollector, transform=None):
        super(TabularSupervisedPredictor, self).__init__(model, data, transform)

    def _pre_check(self, *args: Any, **kwargs: Any) -> bool:
        la, lk = len(args), len(kwargs)
        if la == 0 and lk == 0:
            return False
        elif la > 0 and lk > 0:
            return False
        else:
            return True

    def _pre_predict(self, *args: Any, **kwargs: Any) -> torch.Tensor:
        is_clean = self._pre_check(*args, **kwargs)
        if is_clean:
            if len(args) > 0 and len(kwargs) == 0:
                data = torch.Tensor([args])
            else:
                if 'csv_file' in kwargs:
                    csv_file = kwargs.get('csv_file')
                    frame = pd.read_csv(csv_file)
                    data = torch.from_numpy(frame.values).float()
                elif 'dataframe' in kwargs:
                    frame = kwargs.get('dataframe')
                    data = torch.from_numpy(frame.values).float()
                elif 'tensor_data' in kwargs:
                    data = kwargs.get('tensor_data')
                elif 'numpy_data' in kwargs:
                    numpy_data = kwargs.get('numpy_data')
                    data = torch.from_numpy(numpy_data).float()
                elif 'list_data' in kwargs:
                    list_data = kwargs.get("list_data")
                    data = torch.Tensor([list_data]).float()
                else:
                    data = None
        else:
            data = None

        return data


class TabularUnsupervisedPredictor(_Predictor):
    def __init__(self):
        super(TabularUnsupervisedPredictor, self).__init__()


class TabularClassifierPredictor(TabularSupervisedPredictor):
    def __init__(self, model: nn.Module, data: DatasetCollector, transform=None):
        super(TabularClassifierPredictor, self).__init__(model, data, transform)
        if transform is None:
            self.transform = self.data.validset_attr.transform

    def _predict(self, feature: torch.Tensor):
        prediction = None
        if len(feature):
            feature.to(self.device)
            self.model = self.model.to(self.device)
            self.model.eval()
            with torch.no_grad():
                prediction = self.model(feature)
        return prediction

    def _post_predict(self, prediction: torch.Tensor, use_topk: bool = False, kval: int = 5) -> Union[None, Tuple]:
        is_clean = self._post_check(prediction)
        if is_clean:
            if not use_topk:
                return self._predict_label(prediction)
            else:
                return self._predict_topk(prediction, kval=kval)
        return None

    def _post_check(self, prediction: torch.Tensor) -> bool:
        # check output is clean (classfier label image, not image)
        return True

    def _class_label(self, class_index: torch.Tensor, is_topk=False) -> Union[str, List, None]:
        class_label = []
        classes = self.data.trainset_attr.classes
        if classes:
            if not is_topk:
                if len(class_index) >= 2:
                    for cidx in class_index:
                        class_label.append(classes[cidx])
                    return class_label
                else:
                    return classes[class_index]
            else:
                for ctn in class_index:
                    topk_label = []
                    for cidx in ctn:
                        topk_label.append(classes[cidx])
                    class_label.append(topk_label)
                return class_label
        return None

    def _predict_topk(self, prediction: torch.Tensor, kval: int = 5) -> Union[bool, Tuple]:
        if is_tensor_label(prediction):
            output = F.log_softmax(prediction, dim=1)
            ps = torch.exp(output)
            probability, class_index = ps.topk(kval, dim=1, largest=True, sorted=True)
            class_label = self._class_label(class_index, is_topk=True)
            return probability, class_index, class_label
        return False

    def _predict_label(self, prediction: torch.Tensor) -> Union[bool, Tuple]:
        if is_tensor_label(prediction):
            class_index = torch.argmax(prediction, dim=1)
            class_label = self._class_label(class_index)
            return class_index, class_label
        return False

    def predict(self, *args: Any, **kwargs: Any):
        use_topk, kval = kwargs.get("use_topk", False), kwargs.get("kval", 1)
        if 'use_topk' in kwargs: kwargs.pop("use_topk")
        if 'kval' in kwargs: kwargs.pop("kval")

        feature = self._pre_predict(*args, **kwargs)
        prediction = self._predict(feature)
        result = self._post_predict(prediction, use_topk=use_topk, kval=kval)
        return result


class TabularRegressorPredictor(TabularSupervisedPredictor):
    def __init__(self, model: nn.Module, data: DatasetCollector, transform=None):
        super(TabularRegressorPredictor, self).__init__(model, data, transform)
        if transform is None:
            self.transform = self.data.validset_attr.transform

    def _predict(self, feature: torch.Tensor):
        prediction = None
        if len(feature):
            feature.to(self.device)
            self.model = self.model.to(self.device)
            self.model.eval()
            with torch.no_grad():
                prediction = self.model(feature)
        return prediction

    def _post_predict(self, prediction: torch.Tensor) -> Union[None, Tuple]:
        is_clean = self._post_check(prediction)
        if is_clean:
            return prediction
        return None

    def _post_check(self, prediction: torch.Tensor) -> bool:
        # check output is clean (classfier label image, not image)
        return True

    def predict(self, *args: Any, **kwargs: Any):
        if 'use_topk' in kwargs: kwargs.pop("use_topk")
        if 'kval' in kwargs: kwargs.pop("kval")
        feature = self._pre_predict(*args, **kwargs)
        prediction = self._predict(feature)
        result = self._post_predict(prediction)
        return result

if __name__ == "__main__":
    ...


