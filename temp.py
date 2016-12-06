import os
with open(os.path.join(os.path.sep, "sys", "class", "thermal", "thermal_zone0", "temp"), 'r') as f:
    temp_string = f.readline()
    temp = int(temp_string) / 1000  # convert to celsius
print(temp)
