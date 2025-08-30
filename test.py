#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 18:16:06 2020

@author: Saad
"""

" Load libraries "
import pandas as pd
import numpy as np
import sys, getopt

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
       opts, args = getopt.getopt(argv,"hi:o:n:",["ifile=","ofile=","pname="])
    except getopt.GetoptError:
       print('test.py -i <inputfile> -o <outputfile>')
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print('test.py -i <inputfile> -o <outputfile> -n')
          sys.exit()
       elif opt in ("-i", "--ifile"):
          inputfile = arg
       elif opt in ("-o", "--ofile"):
          outputfile = arg
       elif opt in ("-n", "--pname"):
          programname = arg
          
          
    print('Input file is ', inputfile)
    print('Output file is ', outputfile)
    
    " Load spreadsheet "
    try:
         FSM_table = pd.ExcelFile(inputfile)
    except FileNotFoundError:
         print('Input file ', inputfile, ' does not exist')
    
    # Print the sheet names
    print(FSM_table.sheet_names)
    
    FSM_data = FSM_table.parse('FSM')
    
    print(FSM_data)
    
    States = FSM_data.values[:,0].tolist()    
    
    print(States)
    print(FSM_data.Outputs)
   
    out_file = open(outputfile, "w")
    
    # declaring program
    out_file.write('PROGRAM ')
    out_file.write(programname)
    
    #define state type 
    out_file.write('\n\nTYPE\n   state_var: (')
    for state in States:               
        out_file.write(state)
        if state != States[-1]:
            out_file.write(', ')    
           
    out_file.write(');\nEND_TYPE\n\n')
    
    # define output variables                  
    out_file.write('VAR_EXTERNAL\n')
    out_file.write('   output : BOOL;\n\n')
    for output in FSM_data.Outputs:
        out_file.write('   ')
        out_file.write(output)    
        out_file.write(' : BOOL;\n')
        
    out_file.write('\n')

    # define input variables                  
    for condition in FSM_data.columns.array[1:-1]:
        out_file.write('   ')
        out_file.write(condition)    
        out_file.write(' : BOOL;\n')
        
    out_file.write('END_VAR\n\n')
    
    # define state variable                  
    out_file.write('state: state_var := ')
    out_file.write(States[0])
    out_file.write(';\n\n')

    # FSM CASE statement
    out_file.write('CASE state OF\n')
        
    for state in States:
        out_file.write(state)
        out_file.write(':\n')
        
        for column in FSM_data.columns[1:-1]:
            #print(column)
            #print(FSM_data.values[States.index(state),FSM_data.columns.tolist().index(column)])
            try:
                np.isnan(FSM_data.values[States.index(state),FSM_data.columns.tolist().index(column)])                   
            except TypeError:
                
                out_file.write('   IF ')
                out_file.write(column)
                out_file.write(' THEN\n')
                
                out_file.write('       output := ')
                out_file.write(FSM_data.values[States.index(state),-1])
                out_file.write(';\n')
                
                out_file.write('       state := ')
                out_file.write(FSM_data.values[States.index(state),FSM_data.columns.tolist().index(column)])
                out_file.write(';\n')
        
                out_file.write('   END_IF;\n')                    

        
    out_file.write('END_CASE;\n\nEND_PROGRAM')

    out_file.close()

if __name__ == "__main__":
   main(sys.argv[1:])