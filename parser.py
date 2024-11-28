#!/bin/python

from typing import List


"""
Stage 1 Token types

Illegal

Identifier

OpenParen    #(
CloseParen   #)

OpenSquirly  #{
CloseSquirly #}

OpenBracket  #[
CloseBracket #]

CommentStart

CommentBlockStart
CommentBlockEnd

Literal

Comma
Semicolon
Operator

Comparator

LineBreak


"""


class Stage1Token():
    def __init__(self, pos:int, token_type:str, value:str) -> None:
        self.src_pos=pos
        self.token_type=token_type
        self.value=value
        




def tokenize_stage1(src:str) -> List[Stage1Token]:
    """
    Tokenize a file
    """
    str_position = 0

    tokenList=[]

    while(str_position < len(src)):
        char = src[str_position]

        match char:
            case char if char.isalpha():
                #start parsing identifier 
                s=""
                while (src[str_position].isalpha()):
                    s+=src[str_position]
                    str_position+=1

                tokenList.append(Stage1Token(str_position,"Identifier",s))
                #end 

            case char if char.isnumeric():
                #start parsin num literal
                s=""
                while (src[str_position].isnumeric()):
                    s+=src[str_position]
                    str_position+=1

                tokenList.append(Stage1Token(str_position,"Literal",s))
                #end 

            case "\"":
                #start parsin string literal
                s=""
                str_position+=1
                while ( src[str_position] is not "\"" ):
                    s+=src[str_position]
                    str_position+=1

                tokenList.append(Stage1Token(str_position,"Literal",s))
                #end

            case ";":
                tokenList.append(Stage1Token(str_position,"Semicolon",None))

            case ",":
                tokenList.append(Stage1Token(str_position,"Comma",None))

            case ">" | "==" | "<=" | ">=" | "<" :
                tokenList.append(Stage1Token(str_position,"Comparator",char))

            case "-" | "*" | "/" | "+" :
                tokenList.append(Stage1Token(str_position,"Operator",char))

            case "//":
                tokenList.append(Stage1Token(str_position,"CommentStart",None))

            case "/*":
                tokenList.append(Stage1Token(str_position,"CommentBlockStart",None))

            case "*/":
                tokenList.append(Stage1Token(str_position,"CommentBlockEnd",None))

            case "(":
                tokenList.append(Stage1Token(str_position,"OpenParen",None))
            case ")":
                tokenList.append(Stage1Token(str_position,"CloseParen",None))
            case "[":
                tokenList.append(Stage1Token(str_position,"OpenBracket",None))
            case "]":
                tokenList.append(Stage1Token(str_position,"CloseBracket",None))
            case "{":
                tokenList.append(Stage1Token(str_position,"OpenSquirly",None))
            case "}":
                tokenList.append(Stage1Token(str_position,"CloseSquirly",None))

            case "\n":
                tokenList.append(Stage1Token(str_position,"LineBreak","\n"))


            case _:
                tokenList.append(Stage1Token(str_position,"Illegal",None))
            # end of match statement

        #end of while loop

    return tokenList







"""
Stage 2 Token types

Comment
CommentBlock                # incase we need it
FunctionDefinition
FunctionDeclaration
TypeDefinition              # this also includes just struct and enum defines without the typedef keyword
WhiteSpace                  # junk whitespace


"""

class Stage2Token():
    def __init__(self,token_type,start,end) -> None:
        self.token_type=token_type
        self.start=start
        self.end=end



def find_pattern(lst:List[Stage2Token],pattern:List[str])->List[int]:
    """
    pattern is a list of tokentypes
    returns list of indexes where patterns start
    """

    return_value=[]

    #holy shit this fn is scitzo

    for i in range(0,len(lst)):

        # if first is a hit
        if lst[i].token_type == pattern[0]:

            # match entire pattern
            for j in range(0,len(pattern)):

                if (lst[i+j]==pattern[j]):

                    if j == len(pattern-1):
                        # we have the pattern
                        return_value.append(i)
                        pass
                else:
                    break

        else:
            continue


    return return_value


# tokenize string 
def tokenize_stage2(src:List[Stage1Token])->List[Stage2Token]:
    """
    Tokenize a list of stage1 tokens
    """
    pos = 0

    while (pos < len(src)):
        char= src[pos]

        match char:
            case _:
                pass

        pos+=1















def main():
    # read file
    # parse stage1
    # parse stage2
    # get options on what to do with the content of the file
    # write to out
    pass




if __name__ == "__main__" :
    main()
