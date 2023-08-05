# METAS UncLib

To use METAS UncLib, simply do:

    >>> from metas_unclib import *
    >>> use_linprop()
    
    >>> a = ufloat(3.0, 0.3, desc='a')
    >>> b = ufloat(4.0, 0.4, desc='b')
    
    >>> c = umath.sqrt(a**2 + b**2)
    >>> print(c)
    5.0 ± 0.3671511950137164


# Requirements

- numpy
- pythonnet

# Optional Requirements

- scipy
- matplotlib
- jupyter

# Linux

The `LD_LIBRARY_PATH` environment variable has to be set to:

    export LD_LIBRARY_PATH=~/.local/lib/python3.6/site-packages/metas_unclib/mkl_custom/linux/intel64

# macOS

The `DYLD_LIBRARY_PATH` environment variable has to be set to:

    export DYLD_LIBRARY_PATH=~/.local/lib/python3.6/site-packages/metas_unclib/mkl_custom/macos/intel64
