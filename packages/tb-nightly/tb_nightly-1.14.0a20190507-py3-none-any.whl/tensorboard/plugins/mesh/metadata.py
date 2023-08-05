# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
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
# ==============================================================================
"""Internal information about the mesh plugin."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorboard.compat.proto import summary_pb2
from tensorboard.plugins.mesh import plugin_data_pb2


PLUGIN_NAME = 'mesh'

# The most recent value for the `version` field of the
# `MeshPluginData` proto.
_PROTO_VERSION = 0


def get_current_version():
  """Returns current verions of the proto."""
  return _PROTO_VERSION


def get_instance_name(name, content_type):
  """Returns a unique instance name for a given summary related to the mesh."""
  return '%s_%s' % (
      name,
      plugin_data_pb2.MeshPluginData.ContentType.Name(content_type))


def create_summary_metadata(name,
                            display_name,
                            content_type,
                            shape,
                            description=None,
                            json_config=None):
  """Creates summary metadata which defined at MeshPluginData proto.

  Arguments:
    name: Original merged (summaries of different types) summary name.
    display_name: The display name used in TensorBoard.
    content_type: Value from MeshPluginData.ContentType enum describing data.
    shape: list of dimensions sizes of the tensor.
    description: The description to show in TensorBoard.
    json_config: A string, JSON-serialized dictionary of ThreeJS classes
      configuration.

  Returns:
    A `summary_pb2.SummaryMetadata` protobuf object.
  """
  # Shape should be at least BxNx3 where B represents the batch dimensions
  # and N - the number of points, each with x,y,z coordinates.
  if len(shape) != 3:
    raise ValueError('Tensor shape should be of shape BxNx3, but got %s.' % str(shape))
  mesh_plugin_data = plugin_data_pb2.MeshPluginData(
      version=get_current_version(),
      name=name,
      content_type=content_type,
      shape=shape,
      json_config=json_config)
  content = mesh_plugin_data.SerializeToString()
  return summary_pb2.SummaryMetadata(
      display_name=display_name,  # Will not be used in TensorBoard UI.
      summary_description=description,
      plugin_data=summary_pb2.SummaryMetadata.PluginData(
          plugin_name=PLUGIN_NAME,
          content=content))


def parse_plugin_metadata(content):
  """Parse summary metadata to a Python object.

  Arguments:
    content: The `content` field of a `SummaryMetadata` proto
      corresponding to the mesh plugin.

  Returns:
    A `MeshPluginData` protobuf object.
  Raises: Error if the version of the plugin is not supported.
  """
  if not isinstance(content, bytes):
    raise TypeError('Content type must be bytes.')
  result = plugin_data_pb2.MeshPluginData.FromString(content)
  if result.version == get_current_version():
    return result
  raise ValueError('Unknown metadata version: %s. The latest version known to '
                   'this build of TensorBoard is %s; perhaps a newer build is '
                   'available?' % (result.version, get_current_version()))
