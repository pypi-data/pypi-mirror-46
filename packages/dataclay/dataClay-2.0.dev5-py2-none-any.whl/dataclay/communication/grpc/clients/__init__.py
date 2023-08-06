
""" Class description goes here. """

"""Package containing clients gRPC classes."""
import os

__author__ = 'Enrico La Sala <enrico.lasala@bsc.es>'
__copyright__ = '2017 Barcelona Supercomputing Center (BSC-CNS)'

# @abarcelo Tale time! In a Mare Nostrum typical deployment, the _deploying a
# class process_ --i.e. LogicModule => Execution Environments-- is 0.5 seconds
# long, give or take. That means that a timeout of 20 seconds allows up to 40
# Execution Environments. Given that typical Mare Nostrum executions deploy 32
# Backends *per node*, we have to raise the timeout up to the sky. At least for
# that specific management operation.
GRPC_TIMEOUT = int(os.getenv("DATACLAY_GRPC_TIMEOUT", "300"))
