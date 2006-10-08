#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class ConfigContext(object):


    def error(self, *args):
        self.ue.append(args)


    def unknownComponent(self, name):
        self.uuc.append(name)


    def unknownProperty(self, *args):
        self.uup.append(args)


    def claim(self, name):

        if not (self.uup or self.uuc or self.ue):
            return True
        
        self.up = [ (name + '.' + key, value, locator)
                    for key, value, locator in self.uup ]
        
        self.uc = [ name + '.' + key
                    for key in self.uuc]
        
        self.ue = [ (error, name + '.' + key, value, locator)
                    for error, key, value, locator in self.ue ]
        
        self.unknownProperties += self.uup
        self.unknownComponents += self.uuc
        self.errors += self.ue
        
        self.uup = []
        self.uuc = []
        self.ue = []
        
        return False


    def verifyConfiguration(self, modeName):
        """verify that the user input did not contain any typos"""

        class Channel(object):
            def __init__(self, factory):
                self.channel = factory("pyre.inventory")
                self.tally = 0
            def line(self, message):
                self.channel.line(message)
            def log(self, message=None, locator=None):
                self.channel.log(message, locator)
                self.tally += 1

        import journal
        info     = Channel(journal.info)
        warning  = Channel(journal.warning)
        error    = Channel(journal.error)

        mode = dict(
            relaxed   = dict(up=warning, uc=info,    e=warning),
            strict    = dict(up=error,   uc=warning, e=error),
            pedantic  = dict(up=error,   uc=error,   e=error),
            )
        
        channel = mode[modeName]

        if self.unknownProperties:
            for key, value, locator in self.unknownProperties:
                problem = ("unrecognized property '%s'" % key, key, value, locator)
                self.log(channel['up'], problem)

        if self.unknownComponents:
            self.log(channel['uc'], ("unknown components: %s" % ", ".join(self.unknownComponents),
                                     None, None, None))
        
        if self.errors:
            for problem in self.errors:
                self.log(channel['e'], problem)

        return error.tally == 0


    def log(self, channel, problem):
        
        error, key, value, locator = problem

        if value:
            channel.line("%s <- '%s'" % (key, value))
        channel.log(error, locator)

        channel.tally = channel.tally + 1
        
        return


    def __init__(self):
        self.unknownProperties = []
        self.unknownComponents = []
        self.errors = []

        # unclaimed errors
        self.uup = []
        self.uuc = []
        self.ue = []

        return


# end of file 
