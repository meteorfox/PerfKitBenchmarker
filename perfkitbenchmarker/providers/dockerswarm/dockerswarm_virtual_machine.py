# Copyright 2015 PerfKitBenchmarker Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from perfkitbenchmarker import flags
from perfkitbenchmarker import linux_virtual_machine
from perfkitbenchmarker import virtual_machine
from perfkitbenchmarker import vm_util

FLAGS = flags.FLAGS

UBUNTU_IMAGE = 'ubuntu-upstart'


class DockerSwarmVirtualMachine(virtual_machine.BaseVirtualMachine):
  """ Object representing a Docker Swarm Container. """
  CLOUD = 'DockerSwarm'

  def __init__(self, vm_spec):
    """Initialize a Docker Swarm virtual machine.
    Args:
      vm_spec: virtual_machine.BaseVirtualMachineSpec object of the vm.
    """
    super(DockerSwarmVirtualMachine, self).__init__(vm_spec)
    self.image = self.image or UBUNTU_IMAGE

  def _CreateDependencies(self):
    pass

  def _Create(self):
    pass

  def _Exists(self):
    return True

  @vm_util.Retry()
  def _PostCreate(self):
    pass

  def _Delete(self):
    pass

  def _DeleteDependencies(self):
    pass


class DebianBasedDockerSwarmVirtualMachine(DockerSwarmVirtualMachine,
                                           linux_virtual_machine.DebianMixin):
  DEFAULT_IMAGE = UBUNTU_IMAGE
