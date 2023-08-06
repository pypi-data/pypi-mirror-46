# -*- coding: utf-8 -*-
"""
Created on Tue May 14 17:36:41 2019

@author: adampkehoe
"""

"""
This is the demo, it incorporates a few things.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import operator
import random
from collections import defaultdict
import sys
import time

class CHRDataEntryDemo(object,):
    
    def __init__(self,   local=True,                       
                         run_manual_entry=False,
                         run_tests=False,
                         run_example=False,
                         error_audit=False,
                         employ_hybrid_scheme=False,
                         hybrid_threshold=100,
                         success_number=5
                         ):
        
        if local:
            self.set_working_directory()
        if run_manual_entry:
            self.run_manual_entry(error_audit)
        if run_example:
            self.run_sample()
        if run_tests:
            self.run_against_data(success_number, employ_hybrid_scheme, hybrid_threshold)
           
    def set_working_directory(self, d='C:\\Users\\adamp\\PycharmProjects\\ps_chr_data_entry'):
        success=False
        while not success:
            answer = input('Do you need to reset working directory (Y/N)? ')
            if answer.lower().strip()=='y':
                d = input('input new directory now: ')
                try:
                    os.chdir(d)
                    success=True
                except:
                    print('retry: invalid directory {}' .format(d))
            elif answer.lower().strip()=='n':
                try:
                    os.chdir(d)
                    success=True
                except:
                    print('retry: invalid directory {}' .format(d))
        print('working directory set {} \n' .format(d))   
                
    def error_detection(self, main_probs_table, next_field):
        s = sorted(main_probs_table[next_field].items(), key=operator.itemgetter(1), reverse=True)   
        predictions = []
        percent_not_error = 0
        i = 0
        while i < 50 and len(predictions) < len(s):
            predictions.append(s[i][0])      
            percent_not_error += s[i][1]
            i+=1           
        percent_not_error *= 100       
        return predictions, percent_not_error
    
    def fix_the_fields(self, fields):        
        done = False
        while done == False:
            ans = input('Would you like to fix any fields (Y/N)? ')
            if ans.lower().strip()=='y':
                asserting = True
                while asserting == True:
                    print('Your choices are: {}'.format(fields))
                    fixed_fields = [input('Enter fields separated by commas: \n')]
                    asserting = False
                    done = True
                    for field in fixed_fields:
                        if field not in fields:
                            asserting = True
                            done = False
                    if asserting == True:
                        print('You need to enter valid fields\n')
                    else:
                        fixed_values = [input('Enter the corresponding values in each of those fields separated by commas (note, only one value per field at this time): \n')]
                        if len(fixed_values) != len(fixed_fields):
                            print('Number of fixed fields does not equal number of fixed values \n')
                        else:
                            asserting = False
                            fix_fields = True
                        done = True                  
            elif ans.lower().strip()=='n':
                fixed_values = []
                fixed_fields = []
                fix_fields = False
                done = True         
        return fixed_fields, fixed_values, fix_fields
    
    def fix_the_order(self, fields):        
        done = False
        while done == False:
            ans = input('Would you like to fix any of the order (Y/N)? ')
            if ans.lower().strip()=='y':
                asserting = True
                while asserting == True:
                    print('Your choices are: {}\n'.format(fields))
                    fixed_order = [input('Enter fields to fix in order separated by commas: ')]
                    fix_order = True
                    asserting = False
                    done = True
                    for field in fixed_order:
                        if field not in fields:
                            asserting = True
                            done = False
                    if asserting == True:
                        print('You need to enter valid fields\n')                                       
            elif ans.lower().strip()=='n':
                fixed_order = []
                fix_order = False
                done = True
 
        return fixed_order, fix_order
    
    def get_code_names(self, predictions, next_field, carrier_names, warehouse_names, customer_names):       
        if next_field == 'carrier_code':
            names = []
            for i in predictions:
                try:
                    name = str(i) + ' -> ' + str(carrier_names[i]) 
                    names.append(name)
                except:
                    print(i, 'does not have a name associated with it')
            print('The associated names for', next_field,  'are:', names)
            print()       
        if next_field == 'warehouse_code':
            names = []
            for i in predictions:
                try:
                    name = str(i) + ' -> ' + str(warehouse_names[i])
                    names.append(name) 
                except:
                    print(i, 'does not have a name associated with it')
            print('The associated names for', next_field,  'are:', names)
            print()        
        if next_field == 'customer_code_custs' or 'customer_code_lbt':
            names = []
            for i in predictions:
                try:
                    name = str(i) + ' -> ' + str(customer_names[i])
                    names.append(name)
                except:
                    print(i, 'does not have a name associated with it')
            print('The associated names for', next_field,  'are:', names)
            print()
            
    def input_answer(self, error_audit):       
            answering = True
            while answering == True:
                answer = input('Input the value you\'d like to assign to the field {} (if the field is one of the codes, enter the code itself, not the name): '.format(next_field))
                print()
                if error_audit == True:
                    error_predictions, percent_not_error = self.error_detection(main_probs_table, next_field)
                
                    if answer not in error_predictions:
                    
                        print('According to our system, there is a {} % that {} is an erroneous value'.format(round(percent_not_error, 4), answer))
                        deciding = True
                        while deciding==True: 
                            ans = input('Would you like to enter another value (Y/N)? ')
                            if ans.lower().strip()=='y':
                                deciding = False
                            elif ans.lower().strip()=='n':
                                answering = False
                                deciding = False
                    else:
                        answering = False                          
                else:
                    answering = False
            return answer
                    
    def input_field(self, current_fields, available_fields, previous_field, order_at):
        deciding_field = True
        while deciding_field == True:         
            try:
                available_fields.remove(previous_field)
            except:
                pass
            if order_at == 1:
                print()
                next_field = input('What field would you like to fill in first? Enter here: ')
                print()
            else:
                next_field = input('What field would you like to fill in next? Enter here: ')
                print()
            if next_field in fields:
                current_fields.append(next_field)
                deciding_field = False
            else:
                print('You need to pick a valid field, your choices are {}\n'.format(available_fields))  
            
        return current_fields, next_field
    
    def input_next_field(self, answer_list, length, running):
        order_at += 1
        if len(answer_list) < len(length):   
            questioning = True
            while questioning == True:
                ans = input('Would you like to continue and choose another field (Y/N)?: ')
                print()
                if ans.lower().strip()=='y':
                    questioning = False
                elif ans.lower().strip()=='n':
                    running = False
                    questioning = False
        else:
            print('Entry completed, no more fields to fill out \n')
            running = False  
        
        return running
        
    def load_input(self,):       
        success=False
        while not success:
            answer = input('Would you like to run any tests against previously entered data (Y/N)? ' )
            if answer.lower().strip()=='y':
                while not success:
                    directory = input('Where is the data located? Enter the full directory: ')
                    try:
                        os.chdir(directory)
                        success=True
                    except:
                        print('Not a valid directory')
                success=False
                while not success:
                    file_name = input('What is the name of the file? (Note, only csv, xls, and xlsx files currently supported): ')
                    try:
                        if file_name.split('.')[1] == 'csv':
                            try:
                                print('Loading test file...')
                                df = pd.read_csv(file_name)
                                success=True
                            except:
                                print(file_name, 'not in', directory)
                        elif file_name.split('.')[1] == 'xlsx' or file_name.split('.')[1] == 'xls':
                            try:
                                print('Loading test file...')
                                df = pd.read_excel(file_name)
                                success=True
                            except:
                                print(file_name, 'not in', directory)  
                    except:
                        if file_name not in os.listdir():
                            print(file_name, 'not in', directory)
                        
            elif answer.lower().strip()=='n':
                    success=True
                    
        return df
    
    def load_main_data_file(self,):
        print('A data file must be loaded in order for the hybrid scheme to be successfully employed')
        print('Ideally, this file should be separate from the data you are testing against')
        success=False
        while not success:
            directory = input('Where is the file located? Enter the full directory: \n')
            try:
                os.chdir(directory)
                success=True
            except:
                print('Not a valid directory')
        success=False
        while not success:
            file_name = input('What is the name of the file? (Note, only csv, xls, and xlsx files currently supported \n')
            if file_name.split('.')[1] == 'csv':
                try:
                    print('Loading test file\n')
                    df = pd.read_csv(file_name)
                    success=True
                except:
                    print('Not a valid file\n')
            elif file_name.split('.')[1] == 'xlsx' or file_name.split('.')[1] == 'xls':
                try:
                    print('Loading test file\n')
                    df = pd.read_excel(file_name)
                    success=True
                except:
                    print('Not a valid file\n')                                  
        return df
    
    def load_probability_tables(self,):
        cwd = os.getcwd()
        if 'pair_probs_table.npy' and 'main_probs_table.npy' in os.listdir():
            pass
        else:
            finding = True
            while finding == True:
                directory = input('Please enter the directory in which the files \'pair_probs_table.npy\' and \'main_probs_table.npy\' are located: \n')
                try:
                    os.chdir(directory)
                    if 'pair_probs_table.npy' and 'main_probs_table.npy' in os.listdir():
                        finding = False
                    else:
                        print('\'pair_probs_table.npy\' and \'main_probs_table.npy\ are not in', directory)
                except:
                    print('Not a valid directory')
        
        print('Loading tables...\n')    
        main_probs_table = np.load('main_probs_table.npy').item()
        pair_probs_table = np.load('pair_probs_table.npy').item()
        os.chdir(cwd)
            
        return main_probs_table, pair_probs_table
    
    def most_likely_values(self, main_probs_table, next_field, success_number):
         
        s = sorted(main_probs_table[next_field].items(), key=operator.itemgetter(1), reverse=True)
    
        predictions = []
        i = 0
        while i < success_number and len(predictions) < len(s):
            predictions.append(s[i][0])
            i+=1
            
        return predictions

    
    def run_against_data(self, success_number, employ_hybrid_scheme, hybrid_threshold):
        
        test_file = self.load_input()
        main_probs_table, pair_probs_table = self.load_probability_tables()
        fields = list(main_probs_table.keys())
        fixed_fields, fixed_values, fix_fields = self.fix_the_fields(fields)
        fixed_order, fix_order = self.fix_the_order(fields)
        answer_list = fixed_values
        current_fields = fixed_fields
        success_dict = {}
        order_at = 1
        j = 0
        if employ_hybrid_scheme == True:           
            df = self.load_main_data_file()  
            proportion_val = {}
        for i in fixed_order:
            if type(i) == int:
                fixed_order[j] = test_file.columns[i]
                j += 1
        
        print('beginning tests...')
        start = datetime.now()       
        success_count = 0
        total_guesses = 0
        success_dict = defaultdict(int)
        position_performance = defaultdict(int)
        position_counts = defaultdict(lambda: defaultdict(int))
        field_position_performance = defaultdict(lambda: defaultdict(int))
    
        for i in range(len(test_file)):            
            if i%10 == 0:
                print('beginning test', i)
            entry = test_file.iloc[i]
            if fix_fields == True:           
                predict_fields = [field for field in test_file.columns if field not in fixed_fields]
                random.shuffle(predict_fields)              
            if fix_order == True:          
                predict_fields = [field for field in test_file.columns if field in fixed_order and field not in fixed_fields]
                predict_fields.append(field for field in test_file.columns if field not in predict_fields)   
            else:         
                predict_fields = fields   
                random.shuffle(predict_fields)
                
            current_fields = [field for field in fixed_fields]
            answer_list = [val for val in fixed_values]
            order_at = 1
            
            for field in predict_fields:                
                answer = entry[field]
                if employ_hybrid_scheme == True:                
                    proportion_val[field] = df[field].value_counts(normalize=True)
                    df = df.loc[df[field] == answer]                 
                    if len(df) >= hybrid_threshold:
                        answer_list.append(answer)
                        predictions = proportion_val[field].keys()                      
                    else:
                        if len(answer_list)!= 0:
                            main_probs_table = self.update_probs_table(main_probs_table, pair_probs_table, \
                                                                       current_fields, field, answer_list)
                        predictions = self.most_likely_values(main_probs_table, field, success_number)                                            
                else:       
                    if len(answer_list)!= 0:
                        main_probs_table = self.update_probs_table(main_probs_table, pair_probs_table, \
                                                                   current_fields, field, answer_list)
                    predictions = self.most_likely_values(main_probs_table, field, success_number)                
                if answer in predictions:
                    success_count += 1
                    success_dict[field] += 1
                    position_performance[order_at] += 0
                    field_position_performance[field][order_at] += 1
                
                current_fields.append(field)
                answer_list.append(answer)
                position_counts[field][order_at] += 1    
                order_at += 1
                total_guesses += 1
        
        print('total test time: {} seconds'.format(round((datetime.now() - start).total_seconds(), 3)))
        print()
        
        for k in range(1, success_number+1):
            print('In total', success_count/total_guesses * 100, '%', 'of correct answers were in the top\n', success_number)
        success_dict_pcts = defaultdict(defaultdict)
        for i in success_dict:
            success_dict_pcts[i] = str(success_dict[i]/(len(test_file))*100)+'%'
        print('These are the % in the top', success_number, 'for each field \n')
        print(success_dict_pcts)  
        
        position_performance_pcts = defaultdict(defaultdict)
        for i in position_performance:
            position_performance_pcts[i] = str(position_performance[i]/(len(test_file))*100)+'%'
        print('These are the % in the top', success_number, 'for each position in the order of entry \n')
        print(position_performance_pcts)
        
        field_position_pcts = defaultdict(lambda: defaultdict(defaultdict))
        for field in field_position_performance:
            for order_at in field_position_performance[field]:
                field_position_pcts[field][order_at] = str(field_position_performance[field][order_at]/(position_counts[field][order_at])*100)+'%'
        print('These are the % in the top', success_number, 'for each field for its respective position in the order')
        
    def run_manual_entry(self, error_audit, success_number=5, summary_results=True):
        main_probs_table, pair_probs_table = self.load_probability_tables()
        fields = list(main_probs_table.keys())
        fixed_fields, fixed_values, fix_fields = self.fix_the_fields(fields)
        fixed_order, fix_order = self.fix_the_order(fields)
        answer_list = fixed_values
        current_fields = fixed_fields
        available_fields = fields
        previous_field = []
        success_dict = {}
        order_at = 1
        length = len(main_probs_table.keys())
        customer_names = np.load('customer_names.npy').item()
        carrier_names = np.load('carrier_names.npy').item()
        warehouse_names = np.load('warehouse_names.npy').item()
        running=True
        while running:

            current_fields, next_field = self.input_field(current_fields, available_fields, previous_field, order_at)                
            print('Making predictions...')              
            predictions = self.most_likely_values(main_probs_table, next_field, success_number)
            print('Here are the top {} predictions for {}:\n'.format(success_number, next_field))
            print(predictions)
            print()            
            self.get_code_names(predictions, next_field, carrier_names, warehouse_names, customer_names)
            answer = self.input_answer(error_audit)
            answer_list.append(answer)
            if answer in predictions:
                success_dict[next_field] = 1
            else:
                success_dict[next_field] = 0
            
            start = datetime.now()
            print('Updating table...')
            main_probs_table = self.update_probs_table(main_probs_table, pair_probs_table, current_fields, next_field, answer_list)
            print('Finished updating table, took {} seconds'.format(round((datetime.now() - start).total_seconds(), 3)))
            print()
            previous_field = next_field
            order_at += 1
            running = self.input_next_field(next_field, answer_list, length, running)
       
        if summary_results == True:
            print()
            print('Results summary:')
            print('The selection you made was in the top 5 predictions produced by the system in {} out of {} cases\n'.format(sum(success_dict.values()), len(success_dict)))
            i = 0
            for field in success_dict:
                if success_dict[field] == 1:
                    print('Successful prediction for', field, 'given', current_fields[:i])
                    print()
                if success_dict[field] == 0:
                    print('Unsuccessful prediction for', field, 'given', current_fields[:i])
                    print()
                i+=1
                
    def run_sample(self, success_number=5):      
        main_probs_table, pair_probs_table = self.load_probability_tables() 
        fields = list(main_probs_table.keys())
        available_fields = fields
        answer_list = []
        current_fields = []
        previous_field = []
        success_dict = {}
        order_at = 1
        example_fields = ['inco_terms', 'warehouse_code', 'customer_code_custs']
        example_answers = ['fob', 'w1035958', 'c7210516']
        customer_names = np.load('customer_names.npy').item()
        carrier_names = np.load('carrier_names.npy').item()
        warehouse_names = np.load('warehouse_names.npy').item()
        running=True
        while running:        
            try:
                available_fields.remove(previous_field)
            except:
                pass
            if order_at == 1:
                print()
                print('What field would you like to fill in first? Enter here: ')
                time.sleep(3)
                print(example_fields[0])
                time.sleep(1)
                next_field = example_fields[0]
                current_fields.append(next_field)
            else:
                print('What field would you like to fill in next? Enter here: ')
                time.sleep(3)
                print(example_fields[order_at-1])
                time.sleep(1)
                next_field = example_fields[order_at-1]
                current_fields.append(next_field)
            print()
                     
            print('Making predictions...')              
            predictions = self.most_likely_values(main_probs_table, next_field, success_number)
            print('Here are the top {} predictions for {}:\n'.format(success_number, next_field))
            print(predictions)
            print()            
            self.get_code_names(predictions, next_field, carrier_names, warehouse_names, customer_names)
            print('Input the value you\'d like to assign to the field {} (if the field is one of the codes, enter the code itself, not the name): '.format(next_field))
            answer = example_answers[order_at-1]
            time.sleep(5)
            print(answer)
            print()

            error_predictions, percent_not_error = self.error_detection(main_probs_table, next_field)           
            if answer not in error_predictions:        
                print('According to our system, there is a {} % that {} is an erroneous value'.format(round(percent_not_error, 4), answer))
                print()
                print('Would you like to enter another value (Y/N)? ')
                time.sleep(2)
                print('N')   
            answer_list.append(answer)
            if answer in predictions:
                success_dict[next_field] = 1
            else:
                success_dict[next_field] = 0
            
            start = datetime.now()
            print('Updating table...')
            main_probs_table = self.update_probs_table(main_probs_table, pair_probs_table, current_fields, next_field, answer_list)
            print('Finished updating table, took {} seconds'.format(round((datetime.now() - start).total_seconds(), 3)))
            print()
            previous_field = next_field
            
            print('Would you like to continue and choose another field (Y/N)?: ')
            if order_at < len(example_answers):
                time.sleep(2)
                print('Y')        
            else:
                time.sleep(2)
                print('N')
                running = False
            order_at += 1
       
        print()
        print('Results summary:')
        print('The selection you made was in the top 5 predictions produced by the system in {} out of {} cases\n'.format(sum(success_dict.values()), len(success_dict)))
        i = 0
        for field in success_dict:
            if success_dict[field] == 1:
                print('Successful prediction for', field, 'given', current_fields[:i])
                print()
            if success_dict[field] == 0:
                print('Unsuccessful prediction for', field, 'given', current_fields[:i])
                print()
            i+=1
                
    def update_probs_table(self, main_probs_table, pair_probs_table, current_fields, next_field, answer_list):       
        for val in pair_probs_table[next_field]:
            if type(val) != float:
                update = 0
                i = 0
                for ans in answer_list:
                    if ans in pair_probs_table[current_fields[i]]:
                        if (next_field, val) in pair_probs_table[current_fields[i]][ans]:
                            update += pair_probs_table[current_fields[i]][ans][(next_field, val)]
                    i+=1  
            main_probs_table[next_field][val] = update / len(answer_list)
        return main_probs_table
        
        
def main(argv):
    '''
    Main method to run the script.  But can also pip install and run outstide
    of here by importing the CHRDataEntryDemo class.
    
    '''
    CHRDataEntryDemo(error_audit=True, run_example=True)

if __name__ == "__main__": 
    main(sys.argv[1:])    


        
        
        
    
    
    
    
