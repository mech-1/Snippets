def say_hello(name):
   def _say_hello():
       return f"Hello, {name}"
   return _say_hello

print(say_hello("Peter"))
# print(say_hello()())