#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 10:49:23 2017

@author: srin
"""

import argparse

e_rule = ['me', 'pe', 'ber', 'ke', 'ter', 'se']
dip_rule = ['ai', 'au', 'ei', 'oi']
# chvow_rule = ['ae', 'ia', 'iu', 'ie', 'io', 'ea', 'eo']
end_rule = {'b' : 'p', 'd':'t', 'g':'k'}
eng_rule = ['ng', 'ny']
alphabet = {'b':'b e', 
              'c':'c e', 
              'd':'d e', 
              'f':'e f', 
              'g':'g e', 
              'h':'h a', 
              'j':'j e', 
              'k':'k a', 
              'l':'e l', 
              'm':'e m', 
              'n':'e n', 
              'p':'p e', 
              'q':'k i', 
              'r':'e r', 
              's':'e s', 
              't':'t e', 
              'v':'f e', 
              'w':'w e', 
              'x':'e k s', 
              'y':'y e', 
              'z':'z e t'}

def abb_rule(word):
    word = word.lower().strip()
    phone = []
    skip = 0
    
    if(len(word) > 0):
        for i in range(len(word)):
            if(skip > 0):
                skip = skip - 1
                pass
            elif(word[i] in alphabet):
                phone.append(alphabet[word[i]])
            else:
                phone.append(word[i])

    return phone

def lexi_rule(word):
    word = word.lower().strip()
    phone = []
    skip = 0
    
    if(len(word) > 0):
        for i in range(len(word)):
            if(skip > 0):
                skip = skip - 1
                pass
            else:
                if(word[i] == 'x'):
                    phone.append('k')
                    phone.append('s')
                elif(i+1 == len(word)):
                    if(word[i] in end_rule.keys()):
                        phone.append(end_rule[word[i]])
                    else:
                        phone.append(word[i])
                else:
                    # Check by two letters at a time
                    the_word = word[i]+word[i+1]
                    
                    # The rule
                    if(the_word in e_rule):
                        phone.append(word[i])
                        phone.append('ax')
                        skip = 1
                    elif((the_word in dip_rule) and (i+2 == len(word))):
                        if(the_word == 'ai'):
                            phone.append('a y')
                            skip = 1
                        elif(the_word == 'au'):
                            phone.append('a w')
                            skip = 1
                        elif(the_word == 'ei'):
                            phone.append('e y')
                            skip = 1
                        elif(the_word == 'oi'):
                            phone.append('o y')
                            skip = 1
                        else:
                            phone.append(word[i])
                            pass
#                     elif(the_word in chvow_rule):
#                         phone.append(word[i])
#                         phone.append('y')
#                         phone.append(word[i+1])
                        skip = 1
                    elif(the_word in eng_rule):
                        phone.append(word[i]+word[i+1])
                        skip = 1
                    else:
                        if(i+3 < len(word)):
                            the_3word = word[i]+word[i+1]+word[i+2]
                        
                            if(the_3word in e_rule):
                                phone.append(word[i])
                                phone.append('ax')
                                phone.append(word[i+2])
                                skip = 2
                            else:
                                phone.append(word[i])
                        else:
                            phone.append(word[i])
    
    return phone

def save_lexi(lexi, fl):
    f = open(fl, 'w')
    f.write('SIL <SIL>\n')
    
    for l in lexi:
        print l[0], ' '.join(l[1])
        f.write(l[0]+' '+' '.join(l[1])+'\n')
    
    f.close()
    
    print('DONE')
    

def main(arg):
    res = []
    fl = open(arg.src, 'r')
    
    for ln in fl:
        if(arg.abb):
            phone = abb_rule(ln)
        else:
            phone = lexi_rule(ln)
        res.append([ln.lower().strip(), phone]);
    
    save_lexi(res, arg.save)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
                        '-src',
                        type=str,
                        default='/tmp/data',
                        help='file contain word or sentences')
    parser.add_argument(
                        '-save',
                        type=str,
                        default='resultlexi',
                        help='file result')
    parser.add_argument(
                        '-abb',
                        action='store_true', default=False,
                        help='is abbreviation file')
    
    parsed, unparsed = parser.parse_known_args()
    
    main(parsed)
