import torch
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

ckpt_in = torch.load(infile, map_location='cpu')

ckpt_out = dict()

print(ckpt_in.keys())
minimal_set = ['device', 'model_name', 'model_kwargs', 'model', 'config']

for key in minimal_set:
    ckpt_out[key] = ckpt_in[key]

torch.save(ckpt_out, outfile)
print(ckpt_out.keys())