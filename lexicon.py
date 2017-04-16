#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 10:49:23 2017

@author: srin
"""

import argparse

e_rule = ['me', 'pe', 'ber', 'ke', 'ter', 'se']
dip_rule = ['ai', 'au', 'ei', 'oi']
chvow_rule = ['ae', 'ia', 'iu', 'ie', 'io', 'ea', 'eo']
end_rule = {'b' : 'p', 'd':'t', 'g':'k'}
eng_rule = ['ng']

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
                if(i+1 == len(word)):
                    if(word[i] in end_rule.keys()):
                        phone.append(end_rule[word[i]])
                    else:
                        phone.append(word[i])
                else:
                    # The word to be check
                    the_word = word[i]+word[i+1]
                    
                    # The rule
                    if(the_word in e_rule):
                        phone.append(word[i])
                        phone.append('ax')
                        skip = 1
                    elif(the_word in dip_rule):
                        if(i+2 == len(word)):
                            phone.append('ay')
                            skip = 1
                        else:
                            pass
                    elif(the_word in chvow_rule):
                        phone.append(word[i])
                        phone.append('y')
                        phone.append(word[i+1])
                        skip = 1
                    elif(the_word in eng_rule):
                        phone.append('ng')
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
    
    parsed, unparsed = parser.parse_known_args()
    
    main(parsed)