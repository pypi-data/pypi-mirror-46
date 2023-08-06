
# Table of Contents

1.  [Overview](#org82be5bc)
2.  [Requirements](#org7ecf4d5)
3.  [Installation](#orgff5bee3)
4.  [Usage](#org6e66c30)
5.  [Classes](#org6a8a7d5)
    1.  [ReplayBuffer](#org60a7200)
    2.  [PrioritizedReplayBuffer](#org90ed9a8)
    3.  [NstepReplayBuffer](#org0757298)
    4.  [NstepPrioritizedReplayBuffer](#org5c0e06a)
6.  [Test Environment](#orgac8219e)

[Project Site](https://ymd_h.gitlab.io/cpprb/)


<a id="org82be5bc"></a>

# Overview

Complicated calculation (e.g. Segment Tree) are offloaded onto C++
which must be much faster than Python.

Internal C++ classes and corresponding Python wrapper classes share
memory by [implementing buffer protocol on cython](https://cython.readthedocs.io/en/latest/src/userguide/buffer.html) to avoid overhead of
copying large data.


<a id="org7ecf4d5"></a>

# Requirements

-   C++17 (at least GCC 7.2)
-   Python 3
-   Cython (>= 0.29)

We use [Cython](https://cython.org/) to write C++ extension for Python, so that you need
Cython to build our packages on your computer.

We observed a build failure with Cython 0.28.5 ([#20](https://gitlab.com/ymd_h/cpprb/issues/20) Japanese).

Cython can be installed by `pip`.

    pip install cython

We uses many C++17 features, such as `if constexpr`, structured
bindings, etc., and we highly recommend to use recent gcc, which we
use to build and test.


<a id="orgff5bee3"></a>

# Installation

    git clone https://gitlab.com/ymd_h/cpprb.git cpprb
    cd cpprb
    python setup.py build
    python setup.py install

Depending on your environment, you might need to set `CC` and/or `CXX`
variables like `CXX=g++ python setup.py build`.

You might need `sudo` for installation.


<a id="org6e66c30"></a>

# Usage

A simple example is following;

    from cpprb import ReplayBuffer
    
    buffer_size = 256
    obs_dim = 3
    act_dim = 1
    rb = ReplayBuffer(buffer_size,obs_dim,act_dim)
    
    obs = np.ones(shape=(obs_dim))
    act = np.ones(shape=(act_dim))
    rew = 0
    next_obs = np.ones(shape=(obs_dim))
    done = 0
    
    for i in range(500):
        rb.add(obs,act,rew,next_obs,done)
    
    
    batch_size = 32
    sample = rb.sample(batch_size)
    # sample is a dictionary whose keys are 'obs', 'act', 'rew', 'next_obs', and 'done'


<a id="org6a8a7d5"></a>

# Classes

`ReplayBuffer`, `PrioritizedReplayBuffer`, `NstepReplayBuffer`,
and `NstepPrioritizedReplayBuffer` are supported.

The other classes (including C++ classes) are considered as internal
classes, whose interfaces can change frequently.


<a id="org60a7200"></a>

## ReplayBuffer

`ReplayBuffer` is a basic replay buffer, where we pick up each time
point randomly. (Duplicated pick up is allowed.)


<a id="org90ed9a8"></a>

## PrioritizedReplayBuffer

`PrioritizedReplayBuffer` is a prioritized replay buffer, where you
can set importance (e.g. TD error) to each time point by calling
`PrioritizedReplayBuffer.update_priorities(self,ps)` or
`PrioritizedReplayBuffer.add(self,obs,act,rew,next_obs,done,p)`.
The constructor also take `alpha` parameter, whose default value is `0.6`.
For sampling, you need to pass `beata` argument as well as `batch_size`.


<a id="org0757298"></a>

## NstepReplayBuffer

`NstepReplayBuffer` is a N-step reward version of replay buffer. Its
usage is same as `ReplayBuffer`, except whose return value has
`discounts` key. The step size and discount rate are passed to its
constructor as `n_step` (default `4`) and `discount` (default 0.99),
respectively.


<a id="org5c0e06a"></a>

## NstepPrioritizedReplayBuffer

`NstepPrioritizedReplayBuffer` is a N-step reward version of
prioritized replay buffer.  The usage is a mixture of
`PrioritizedReplayBuffer` and `NstepReplayBuffer`.


<a id="orgac8219e"></a>

# Test Environment

-   GCC 8.2.0
-   Python 3.7.2
-   Cython 0.29.3

