# The existence of this class is a result of the rather unique situation our library setup has put us in.
# We need to access certain global variables from our cogs/plugins such as the channel id
# but we can't control Discord's library or what it passes to our cogs/plugins when they're initialized
# nor can we import our main python file as it'll rerun all the code in the file and our recent refactor to use the
# if __name__ == "__main__": line to prevent most of the class from running when being imported complicates this further

# Our only other option was saving our data to a file and loading it again, which would be inefficient at best
# So I've settled on working around the nature of Python's objects and created a class that returns the same object in
# every instance of that class

# This class does expose the entire config object which could be a security risk
# But the likelihood of this being used for a credible attack is low enough that we can afford to fix this later
class GlobalVariables(object):
    _instance = None
    config = None
    client = None
    messages = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalVariables, cls).__new__(cls)
            # Put any initialization stuff here
        return cls._instance

    def set_config(self, config):
        self.config = config

    def set_client(self, client):
        self.client = client
