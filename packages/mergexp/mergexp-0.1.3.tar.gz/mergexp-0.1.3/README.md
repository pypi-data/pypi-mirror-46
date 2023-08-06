# MyPy Merge Experimentation Library

A library for developing Merge experiments in Python

## Hello world

```python
import mergexp as mx
from mx.unit import gb, ms, mbps
from mx.machine import cores, memory
from mx.net import capacity, latency

# define a topology
topo = mx.Topology('hello mx')

# make some devices
a = topo.device('a', cores > 2, memory <= gb(4))
b = topo.device('b', cores < 6, memory >= gb(4))

# connect devices
topo.connect([a, b], capacity < mbps(100), latency > ms(5))
```


## Hello mobile

```python
import mergexp as mx
from mx.stochastic import normal, poisson
from mx.unit import gb, ms, mbps
from mx.machine import cores, memory, arch, armv7, x86_64
from mx.net import capacity, latency
from mx.mobile import collision, migration

# define a topology
topo = mx.Topology('hello mobile')

# define a few device types
def mobile(name):
    return topo.device(
        name, 
        cores == 1, 
        memory < gb(2), 
        arch == armv7,
    )

def server(name):
    return topo.device(
        name,
        cores >= 8,
        memory >= gb(8),
        arch == x86_64,
    )

# instantiate devices
mobiles = [mobile('m%d'%i) for i in range(47)]
servers = [server(name) for name in ['s0', 's1']]
nodes = mobiles + servers

# connect devices
net = topo.connect(nodes, 
    latency == normal(mean=ms(5), variance=1.0),
    capacity == normal(mean=mbps(15), variance=0.3),
    collision == poisson(rate=47), 
    migration == poisson(rate=10),
)
```
