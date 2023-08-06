
class file_model:
    rootDir = ""
    sourceFileName = ""
    content = ""

    def __init__(self):
        self.rootDir = ""
        self.sourceFileName = ""
        self.content = ""

    def readFile(self, fileName):
        if fileName == "":
            return
        self.extractFileNameAndRoot(fileName)
        try:
            fileHandler = open(self.rootDir + self.sourceFileName)
            self.content = fileHandler.read()
        except IOError:
            print "Couldn't read file"

    def toString(self):
        """
        Returns the content of Object as String.
        :returns: Content of the Object as String
        :rtype: str
        """
        return self.content

    def extractFileNameAndRoot(self, fileName):
        if fileName == "":
            print "getRootPath: FileName was empty!"
            return
        fileName.replace("\\", "/")
        self.sourceFileName = fileName[fileName.rfind('/'):]
        self.rootDir = fileName[:fileName.rfind('/') + 1]