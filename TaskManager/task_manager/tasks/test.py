class test:
    def __init__(self,fifo_callback):
        self.callback = fifo_callback

    def execute(self,data):
        print "Test task has been called !"
