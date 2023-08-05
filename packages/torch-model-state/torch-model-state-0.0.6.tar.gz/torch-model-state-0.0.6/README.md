# torch-model-state [![Build Status](https://travis-ci.com/FebruaryBreeze/torch-model-state.svg?branch=master)](https://travis-ci.com/FebruaryBreeze/torch-model-state) [![codecov](https://codecov.io/gh/FebruaryBreeze/torch-model-state/branch/master/graph/badge.svg)](https://codecov.io/gh/FebruaryBreeze/torch-model-state) [![PyPI version](https://badge.fury.io/py/torch-model-state.svg)](https://pypi.org/project/torch-model-state/)

PyTorch Model State Save & Load.

## Installation

Need Python 3.6+.

```bash
pip install torch-model-state
```

## Usage

Python:

```python
import box
import torch_model_state
from torch.optim import SGD

config = {
  'type': 'MobileNetV2'  # need install torch-basic-models
}
model = box.factory(config=config, tag='model')
optimizer = SGD(model.parameters(), lr=0.1)

state = torch_model_state.to_state(model=model, config=config, optimizers=[optimizer])
torch_model_state.save_state_file(state=state, file_path='checkpoint.sf')

state = torch_model_state.load_state_file(file_path='checkpoint.sf', device='cpu')
torch_model_state.from_state(state, model, [optimizer], device='cpu')
```

Load from State File (.sf) directly:

```python
import torch_model_state

model = torch_model_state.load_model_from_state(file_path='checkpoint.sf', device='cpu')
```

CLI:

```bash
# show help
torch-model-state -h
#> usage: torch-model-state [-h] [--load_model] [--extra_import EXTRA_IMPORT]
#>                          [--device DEVICE]
#>                          state_file
#>
#> Viewer of PyTorch State File [.sf]
#>
#> positional arguments:
#>   state_file            path of PyTorch state file
#>
#> optional arguments:
#>   -h, --help            show this help message and exit
#>   --load_model          load model and show
#>   --extra_import EXTRA_IMPORT
#>                         import extra models
#>   --device DEVICE       load device, cpu in default

# view basic info of state file
torch-model-state checkpoint.sf
#> {
#>   "config": {
#>     "type": "MobileNetV2"
#>   },
#>   "info": null,
#>   "timestamp": "2019-04-27 22:42:55.345000"
#> }

# view & load Model
torch-model-state checkpoint.sf --load_model
#> {
#>   "config": {
#>     "type": "MobileNetV2"
#>   },
#>   "info": null,
#>   "timestamp": "2019-04-27 22:42:55.345000"
#> }
#> MobileNetV2(
#>   (blocks): Sequential(
#>     (0): Sequential(
#>       (0): Conv2d(3, 32, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
#>       (1): BatchNorm2d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
#>       (2): InplaceReLU6(inplace)
#>     )
#>   ...

# export to ONNX
torch-model-state checkpoint.sf --export_onnx checkpoint.onnx
```
