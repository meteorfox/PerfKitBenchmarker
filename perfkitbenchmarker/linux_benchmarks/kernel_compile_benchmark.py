import datetime
import os

from perfkitbenchmarker import configs
from perfkitbenchmarker import sample

from perfkitbenchmarker.linux_packages import kernel_compile


BENCHMARK_NAME = 'kernel_compile'
BENCHMARK_CONFIG = """
kernel_compile:
  description: Compile the Linux kernel
  vm_groups:
    default:
      vm_spec: *default_single_core
      disk_spec: *default_500_gb
"""


class _Paths(object):
  def __init__(self, vm):
    self.working_dir = os.path.join(vm.GetScratchDir(), BENCHMARK_NAME)
    self.source_dir = os.path.join(self.working_dir, kernel_compile.UNTAR_DIR)


def GetConfig(user_config):
  return configs.LoadConfig(BENCHMARK_CONFIG, user_config, BENCHMARK_NAME)


def _GetVm(benchmark_spec):
  vms = benchmark_spec.vms
  if len(vms) != 1:
    raise ValueError(
        'kernel_compile benchmark requires exactly one machine, found {0}'
        .format(len(vms)))
  return vms[0]


def Prepare(benchmark_spec):
  """Install Linux kernel source code and build dependencies.
  Args:
    benchmark_spec: The benchmark specification. Contains all data that is
        required to run the benchmark.
  """
  vm = _GetVm(benchmark_spec)
  vm.Install('kernel_compile')


def Run(benchmark_spec):
  vm = _GetVm(benchmark_spec)
  paths = _Paths(vm)

  def time_command(command):
    start = datetime.datetime.now()
    vm.RemoteCommand(command)
    return (datetime.datetime.now() - start).total_seconds()

  def make(target=''):
    return time_command(
        'make -C {} -j$(egrep -c "^processor" /proc/cpuinfo) {}'
        .format(paths.source_dir, target))

  untar_time = time_command('rm -rf {dir} && '
                            'mkdir {dir} && '
                            'tar -C {dir} -xzf {tarball}'.format(
                                dir=paths.working_dir,
                                tarball=kernel_compile.KERNEL_TARBALL))

  vm.PushDataFile('kernel_compile.config',
                  '{}/.config'.format(paths.source_dir))

  cold_build_time = make()
  clean_time = make('clean')
  warm_build_time = make()

  metadata = dict(vm.GetMachineTypeDict())

  return [
      sample.Sample('Untar time', untar_time, 'seconds', metadata),
      sample.Sample('Cold build time', cold_build_time, 'seconds', metadata),
      sample.Sample('Clean time', clean_time, 'seconds', metadata),
      sample.Sample('Warm build time', warm_build_time, 'seconds', metadata),
  ]


def Cleanup(benchmark_spec):
  vm = _GetVm(benchmark_spec)
  paths = _Paths(vm)
  vm.RemoteCommand('rm -rf {}'.format(paths.working_dir))
