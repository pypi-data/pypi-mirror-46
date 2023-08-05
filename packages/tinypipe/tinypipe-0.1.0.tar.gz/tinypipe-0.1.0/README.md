# TinyPipe

**TinyPipe** is a lightweight library that facilitates the application of the Pipeline Pattern. A pipeline has a general form as follows:

```
       |---|    |----|    |- -|    |----|    |---|
... -> | Q | -> | OP | -> | Q | -> | OP | -> | Q | -> ...
       |---|    |----|    |---|    |----|    |---|
```

As data flows through the pipeline, it is first fed into the input queue (denoted as `Q` above). The following operation unit (`OP`) grabs it and produces a result, which is then fed into its output queue. This process continues until the data encounters a terminating `OP` which has no output queue.

Building blocks are provided for pipeline construction, where each operation unit (represented by `Pipe`), owns a threads and runs individually. A `ParallelPipe` is also included for an operation to run with multiple threads. See the documentation for detail.

## Setup

Python version: 3.6+ (other versions not tested, feel free to try it out!)

To install **TinyPipe**:

```bash
$ pip install tinypipe
```

## Usage

Suppose every data has to go through the functions `f1`, `f2`, and `f3` in sequence. The pipeline can be constructed by:

```python
import tinypipe as tp

# 1. Create pipeline
pipeline = tp.Pipeline()

# 2. Append pipes to pipeline
f1_pipe = tp.pipe.FunctionPipe(f1)
pipeline.append(f1_pipe)

f2_pipe = tp.pipe.FunctionPipe(f2)
pipeline.append(f2_pipe)

f3_pipe = tp.pipe.FunctionPipe(f3)
pipeline.append(f3_pipe)
# One can call `pipeline.extend([f1_pipe, f2_pipe, f3_pipe])` instead

# 3. Build & start the pipeline
# Once the pipeline is started, it will keep trying to get data to process
pipeline.build()
pipeline.start()

# 5. Feed data into the pipeline
data_iterator = ...
for data in data_iterator:
  pipeline.put(data)

# 6. If all the data has been passed into the pipeline,
#    wait for it to finish all the work.
pipeline.join()
```
