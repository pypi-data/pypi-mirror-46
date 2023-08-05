import torch
import unittest
import qtorch
from qtorch.quant import block_quantize

def block_share_first(data, bits, ebit=8):
    """
    Sample implementation of sharing first dimension nearest rounding block floating point.
    """
    max_entry = torch.max(torch.abs(data.view(data.size(0), -1)), 1)[0]
    max_exponent = torch.floor(torch.log2(max_entry))
    # max_exponent = torch.clamp(max_exponent, -2**(ebit-1), 2**(ebit-1)-1)
    max_exponent = max_exponent.view([data.size(0)]+[1 for _ in range(data.dim()-1)])
    i = data * 2**(-max_exponent+(bits-2))
    i.round_()
    i.clamp_(-2**(bits-1), 2**(bits-1)-1)
    temp = i * 2**(max_exponent-(bits-2))
    return temp

class TestPython(unittest.TestCase):
    """
    QPyTorch Implementation should perform the same with PyTorch implementation
    """
    def test_block_sharing(self):
        pass
        # target = torch.ones(1)*0.99
        # for wl in [5]:
        #     python_result = block_share_first(target, wl)
        #     qtorch_result = block_quantize(target, wl=wl, dim=0, rounding="nearest")
        #     eq_mask = python_result.eq(qtorch_result)
        #     # print(python_result.masked_select(1-eq_mask))
        #     # print(qtorch_result.masked_select(1-eq_mask))
        #     mse = torch.sum(diff**2)
        #     # print(mse)

if __name__ == "__main__":
    unittest.main()
