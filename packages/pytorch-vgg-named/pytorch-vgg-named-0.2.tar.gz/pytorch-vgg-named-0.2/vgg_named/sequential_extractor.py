import pprint
import warnings
from collections import OrderedDict
from itertools import islice
import operator

from torch._six import container_abcs
import torch
from torch.nn import Sequential

class SequentialExtractor(Sequential):
    r"""A subclass of torch.nn.Sequential.
    Modules will be added to it in the order they are passed in the constructor.
    Alternatively, an ordered dict of modules can also be passed in.

    You can pass a target key to forward(), and the modules will only be
    executed up to that point, and the target returned.
    You can also pass a list/tuple of targets, and the modules will be executed
    until all of the targets have been computed, and they will be returned as a
    list.
    If the SequentialExtractor is constructed with an "*args" list, you can use
    int or List[int] to query it, otherwise use the keys of the OrderedDict
    used for construction.

    NOTE: this only works for flat structures. So nested sequentials as used
          in torchvision.models (features/classifier blocks) are not supported.

    To make it easier to understand, here is a small example::

        # Example of using SequentialExtractor
        model = nn.SequentialExtractor(
                  nn.Conv2d(1,20,5),
                  nn.ReLU(),
                  nn.Conv2d(20,64,5),
                  nn.ReLU()
                )

        # compute only the second conv feature
        c2 = model(x_input, 2)

        # compute the two relu features
        r1, r2 = model(x_input, [1, 3])

        # compute only the first relu.
        # note that this returns a list with one element.
        r1, r2 = model(x_input, [1])

        # default behaviour: like for torch.nn.Sequential
        r2 = model(x_input)

        # Example of using SequentialExtractor with OrderedDict
        model = nn.SequentialExtractor(OrderedDict([
                  ('conv1', nn.Conv2d(1,20,5)),
                  ('relu1', nn.ReLU()),
                  ('conv2', nn.Conv2d(20,64,5)),
                  ('relu2', nn.ReLU())
                ]))

        # compute only the second conv feature
        c2 = model(x_input, 'conv2')

        # compute the two relu features
        r1, r2 = model(x_input, ['relu1', 'relu2'])

        # compute only the first relu.
        # note that this returns a list with one element.
        r1, r2 = model(x_input, ['relu1'])
    """

    def forward(self, input, targets=None):
        # by default, just run the whole thing
        if targets is None:
          for module in self._modules.values():
              input = module(input)
          return input

        if isinstance(targets, int) or isinstance(targets, str):
          targets = str(targets)
          if targets == 'input':
            return input
          out = input
          assert targets in self._modules.keys(), f'"{targets}" is not a valid target'
          for n, m in self._modules.items():
            out = m(out)
            if n == targets:
              return out
        
        for t in targets:
          assert t in self._modules.keys(), f'"{t}" is not a valid target'
        targets = [str(t) for t in targets]
        
        results = dict()
        out = input
        # special case: input is always a valid key
        if 'input' in targets:
          results['input'] = input
        for n, m in self._modules.items():
          out = m(out)
          if n in targets:
            results[n] = out
          if len(results) == len(set(targets)):
            break

        results = [results[t] for t in targets]
        return results

    def prune(self, targets=None):
        """
        This removes all children that are not needed to compute the targets.
        Note that this is not reversible. Also not that it has the same 
        limitations as forward() in that it only handles shallow sequentials.
        """
        # by default, just run the whole thing
        if targets is None:
          return

        unused = set(self._modules.keys())

        if isinstance(targets, int) or isinstance(targets, str):
          targets = str(targets)
          if targets == 'input':
            unused -= {'input'}
          else:
            assert targets in self._modules.keys(), f'"{targets}" is not a valid target'
            for n, m in self._modules.items():
              unused -= {n}
              if n == targets:
                break
          for n in unused:
            del self._modules[n]
          return
        
        targets = [str(t) for t in targets]
        for t in targets:
          assert t in self._modules.keys(), f'"{t}" is not a valid target'
        
        # special case: input is always a valid key
        outputs = set()
        if 'input' in targets:
          unused -= {'input'}
        for n, m in self._modules.items():
          unused -= {n}
          if n in targets:
            outputs.add(n)
          if len(outputs) == len(set(targets)):
            break
        print('removing these modules:')
        pprint.pprint(unused)
        for n in unused:
          del self._modules[n]

