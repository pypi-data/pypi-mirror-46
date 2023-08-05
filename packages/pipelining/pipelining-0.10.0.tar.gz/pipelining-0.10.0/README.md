# Pipelining

_Pipelining_ provides an abstraction on top of python multiprocessing artifacts to create stream-processing applications in a delcarative fashion.

## Glossary

* Stage: a class providing the business logic of a single step in the context of a complex process.
* WorkUnit: a object containing the data for the execution of a single operation in the stream.
* InputPort: an interface that a _Stage_ exposes to receive WorkUnits.
* OutputPort: an interface that a _Stage_ exposes to send WorkUnits.
* Pipe: a queue that connect output ports from previous stages to the input ports of following stages
* Pipeline: a class that manages the structure and lifecycle of all the stages and pipes of your process.

## Connections

A stage can have any number of ports. The following image illustrates a very simple _stage_ with a single input _port_ and a single output _port_:

![A very simple stage](./docs/Stage.png)

Stages can be combined to form pipelines. The following images illustrates a simple pipeline composed of two stages, connected by a single _pipe_, where one stage produces _work units_ and the other consumes them:

![A very simple pipeline](./docs/Simple_Pipeline.png)

With these basic building block, one can create larger pipelines to fullfil complex workflows. The following image shows an overly-complex pipeline to illustrate different options for connecting _stages_:

![An oveerly complex pipeline](./docs/Overly_Complex_Pipeline.png)