#import dis
import trace

def hi():
    print("Hello, World!")

#dis.dis(hi)

tracer = trace.Trace(count=False, trace=True)
tracer.run('hi()')