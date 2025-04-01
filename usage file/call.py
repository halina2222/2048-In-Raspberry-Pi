import  simple_app as app 


def output(previous):
    current = previous
    for n in app.main():
        if (n != current):
            current = n
            return n
            

