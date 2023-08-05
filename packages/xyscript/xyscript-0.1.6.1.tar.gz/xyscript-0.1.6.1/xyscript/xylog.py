
 # print("\033[1;31m failed \033[0m")
    # print("\033[1;32m success \033[0m")
def faillog(content):
    print("\033[1;31m" + str(content) + "\033[0m")

def successlog(content):
    print("\033[1;32m" + str(content) + "\033[0m")

def warninglog(content):
    print("\033[1;33m" + str(content) + "\033[0m")

class logitem:
    def failitem(self,content,bold=False):
        boldstr = "1" if bold else "0"
        return "\033["+ boldstr +";31m" + str(content) + "\033[0m"

    def successitem(self,content,bold=False):
        boldstr = "1" if bold else "0"
        return "\033["+ boldstr +";32m" + str(content) + "\033[0m"
    
    def warningitem(self,content,bold=False):
        boldstr = "1" if bold else "0"
        return "\033["+ boldstr +";33m" + str(content) + "\033[0m"
    
