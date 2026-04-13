def linear_map(x, in_min, in_max, out_min, out_max):
    displaced_input = (x - in_min) 
    conversion_factor = (out_max - out_min) / (in_max - in_min)
    return displaced_input * conversion_factor + out_min

def clamp(x, min_val, max_val):
    return max(min_val, min(x, max_val))