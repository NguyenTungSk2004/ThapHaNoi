stack = [1,2,3,4,5]
stack1 = [1,2,3,4]
def check(s):
    if s != stack:
        return "stack1"
    if s != stack1:
        return "stack"
    
print(check(stack1))
