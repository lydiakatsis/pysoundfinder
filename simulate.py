'''
Simulate a sound's time delay of arrival 
to each recorder in a synchronized array

Usage:
Simulate TDOAs at recorders 1-4 for a 
sound located at (3, 17):

    [r1, r2, r3, r4] = simulate_dist(
            recorder_coords = [(0, 0), 
                           (0, 30),
                           (30, 0),
                           (30, 30)]
            source_coords = (3, 17),
            temp_c = 21.5
            print_results = False)


Simulate TDOAs  at recorders 1-3 for a sound at 
a randomly chosen location with random seed 222. 
Print results, including the chosen spot location:

    [r1, r2, r3] = simulate_dist(
            recorder_coords = [(0, 0), (0, 30), (30, 0)],
            rand_seed = 222, 
            temp_c = 10.0
            print_results = True):

    
'''

import numpy as np
import random
import pandas as pd

def calc_sos(temp_celsius = 20, humidity = None):
    '''
    Calculate speed of sound
    
    Calculate speed of sound for a given temperature
    in Celsius and humidity. (Humidity has a negligible
    effect on speed of sound and so this functionality
    is not implemented yet; will raise a NotImplementedError.)
    
    Inputs: 
        temp_celsius: the temperature in Celsius
        humidity: the humidity 
        
    Returns:
        the speed of sound
    '''
    if humidity:
        raise NotImplementedError('Humidity functionality is not implemented yet')
    else:
        return 331.3 * np.sqrt(1 + float(temp_celsius)/273.15)

def compute_toa(sound_pos, rec_pos, sos):
    '''
    Calculate sound time of arrival at recorder
    
    Assuming sound was made at time 0 at sound_pos,
    calculate what time it arrived at rec_pos
    
    Inputs:
        sound_pos: np.array position at which the sound was made
        rec_pos: np.array position of recorder to calculate sound toa
        sos: speed of sound in m/s
    
    Returns:
        the time of arrival of the sound
    '''
    
    distance = np.linalg.norm(sound_pos - rec_pos)
    return distance / sos

def quiet_print(desired_text, should_print):
    if should_print:
        print(desired_text)
        return
    else:
        return

def check_inputs(recorders, desired_spot, rand_seed):
             
    # Create np.array list of recorders
    recorders
    for i, coord in enumerate(recorders):
        recorders[i] = np.array(coord)
    assert len(recorders) >= 3
    
    # Ensure one of the coordinates is either 2 or 3 dimensions,
    # and all of the other coordinates have the same dimensions
    dimension = len(recorders[0])
    assert ((dimension == 2) or (dimension == 3))
    for coord in recorders:
        assert len(coord) == dimension
    
    if desired_spot:
        # Make sure the desired spot is the same 
        # dimension as the (already-checked) recorders
        assert len(desired_spot) == dimension
    else:
        # Create a random point with the same dimensions
        random.seed(rand_seed)
        sound_x = random.random()*30
        sound_y = random.random()*30
        if dimension == 3: 
            sound_z = random.random()*30
            desired_spot = [sound_x, sound_y, sound_z]
        else:
            desired_spot = [sound_x, sound_y]
    s_pos = np.array(desired_spot)

    return recorders, s_pos
    

def simulate_dist(
        recorder_coords,
        source_coords = None, 
        rand_seed = 1, 
        temp_c = 20.0,
        print_results = True):
    
    '''
    
    Given a set of recorder coordinates, simulates
    a sound's time delays of arrival at recorder microphones.
    Sound can either be given, or generated randomly.
    
    Inputs:
        recorder_coords: a list or tuple of (x, y) or (x, y, z) 
            coordinates of recorders. All coordinates must 
            have the same dimension.
            
        source_coords: coordinates of the spot from which the
            simulated sound should emulate. If not provided,
            a random spot is created with the same
            dimensions as the provided recorder coordinates

        rand_seed: random seed for creating the desired spot

        temp_c: temperature in celsius

        print_results: Boolean, whether or not to print results
            (results are printed by default)

    Returns:
        a list of time delays for each recorder in the order
        that their coordinates were given
    '''
    
    coords, s_pos = check_inputs(recorder_coords, source_coords, rand_seed)
   
    # Compute time of arrivals:
    toa_list = []
    for coord in coords:
        toa_list.append(compute_toa(sound_pos = s_pos, rec_pos = coord, sos = calc_sos(temp_celsius = temp_c)))
    
    quiet_print("Recorder positions are:", print_results)
    for i, coord in enumerate(coords):
        quiet_print("{0}: {1}".format(i+1, coord), print_results)
        
    quiet_print("Sound position is {}\n".format(s_pos), print_results)
    quiet_print("Temperature is {}\n".format(temp_c), print_results)
    
    quiet_print("Time delays are:", print_results)
    for i, toa in enumerate(toa_list):
        quiet_print("To recorder {0}: {1}".format(i+1, toa), print_results)
    
    return toa_list
