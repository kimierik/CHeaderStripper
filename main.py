import subprocess


class PreProcessor():
    def __init__(self,src) -> None:
        self.src=src
        self.defines={}

    def expand(self,line):
        retval = line
        for key,val in self.defines.items():
            if key in retval: 
                retval = retval.replace(key,val)
        return retval
        

    def read_defines(self):
        for line in self.src:
            if "#include" in line:
                continue
            if "#define" in line:
                r = line.strip()
                r= r[7:]# remove #define 
                r = r.split()
                if r[1] == "//":
                    r[1]=""

                self.defines[r[0]]=r[1]
                continue







# TODO: 
# remove OOP this can just be a few functions
class Parser():
    def __init__(self,src):
        self.src=src
        self.pos=0

    # if it comment should be deleted or not
    def check_comment_end(self)-> bool:
        i=1
        while(self.src[self.pos+i][0:2] == "//"):
            i+=1
            if self.pos+i == len(self.src):
                return True


        return self.src[self.pos+i]==""



    def parse_stage1(self):
        return_value =""

        #TODO: this needs to be able to handle /**/ syntax

        while (self.pos < len(self.src)):
            line = self.src[self.pos]
            self.pos+=1

            if line=="":
                return_value+= "\n"
                continue

            if line[0:2] =="//":
                if self.check_comment_end():
                    # remove comment
                    pass
                else:
                    # so add comment
                    return_value += line
                    return_value+= "\n"

                continue

            if line[0:2] =="/*":
                while(not "*/" in self.src[self.pos]):
                    self.pos+=1
                continue

            if line[0] =="*":
                continue

            return_value+= line
            return_value+= "\n"


        return return_value

    # stage 2 parse
    # remove lines that start with #
    def parse_stage2(self,src):
        src = src.split(sep="\n")
        pos=0
        returnval=""

        processor = PreProcessor(src)
        processor.read_defines()
        
        while (pos < len(src)):
            line = src[pos]
            pos+=1
            if "#include" in line:
                continue
            if "#define" in line:
                continue
            if line =="":
                returnval+="\n"
            else:
               returnval += processor.expand(line)
               returnval+="\n"
               

        return returnval



def main():
    filename="raygui.h"

    r = subprocess.run(
            ["gcc","-E","-nostdinc","-P","-C","-traditional-cpp",filename],
            capture_output=True,
            text=True)

    output = r.stdout

    totalout=""

    output=output.split(sep="\n")

    parser = Parser(output)
    totalout = parser.parse_stage1()
    totalout = parser.parse_stage2(totalout)

    parser2 = Parser(totalout.split(sep="\n"))
    totalout= parser2.parse_stage1()

    #remove leading and trailing whitespace from totalout
    totalout = totalout.strip()

    print(totalout)




if __name__=="__main__":
    main()
