# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
r"""Vision models export utility function for serving/inference."""

import os
from typing import Optional, List

from absl import logging
import tensorflow as tf

from official.core import config_definitions as cfg
from official.core import export_base
from official.core import train_utils
from official.vision.beta import configs
from official.vision.beta.serving import detection
from official.vision.beta.serving import image_classification
from official.vision.beta.serving import semantic_segmentation
from official.vision.beta.serving import video_classification


def export_inference_graph(
    input_type: str,
    batch_size: Optional[int],
    input_image_size: List[int],
    params: cfg.ExperimentConfig,
    checkpoint_path: str,
    export_dir: str,
    num_channels: Optional[int] = 3,
    export_module: Optional[export_base.ExportModule] = None,
    export_checkpoint_subdir: Optional[str] = None,
    export_saved_model_subdir: Optional[str] = None,
    save_options: Optional[tf.saved_model.SaveOptions] = None,
    log_model_flops_and_params: bool = False):
  """Exports inference graph for the model specified in the exp config.

  Saved model is stored at export_dir/saved_model, checkpoint is saved
  at export_dir/checkpoint, and params is saved at export_dir/params.yaml.

  Args:
    input_type: One of `image_tensor`, `image_bytes`, `tf_example` or `tflite`.
    batch_size: 'int', or None.
    input_image_size: List or Tuple of height and width.
    params: Experiment params.
    checkpoint_path: Trained checkpoint path or directory.
    export_dir: Export directory path.
    num_channels: The number of input image channels.
    export_module: Optional export module to be used instead of using params
      to create one. If None, the params will be used to create an export
      module.
    export_checkpoint_subdir: Optional subdirectory under export_dir
      to store checkpoint.
    export_saved_model_subdir: Optional subdirectory under export_dir
      to store saved model.
    save_options: `SaveOptions` for `tf.saved_model.save`.
    log_model_flops_and_params: If True, writes model FLOPs to model_flops.txt
      and model parameters to model_params.txt.
  """

  if export_checkpoint_subdir:
    output_checkpoint_directory = os.path.join(
        export_dir, export_checkpoint_subdir)
  else:
    output_checkpoint_directory = None

  if export_saved_model_subdir:
    output_saved_model_directory = os.path.join(
        export_dir, export_saved_model_subdir)
  else:
    output_saved_model_directory = export_dir

  # TODO(arashwan): Offers a direct path to use ExportModule with Task objects.
  if not export_module:
    if isinstance(params.task,
                  configs.image_classification.ImageClassificationTask):
      export_module = image_classification.ClassificationModule(
          params=params,
          batch_size=batch_size,
          input_image_size=input_image_size,
          input_type=input_type,
          num_channels=num_channels)
    elif isinstance(params.task, configs.retinanet.RetinaNetTask) or isinstance(
        params.task, configs.maskrcnn.MaskRCNNTask):
      export_module = detection.DetectionModule(
          params=params,
          batch_size=batch_size,
          input_image_size=input_image_size,
          input_type=input_type,
          num_channels=num_channels)
    elif isinstance(params.task,
                    configs.semantic_segmentation.SemanticSegmentationTask):
      export_module = semantic_segmentation.SegmentationModule(
          params=params,
          batch_size=batch_size,
          input_image_size=input_image_size,
          input_type=input_type,
          num_channels=num_channels)
    elif isinstance(params.task,
                    configs.video_classification.VideoClassificationTask):
      export_module = video_classification.VideoClassificationModule(
          params=params,
          batch_size=batch_size,
          input_image_size=input_image_size,
          input_type=input_type,
          num_channels=num_channels)
    else:
      raise ValueError('Export module not implemented for {} task.'.format(
          type(params.task)))

  export_base.export(
      export_module,
      function_keys=[input_type],
      export_savedmodel_dir=output_saved_model_directory,
      checkpoint_path=checkpoint_path,
      timestamped=False,
      save_options=save_options)

  if output_checkpoint_directory:
    ckpt = tf.train.Checkpoint(model=export_module.model)
    ckpt.save(os.path.join(output_checkpoint_directory, 'ckpt'))
  train_utils.serialize_config(params, export_dir)

  if log_model_flops_and_params:
    inputs_kwargs = None
    if isinstance(
        params.task,
        (configs.retinanet.RetinaNetTask, configs.maskrcnn.MaskRCNNTask)):
      # We need to create inputs_kwargs argument to specify the input shapes for
      # subclass model that overrides model.call to take multiple inputs,
      # e.g., RetinaNet model.
      inputs_kwargs = {
          'images':
              tf.TensorSpec([1] + input_image_size + [num_channels],
                            tf.float32),
          'image_shape':
              tf.TensorSpec([1, 2], tf.float32)
      }
      dummy_inputs = {
          k: tf.ones(v.shape.as_list(), tf.float32)
          for k, v in inputs_kwargs.items()
      }
      # Must do forward pass to build the model.
      export_module.model(**dummy_inputs)
    else:
      logging.info(
          'Logging model flops and params not implemented for %s task.',
          type(params.task))
      return
    train_utils.try_count_flops(export_module.model, inputs_kwargs,
                                os.path.join(export_dir, 'model_flops.txt'))
    train_utils.write_model_params(export_module.model,
                                   os.path.join(export_dir, 'model_params.txt'))
