### How to save index

Note you have to move it to cpu before saving it.

```
import faiss

cpu_index = faiss.index_gpu_to_cpu(gpu_index)
faiss.write_index(cpu_index, 't5_index.index')
```

## How to load index

This should save the time to create the larger indexes.

```
cpu_index = faiss.read_index('t5_index.index')
res = faiss.StandardGpuResources()
gpu_index = faiss.index_cpu_to_gpu(res, 0, cpu_index)
```
