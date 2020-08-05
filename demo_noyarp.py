from pyicubsim import NoYarp

query = NoYarp.query('localhost','/icubSim/left_arm/rpc:i')
print(query)

position = NoYarp.command(query,'get pos 1')
print(position)

NoYarp.command(query,'set pos 1 130')
position = NoYarp.command(query,'get pos 1')
print(position)
