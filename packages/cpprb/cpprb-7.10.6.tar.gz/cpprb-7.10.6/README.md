
# Table of Contents

1.  [Overview](#org24b3de8)
2.  [Requirements](#orgfb4f198)
3.  [Installation](#orgb441d55)
4.  [Usage](#orgc5f3852)
5.  [Classes](#org6af13a8)
    1.  [ReplayBuffer](#org4bd76ff)
    2.  [PrioritizedReplayBuffer](#orgb7da8b6)
    3.  [NstepReplayBuffer](#orgad80bec)
    4.  [NstepPrioritizedReplayBuffer](#orgc9ba088)
6.  [Test Environment](#orga2651aa)

[Project Site](https://ymd_h.gitlab.io/cpprb/)


<a id="org24b3de8"></a>

# Overview

Complicated calculation (e.g. Segment Tree) are offloaded onto C++
which must be much faster than Python.

Internal C++ classes and corresponding Python wrapper classes share
memory by [implementing buffer protocol on cython](https://cython.readthedocs.io/en/latest/src/userguide/buffer.html) to avoid overhead of
copying large data.


<a id="orgfb4f198"></a>

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


<a id="orgb441d55"></a>

# Installation

    git clone https://gitlab.com/ymd_h/cpprb.git cpprb
    cd cpprb
    python setup.py build
    python setup.py install

Depending on your environment, you might need to set `CC` and/or `CXX`
variables like `CXX=g++ python setup.py build`.

You might need `sudo` for installation.


<a id="orgc5f3852"></a>

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


<a id="org6af13a8"></a>

# Classes

`ReplayBuffer`, `PrioritizedReplayBuffer`, `NstepReplayBuffer`,
and `NstepPrioritizedReplayBuffer` are supported.

The other classes (including C++ classes) are considered as internal
classes, whose interfaces can change frequently.


<a id="org4bd76ff"></a>

## ReplayBuffer

`ReplayBuffer` is a basic replay buffer, where we pick up each time
point randomly. (Duplicated pick up is allowed.)


<a id="orgb7da8b6"></a>

## PrioritizedReplayBuffer

`PrioritizedReplayBuffer` is a prioritized replay buffer, where you
can set importance (e.g. TD error) to each time point by calling
`PrioritizedReplayBuffer.update_priorities(self,ps)` or
`PrioritizedReplayBuffer.add(self,obs,act,rew,next_obs,done,p)`.
The constructor also take `alpha` parameter, whose default value is `0.6`.
For sampling, you need to pass `beata` argument as well as `batch_size`.


<a id="orgad80bec"></a>

## NstepReplayBuffer

`NstepReplayBuffer` is a N-step reward version of replay buffer. Its
usage is same as `ReplayBuffer`, except whose return value has
`discounts` key. The step size and discount rate are passed to its
constructor as `n_step` (default `4`) and `discount` (default 0.99),
respectively.


<a id="orgc9ba088"></a>

## NstepPrioritizedReplayBuffer

`NstepPrioritizedReplayBuffer` is a N-step reward version of
prioritized replay buffer.  The usage is a mixture of
`PrioritizedReplayBuffer` and `NstepReplayBuffer`.


<a id="orga2651aa"></a>

# Test Environment

-   GCC 8.2.0
-   Python 3.7.2
-   Cython 0.29.3

