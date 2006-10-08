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


from Cheetah.Template import Template


class BatchScriptTemplate(Template):


    """base class for Cheetah batch script templates"""

    
    def getStdin(self):        return self.getRemoteFilename('stdin')
    def getStdout(self):       return self.getRemoteFilename('stdout')
    def getStderr(self):       return self.getRemoteFilename('stderr')


    def getRemoteFilename(self, name):
        # stub
        stream = self.job.getTraitValue(name)
        return stream.name


    def getStagedFiles(self):
        # stub
        return []

    
    stdin        = property(getStdin)
    stdout       = property(getStdout)
    stderr       = property(getStderr)

    stagedFiles  = property(getStagedFiles)


# end of file 
