*Hufflepuffs are particularly good finders.*

Hufflepuff is a program for exploring large mostly-convex search spaces.
The algorithm it uses is basically
[beam search](https://en.wikipedia.org/wiki/Beam_search), except that it’s
expected that exploring all successors of any node is too computationally
expensive, and so it explores a sample of them (with larger sample sizes for
higher-scoring nodes).

You need to provide three things to Hufflepuff:

1. The initial state(s) to explore from.
1. A program for generating a successor of a given state.
   (the same state may be given multiple times to get multiple successors)
1. A program for assigning a score to any state.

Hufflepuff has been used to:

* Group students into roughly equal teams, given approximate skill levels.
* Assign students to classes, such that class sizes are roughly equal and
  students’ preferences are taken into account.
* Generate source code for an esoteric programming language that produced a
  desired output.

In those three cases, the initial states were randomly generated (with virtually
no domain knowledge), the successor generation just randomly changed elements in
the state, leaving the scoring program as the single place for specifying the
desired properties of the solution.

# Invocation

With a config file:

    $ hufflepuff -c config.cfg

config.cfg:

    initial-file = initial.json
    initial-binary = cat $initial-file
    mutate-binary = ./mutate
    score-binary = ./score

    beam-width = 5
    expand-mantissa = 1.25
    expand-multiplier = 3
    target = max

    num-iterations = 20
    parallelism = NUM_CPUS

The config file is a shorthand for providing the args on the command line:

    $ hufflepuff --initial-binary=./initial

# Search parameters

By default, hufflepuff will attempt to find states with the highest scores: this
is specified by ``--target=max``. If your score metric is a “cost”, then setting
``--target=min`` will make it attempt to find states with the lowest scores.

The algorithm followed for searching is:

1. Get the states from ``--initial-binary``.
1. For ``--num-iterations`` iterations:
  1. Generate a new set of states from the current set of states.
    * The best-scored state will have ``--expand-multiplier`` states generated
      from it.
    * Following states will have an exponentially decreasing number of states
      generated from them (rounding down, but there will always be at least one
      new state for each current state).
  1. Score the new states.
  1. Throw away all but the best ``--beam-width`` states.

However, in addition, the best ``--beam-width`` states ever seen are kept, for
output at the end of the search.

# Communication

All binaries are expected to use newline-separated JSON values, either read from
stdin, or written to stdout, encoded in UTF-8.

In order to fully utilise multiple cores, multiple instances of the mutation and
scoring binaries are run, and input is provided simultaneously (so these
binaries can be written as naïve single-threaded processes but still scale
seamlessly).

If this is not desired (for instance, if there is a shared resource, or if you
want to implement an more sophisticated form of parallelism),
set ``--parallelism=1``.
Future lines of input may be provided before a given line has finished
processing to aid in this, but this should not be relied upon (don’t block a
line of output on reading the next line of input).

## Initial binary

The ``initial-binary`` is run to provide the set of starting values for the
search. For convenience, the substring "$initial-file" is replaced with the
value of the ``initial-file`` argument, so the default behaviour is to read from
that file.

A particularly useful thing to do with this is to store the results of a search
in ``best.txt``, and then use ``--initial-file=best.json`` to continue the
search from that point.

## Mutation binary

The ``mutate-binary`` is run to take values and turn them into slightly
different values (e.g., swap two values in a list, or add/subtract some amount
from a number). Usually this should be done entirely at random, rather than
trying to make a “smart” decision: the search will quickly eliminate **really**
bad options, and you may need intermediate okay-ish states.

Each line of input should correspond to exactly one line of output (if
hufflepuff wants multiple mutations, it will enter the value multiple times).

## Scoring binary

The ``score-binary`` is run to provide a number (floating point or integral)
value for a value. The default meaning is that larger numbers are better, but
this is controlled by ``--target={max,min}``.

Each line of input should correspond to exactly one line of output, and this
program should be deterministic (a given value produces the same score every
time).
