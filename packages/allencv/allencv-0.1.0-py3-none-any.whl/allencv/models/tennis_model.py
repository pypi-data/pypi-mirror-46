import logging
from overrides import overrides
from typing import Dict, List

import torch
import torch.nn as nn
import torch.nn.functional as F

from allennlp.models.model import Model
from allennlp.nn import InitializerApplicator
from allennlp.training.metrics import CategoricalAccuracy
from allennlp.modules import FeedForward
from allennlp.training.metrics import Average

from allencv.common import util
from allencv.models.object_detection.region_proposal_network import RPN
from allencv.models.semantic_segmentation import SemanticSegmentationModel
from allencv.modules.image_encoders import ImageEncoder, ResnetEncoder
from allencv.modules.image_decoders import ImageDecoder
from allencv.modules.im2vec_encoders.flatten_encoder import FlattenEncoder
from allencv.modules.im2im_encoders.feedforward_encoder import FeedforwardEncoder, StdConv

from maskrcnn_benchmark.structures.boxlist_ops import *
from maskrcnn_benchmark.modeling.rpn.utils import concat_box_prediction_layers

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

@Model.register("tennis")
class TennisModel(Model):
    """
    """
    def __init__(self,
                 rpn: RPN,
                 initializer: InitializerApplicator = InitializerApplicator()) -> None:
        super(TennisModel, self).__init__(None)
        self._feedforward = nn.Sequential(FeedforwardEncoder(15, 4, [8, 16, 16, 16], 'relu'),
                                          FlattenEncoder(16, 8, 8))
        self._rpn = rpn
        loaded = torch.load("/home/sethah/ssd/allencv/models/tennis_rpn6/best.th")
        self._rpn.load_state_dict(loaded)
        self._rpn.anchor_generator.straddle_thresh = 200
        for p in self._rpn.parameters():
            p.requires_grad = False
        self._rpn.decoder.fpn_post_nms_top_n = 30
        self._rpn.decoder.nms_thresh = 0.3
        self._rpn.loss_evaluator.discard_cases = []
        self._predict = FeedForward(1024 + 4, 3, [256, 128, 64], nn.ReLU())
        self._head = nn.Linear(64, 1)
        self._accuracy = CategoricalAccuracy()
        self._loss = nn.BCEWithLogitsLoss()
        initializer(self)

    def forward(self,
                image: torch.Tensor,  # (batch_size, c, h, w)
                image_sizes: torch.Tensor,  # (batch_size, 2)
                boxes: torch.Tensor = None,  # (batch_size, max_boxes_in_batch, 4)
                box_classes: torch.Tensor = None
                ) -> Dict[str, torch.Tensor]:

        rpn_out = self._rpn.forward(image, image_sizes, boxes, box_classes)
        rpn_out = self._rpn.decode(rpn_out)
        proposals = rpn_out['proposals']
        proposal_boxlist = self._rpn._padded_tensor_to_box_list(proposals, image_sizes)
        for bl in proposal_boxlist:
            bl.add_field("visibility", torch.ones(len(bl)).byte())

        bs = image.shape[0]
        peopleness = [rpn_out['objectness'][0]]
        for objectness_map in rpn_out['objectness'][1:]:
            peopleness.append(F.interpolate(objectness_map, size=rpn_out['objectness'][0].shape[-2:]))
        features = self._feedforward(torch.cat(peopleness, dim=1))



        # proposal_anchors_ = [cat_boxlist(anchors_per_image) for anchors_per_image in proposal_boxlist]
        box_list: List[BoxList] = self._rpn._padded_tensor_to_box_list(boxes, image_sizes)
        _labels: List[torch.Tensor] = None
        _labels, _regression_targets = self._rpn.loss_evaluator.prepare_targets(proposal_boxlist, box_list)
        # sampled_pos_inds, sampled_neg_inds = self.fg_bg_sampler(_labels)
        # sampled_pos_inds = torch.nonzero(torch.cat(sampled_pos_inds, dim=0)).squeeze(1)
        # sampled_neg_inds = torch.nonzero(torch.cat(sampled_neg_inds, dim=0)).squeeze(1)
        #
        # sampled_inds = torch.cat([sampled_pos_inds, sampled_neg_inds], dim=0)
        # objectness, box_regression = \
        #     concat_box_prediction_layers(rpn_out['objectness'], rpn_out['rpn_box_regression'])

        # objectness = objectness.squeeze()

        labels = torch.cat(_labels, dim=0)
        # logger.warning(f"Nonzero labels: {(labels > 0).sum().item()}")
        combined = []
        for i, image_proposal_anchors in enumerate(proposal_boxlist):
            combined.append(torch.cat([image_proposal_anchors.bbox, features[i].expand(image_proposal_anchors.bbox.shape[0], features.shape[1])], dim=1))

        final_features = torch.cat(combined, dim=0)
        assert final_features.shape[0] == labels.shape[0]
        out = rpn_out
        logits = self._head(self._predict.forward(final_features)).view(-1)
        assert logits.shape[0] == labels.shape[0]
        out['loss'] = self._loss(logits, labels)
        self._accuracy(torch.stack([1-logits, logits], dim=1), labels)
        logger.info(f"{logits.max().item(), logits.min().item(), labels.sum().item()}")
        # masks = [lbl[:49152].view(128, 128, 3)[:, :, 2] != 0 for lbl in _labels]
        # peopleness = torch.cat([peopleness.view(bs, 1, 128, 128), torch.zeros(bs, 1, 128, 128, device=peopleness.device),
        #                           torch.zeros(bs, 1, 128, 128, device=peopleness.device)], dim=1)
        # segmentation_out = self._segmenter.forward(peopleness, torch.stack(masks, dim=0).float())
        return out


    @overrides
    def decode(self, output_dict: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        output_dict['predicted_mask'] = output_dict['probs'].argmax(dim=1)
        return output_dict

    def get_metrics(self, reset: bool = False) -> Dict[str, float]:
        metrics = {'accuracy': self._accuracy.get_metric(reset)}
        return metrics

@Model.register("tennis2")
class TennisModel2(Model):
    """
    """
    def __init__(self,
                 rpn: RPN,
                 initializer: InitializerApplicator = InitializerApplicator()) -> None:
        super(TennisModel2, self).__init__(None)
        self._feedforward = nn.Sequential(FeedforwardEncoder(15, 4, [8, 16, 16, 16], 'relu'),
                                          FlattenEncoder(16, 8, 8))
        self._rpn = rpn
        loaded = torch.load("/home/sethah/ssd/allencv/models/tennis_rpn6/best.th")
        self._rpn.load_state_dict(loaded)
        self._rpn.anchor_generator.straddle_thresh = 200
        for p in self._rpn.parameters():
            p.requires_grad = False
        self._rpn.decoder.fpn_post_nms_top_n = 1000
        self._rpn.decoder.nms_thresh = 0.7
        self._rpn.loss_evaluator.discard_cases = []
        # self._predict = FeedForward(1024 + 4, 3, [256, 128, 64], nn.ReLU())
        # self._head = nn.Linear(64, 3)
        self._accuracy = CategoricalAccuracy()
        kernel_size = 11
        dilation = 2
        padding = 10
        self._feedforward1 = nn.Sequential(StdConv(3, 8, kernel_size, padding=padding, dilation=dilation),
                                           StdConv(8, 16, kernel_size, padding=padding, dilation=dilation),
                                           StdConv(16, 16, kernel_size, padding=padding, dilation=dilation),
                                           nn.Conv2d(16, 3, 3, padding=1))
        self._feedforward2 = nn.Sequential(StdConv(3, 8, kernel_size, padding=padding, dilation=dilation),
                                           StdConv(8, 16, kernel_size, padding=padding, dilation=dilation),
                                           StdConv(16, 16, kernel_size, padding=padding, dilation=dilation),
                                           nn.Conv2d(16, 3, 3, padding=1))
        self._feedforwards = [self._feedforward1, self._feedforward2]
        self._loss_meters = {'rpn_cls_loss': Average(), 'rpn_reg_loss': Average()}
        initializer(self)

    def forward(self,
                image: torch.Tensor,  # (batch_size, c, h, w)
                image_sizes: torch.Tensor,  # (batch_size, 2)
                boxes: torch.Tensor = None,  # (batch_size, max_boxes_in_batch, 4)
                box_classes: torch.Tensor = None
                ) -> Dict[str, torch.Tensor]:

        rpn_out = self._rpn.forward(image, image_sizes, boxes, box_classes)
        # rpn_out = self._rpn.decode(rpn_out)
        # proposals = rpn_out['proposals']
        # proposal_boxlist = self._rpn._padded_tensor_to_box_list(proposals, image_sizes)
        # for bl in proposal_boxlist:
        #     bl.add_field("visibility", torch.ones(len(bl)).byte())

        bs = image.shape[0]
        # peopleness = [rpn_out['objectness'][0]]
        # for objectness_map in rpn_out['objectness'][1:2]:
        #     peopleness.append(F.interpolate(objectness_map, size=rpn_out['objectness'][0].shape[-2:])[:, -1:, :, :])
        # [(b, 3, 128, 128), (b, 3, 64, 64)] -> [(b, 3, 128, 128), (b, 3, 128, 128)]
        peopleness = rpn_out['objectness'][:2]
        objectness = [ff(f) for f, ff in zip(peopleness, self._feedforwards)]



        # anchors_ = [cat_boxlist(anchors_per_image) for anchors_per_image in rpn_out['anchors']]
        # box_list: List[BoxList] = self._rpn._padded_tensor_to_box_list(boxes, image_sizes)
        # _labels: List[torch.Tensor] = None
        # _labels, _regression_targets = self._rpn.loss_evaluator.prepare_targets(anchors_, box_list)
        # gt_list = BoxList(box.detach(), tuple(im_size))
        # _labels, _regression_targets = model.loss_evaluator.prepare_targets(anchors_, [gt_list])
        # label_maps1 = []
        # label_maps2 = []
        # for lbls_per_image in _labels:
        #     label_maps1.append(lbls_per_image[128*128*2:128*128*3])
        #     label_maps2.append(lbls_per_image[128*128*3 + 64*64*2:128*128*3 + 64*64*3])
        # # (2, 16384)
        # label_maps1 = torch.stack(label_maps1, dim=0)
        # # (2, 4096)
        # label_maps2 = torch.stack(label_maps2, dim=0)
        # labels = torch.cat([label_maps1, label_maps2], dim=1)
        # # (b, 2,
        # logits = torch.cat([x.permute(0, 2, 3, 1).contiguous().view(-1, self.num_classes) for x in logits])
        # flattened_logits = logits.permute(0, 2, 3, 1).contiguous().view(-1, self.num_classes)
        # anchors: List[List[BoxList]] = self.anchor_generator(image_list, features)
        rpn_box_regression = rpn_out['rpn_box_regression'][:2]
        anchors = [a[:2] for a in rpn_out['anchors']]
        out = {'objectness': objectness,
               'rpn_box_regression': rpn_box_regression,
               'anchors': rpn_out['anchors']}
        if boxes is not None:
            box_list: List[BoxList] = self._rpn._padded_tensor_to_box_list(boxes, image_sizes)
            loss_objectness, loss_rpn_box_reg = self._rpn.loss_evaluator(
                anchors, objectness, rpn_box_regression, box_list
            )
            out["loss_objectness"] = loss_objectness
            out["loss_rpn_box_reg"] = loss_rpn_box_reg
            self._loss_meters['rpn_cls_loss'](loss_objectness.item())
            self._loss_meters['rpn_reg_loss'](loss_rpn_box_reg.item())
            out["loss"] = loss_objectness + 10 * loss_rpn_box_reg
        return out

    @overrides
    def decode(self, output_dict: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        output_dict['predicted_mask'] = output_dict['probs'].argmax(dim=1)
        return output_dict

    def get_metrics(self, reset: bool = False) -> Dict[str, float]:
        metrics = {k: v.get_metric(reset) for k, v in self._loss_meters.items()}
        return metrics
