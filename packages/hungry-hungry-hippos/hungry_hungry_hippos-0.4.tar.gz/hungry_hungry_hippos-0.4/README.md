# Use cases

- Got a script that you want to be able to run multiple instances of in parallel?
- Want to write a program from scratch that's ready to scale up?
- Using someone else's code that has race conditions and want to singleton-ize it?

# Intro

Hungry Hungry Hippos, (HHH) is a python implementation of redlock https://redis.io/topics/distlock with a set of examples that use docker, redis and docker compose.
The advantage of this approch, compared to multithreading, is that is can be applied in a single-threaded context (for example if you have to integrate existing code), or in a mutliple container instance context (think microservices) 

# Features

- atomic locking guarantees single lock acquisition
- works across machines / containers
- handles dead lock recovery
- can wrap existing code for cases when you cannot or do not want to do a rewrite.

# Key concepts

- Process isolation
- Destributed locks (see https://redis.io/topics/distlock)
- Command orchestration

# Toolchain

- docker - images, containers, volumes
- docker-compose - building, linking services, scaling services
- redis - in memory key-value database

# Installation

<code>pip install hungry-hungry-hippos</code>

See examples for use cases
