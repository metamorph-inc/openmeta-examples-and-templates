# optimizeContainer.py

# from __future__ import print_function
# import math

def optimizeContainer(L1, W1, H1, L2, W2, H2):
    Length = L1 + L2
    Width = W1 + W2
    Height = H1 + H2
    Volume = Length * Width * Height
    return [Length, Width, Height, Volume]