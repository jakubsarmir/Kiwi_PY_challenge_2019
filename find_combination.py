#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
usage:
cat about.txt | python soinput.py
'''

import sys
from datetime import datetime


def read_in():
    lines = sys.stdin.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '')
    header = lines.pop(0).split(',')
    flights_list = []

    for line in lines:
        line_to_array = line.split(',')
        flights_list.append(dict(zip(header, line_to_array)))

    flights = [item for item in flights_list if int(item['bags_allowed']) >= int(sys.argv[1])]

    for item in flights:
        item['arrival'] = datetime.strptime(item['arrival'].replace('T', ' '), '%Y-%m-%d %H:%M:%S')
        item['departure'] = datetime.strptime(item['departure'].replace('T', ' '), '%Y-%m-%d %H:%M:%S')

    sorted_data = sorted(flights, key=lambda x: (x['source'], x['departure']))

    return sorted_data


def search(previous, lst, whole_lst, all_possible_combinations):
    x = []
    for i in previous:
        x.append(i)
    if not lst:
        return False

    for item in lst:
        previous.append(item)
        z = []
        for i in previous:
            z.append(i)
        all_possible_combinations.append(z)
        for node in whole_lst:
            if item == node['node']:
                if not search(previous, node['options'], whole_lst, all_possible_combinations):
                    previous = []
                    for i in x:
                        previous.append(i)
                break

    return False


def main():
    # read the data and format it to suitable form for an searching algorithm
    data = read_in()

    possible_flights_from_a_node = []
    for flight in data:
        flights_from_node = dict()
        flights_from_node['node'] = flight['flight_number']
        flights_from_node['options'] = []
        for item in data:
            diff = (item['departure'] - flight['arrival']).total_seconds() / 3600
            if item['source'] == flight['destination'] and (1 <= diff <= 4):
                flights_from_node['options'].append(item['flight_number'])
        possible_flights_from_a_node.append(flights_from_node)

    # call the searching algorithm and find all combinations
    all_combinations = []
    for item in possible_flights_from_a_node:
        prev = [item['node']]
        search(prev, item['options'], possible_flights_from_a_node, all_combinations)

    # remove combinations flying the same direction twice and format the rest to final format
    output_data = []
    for combination in all_combinations:
        if len(combination) > 2:
            source_departure_pairs = []
            for i in range(len(combination)):
                pair = []
                for segment in data:
                    if i < len(combination) - 1:
                        if segment['flight_number'] == combination[i] or segment['flight_number'] == combination[i + 1]:
                            pair.append(segment['source'])
                    else:
                        if segment['flight_number'] == combination[i]:
                            pair.append(segment['source'])
                            pair.append(segment['destination'])
                if pair not in source_departure_pairs:
                    source_departure_pairs.append(pair)
                else:
                    break
            if len(source_departure_pairs) != len(combination): continue
        output_dict = dict()
        output_dict['flight_numbers'] = []
        output_dict['destinations'] = []
        output_dict['price'] = 0
        for index in range(len(combination)):
            for flight_data in data:
                if flight_data['flight_number'] == combination[index]:
                    output_dict['flight_numbers'].append(flight_data['flight_number'])
                    if index < len(combination) - 1:
                        output_dict['destinations'].append(flight_data['source'])
                    else:
                        output_dict['destinations'].append(flight_data['source'])
                        output_dict['destinations'].append(flight_data['destination'])
                    output_dict['price'] += int(flight_data['price']) + int(flight_data['bag_price']) * int(sys.argv[1])
        output_data.append(output_dict)

    print(output_data)


if __name__ == '__main__':
    main()
