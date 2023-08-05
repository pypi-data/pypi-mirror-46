# torch-utils [![Build Status](https://travis-ci.com/FebruaryBreeze/torch-utils.svg?branch=master)](https://travis-ci.com/FebruaryBreeze/torch-utils) [![codecov](https://codecov.io/gh/FebruaryBreeze/torch-utils/branch/master/graph/badge.svg)](https://codecov.io/gh/FebruaryBreeze/torch-utils) [![PyPI version](https://badge.fury.io/py/torch-utils.svg)](https://pypi.org/project/torch-utils/)

Common Utils for PyTorch.

## Installation

Need Python 3.6+.

```bash
pip install torch-utils
```

## Usage

1. Accuracy

```python
import torch_utils

# ...

top_1, top_5 = torch_utils.accuracy(output=..., target=..., top_k=(1, 5))
```

2. Meter

```python
import torch_utils

loss_meter = torch_utils.AverageMeter(name='Meter', length=10)
loss_meter.update(val=...)

print(loss_meter.avg, loss_meter.val)
print(loss_meter)
#> Test 0.00 (0.00)

progress_meter = torch_utils.ProgressMeter(total_steps=100, total_epochs=10)
progress_meter.update(step=10)
assert progress_meter.step == 10
assert progress_meter.ratio == 0.1
assert progress_meter.epoch == 1
print(progress_meter)
#> Step 10/100=10.0% (1/10)
```
