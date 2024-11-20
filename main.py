"""
License : zlib/libpng
Copyright (c) 2024 Kimi Malkamäki (@kimierik)

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.
"""

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




def remove_floating_comments(src):
    pos=0
    return_value =""

    def check_comment_end()-> bool:
        i=0
        while(src[pos+i][0:2] == "//"):
            i+=1
            if pos+i == len(src):
                return True
        return src[pos+i]==""


    while (pos < len(src)):
        line = src[pos]
        pos+=1

        if line=="":
            return_value+= "\n"
            continue

        if line[0:2] =="//":
            if check_comment_end():
                # remove comment
                pass
            else:
                #keep comment
                return_value += line
                return_value+= "\n"
            continue

        if line[0:2] =="/*":
            while(not "*/" in src[pos]):
                pos+=1
            continue
        if line[0] =="*":
            continue

        return_value+= line
        return_value+= "\n"

    return return_value



def removeDefinitions(src):
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

    totalout = remove_floating_comments(output)
    totalout = removeDefinitions(totalout)

    totalout = remove_floating_comments(totalout.split(sep="\n"))

    #remove leading and trailing whitespace from totalout
    totalout = totalout.strip()

    print(totalout)



if __name__=="__main__":
    main()
