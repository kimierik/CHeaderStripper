#!/bin/python
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
import argparse


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

                if len(r)>=2:
                    if r[1] == "//":
                        r[1]=""
                else:
                    r.append("")

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
            if line[0]=="#":
                continue
            returnval += processor.expand(line)
            returnval+="\n"
           

    return returnval


def remove_typedef(src):
    pos=0
    returnval=""

    while (pos < len(src)):
        line = src[pos]
        pos+=1

        if line.strip()[0:7]=="typedef":
            nl = line
            while (nl != "}"):
                pos+=1
                tmp = src[pos]
                if tmp == "":
                    continue
                nl=tmp[0]
            pos+=1
            continue


        returnval+= src[pos-1]
        returnval+= "\n"

    return returnval


def remove_include_directive(src):
    pos=0
    returnval=""

    while (pos < len(src)):
        line = src[pos]
        pos+=1
        if "#include" in line:
            continue
        returnval+=line
    return returnval



def main():

    arg_parser=argparse.ArgumentParser( prog="Header Stripper", description="Strips C headers")

    arg_parser.add_argument("-f","--filename",help="input filename",required=True)
    arg_parser.add_argument("-o","--output",help="output filename, default = out.h",default="out.h")
    arg_parser.add_argument("-d","--define",help="all definitions to give to gcc",nargs="+")
    arg_parser.add_argument("--remove-comments",help="remove all comments from output",action="store_true")
    arg_parser.add_argument("--remove-typedef",help="remove all typedefs from output",action="store_true")

    args = arg_parser.parse_args()

    # read file first, remove #include directive, give to gcc
    file = open(args.filename)
    raw_content = file.readlines()
    file.close()
    # this fn cannot be used here
    strippedContent = remove_include_directive(raw_content)

    gcc_command = ["gcc","-E","-nostdinc",]
    if not args.remove_comments:
        gcc_command.append("-C")

    if args.define:
        for define in args.define:
            gcc_command.append(f"-D{define}")

    gcc_command.append("-")

    result = subprocess.run(
            gcc_command,
            capture_output=True,
            input=strippedContent,
            text=True)

    if result.returncode != 0:
        print("error executing",gcc_command)
        print(result.stderr)

    output = result.stdout
    output = output.split(sep="\n")
    output = remove_floating_comments(output)
    output = removeDefinitions(output.split(sep="\n"))

    if args.remove_typedef:
        output = remove_typedef(output.split(sep="\n"))

    output = remove_floating_comments(output.split(sep="\n"))

    #remove leading and trailing whitespace from output
    output = output.strip()

    with open(args.output,'w') as f:
        f.write(output)
    
    



if __name__=="__main__":
    main()
