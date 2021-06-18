import math; import sys
# --- Program Title and Lines Section ---
title = 'This program calculates the coordinates in open traverse serie'
proportion = len(title)
print('\n' + title + '\n' + ('-' * proportion))  # Print Title and Lines

# --- Variable Section ---
pID_first = input(f'{"Enter the point ID of first known point":<{proportion - 2}} {": "}')  # First PID
y_known_1 = float(input(f'{"Enter the Y coordinates of first known point":<{proportion - 5}} {"(m): "}'))  # First Known Y Coordinate
x_known_1 = float(input(f'{"Enter the X coordinates of first known point":<{proportion - 5}} {"(m): "}'))  # First Known X Coordinate
pID_second = input(f'{"Enter the point ID of second known point":<{proportion - 2}} {": "}')  # Second PID
y_known_2 = float(input(f'{"Enter the Y coordinates of second known point":<{proportion - 5}} {"(m): "}'))  # Second Known Y Coordinate
x_known_2 = float(input(f'{"Enter the X coordinates of second known point":<{proportion - 5}} {"(m): "}'))  # Second Known X Coordinate
number_traverse = int(input(f'{"Enter the number of unknown traverse points":<{proportion - 2}} {": "}'))  # Number of Unknown Traverse

pID_list = [pID_first, pID_second]  # PID List
for i in range(1, number_traverse + 1):
    pID_unknown = input(f'{"Enter the point ID of unknown known point"} {i:<{proportion - 44}} {": "}')
    pID_list.append(pID_unknown)

# Same Point ID Exception
def Same_except(error_message):
    if error_message.lower() == 'y' or error_message.lower() == 'yes':
        print('Resuming...')
        pass
    else:
        sys.exit()
if len(pID_list) != len(set(pID_list)):
    print('\n'+'You Should Not Have Same Point ID' + '\n' + 'That Can Cause Conflict')
    error_message = input('Do You Want To Continue? (Not Recommended) (y/n): ')
    Same_except(error_message)
else:
    pass    

# Traverse Angles
angle_list = []  # Traverse Angle List
for j in range(1, len(pID_list) - 1):
    traverse_angle = float(input(f'{"Enter the traverse angle of"} {pID_list[j]:<{proportion - 36}} {"(grad): "}')) 
    angle_list.append(traverse_angle)

# Horizontal Distances
horizontal_list = []  # Horizontal Distance List
for k in range(1, len(pID_list) - 1):
    horizontal_distance = float(input(f'{"Enter the horizontal distance between"} {pID_list[k]} {"and"} {pID_list[k + 1]:<{proportion - (len(pID_list[k]) + 48)}} {"(m): "}'))
    horizontal_list.append(horizontal_distance)

#  ---  List Section ---
delta_y_list = []  # Delta Y List
delta_x_list = []  # Delta X List
coord_y_list = [y_known_1, y_known_2]  # Coordination Y List
coord_x_list = [x_known_1, x_known_2]  # Coordination X List
azimuth_list = []

# Distance Between Coordinates
delta_Y = y_known_2 - y_known_1  # Delta Y Value (FOR AZIMUTH)
delta_X = x_known_2 - x_known_1  # Delta X Value (FOR AZIMUTH)

# --- Azimuth Calculation Section ---
global first_azimuth
try:
    first_azimuth = (math.atan(abs(delta_Y / delta_X))) * 200 / math.pi  # First Azimuth
    #  First Azimuth Correction
    if delta_Y > 0 and delta_X > 0:
        first_azimuth = first_azimuth
    elif delta_Y > 0 and delta_X < 0:
        first_azimuth = 200 - first_azimuth
    elif delta_Y < 0 and delta_X < 0:
        first_azimuth = 200 + first_azimuth
    elif delta_Y < 0 and delta_X > 0:
        first_azimuth = 400 - first_azimuth
    elif delta_Y == 0 and delta_X >= 0:
        first_azimuth = 0
    elif delta_Y == 0 and delta_X < 0:
        first_azimuth = 200
except ZeroDivisionError:
    if delta_Y < 0:
        first_azimuth = 300
    elif delta_Y > 0:
        first_azimuth = 100
    else:
        first_azimuth = 0
        
azimuth_list.append(first_azimuth)

# K Value Calculation
for val in range(len(pID_list) - 2):
    k = azimuth_list[val] + angle_list[val]
    # K Value Correction
    if k < 200:
        k += 200
    elif 200 < k < 600:
        k -= 200
    elif k > 600:
        k -= 600
    azimuth_list.append(k)

# --- Delta Calculation Section ---
delta_y_list.append(0)
delta_x_list.append(0)
for val in range(1, len(azimuth_list)):
    d_y = horizontal_list[val - 1] * math.sin(azimuth_list[val] * math.pi / 200)  # Delta Y Value Between Two Point
    delta_y_list.append(d_y)
    d_x = horizontal_list[val - 1] * math.cos(
        azimuth_list[val] * math.pi / 200)  # Delta X Value Between Two Point
    delta_x_list.append(d_x)

# --- Coordinate Calculation Section ---
for val in range(len(pID_list) - 2):
    coord_y = coord_y_list[val + 1] + delta_y_list[val + 1]  # Coordinate Delta Y
    coord_y_list.append(coord_y)
for val in range(len(pID_list) - 2):
    coord_x = coord_x_list[val + 1] + delta_x_list[val + 1]  # Coordinate Delta X
    coord_x_list.append(coord_x)
    
# --- Output Section ---
# It is recommended that you use a minimum 75X35 tab for the proper notation.
# First Calculation
first_calc_title = f'{"Point ID":<10} {"Point ID":<10} {"Azimuth":<10} {"Delta Y":<10} {"Delta X"}'
print('\n' + first_calc_title + '\n' + ('-' * len(first_calc_title)))
for i in range(len(azimuth_list)):
    azimuth_calculations = f'{pID_list[i]:<10} {pID_list[i + 1]:<10} {format(azimuth_list[i], ".4f"):>8}'
    delta_calculations = f'{format(delta_y_list[i], ".2f"):>10} {format(delta_x_list[i], ".2f"):>10}'
    if delta_calculations == f'{format(delta_y_list[0], ".2f"):>10} {format(delta_x_list[0], ".2f"):>10}':
        print(azimuth_calculations + '')
    else:
        print(azimuth_calculations + delta_calculations)
print(('-' * len(first_calc_title)))
# Second Calculation
second_calc_title = f'{"Point ID":<11} {"Coordinate(Y)":<16} {"Coordinate(X)"}'
print(second_calc_title + '\n' + ('-' * len(second_calc_title)))
for i in range(2, len(pID_list)):
    coordinate_calculations = f'{pID_list[i]:<11} {format(coord_y_list[i], ".2f"):<16} {format(coord_x_list[i], ".2f")}'
    print(coordinate_calculations)
print(('-' * len(second_calc_title)))
