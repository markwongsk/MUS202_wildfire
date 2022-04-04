# UTC | TIME | Radiant Heat | Convective Heat | Total Heat | Temperature | Vert Wind | Horiz Wind
def process_data():
    with open("../Downloads/firedata.csv") as f:
        # drop header
        return [line.strip().split(",") for line in f.readlines()][1:]

def aggregate(start, delta, data):
    """
    Takes in data, and uses a start index and a delta to aggregate
    all the delta rows after the start index into (len(data)-start)/buckets
    """
    aggregate = []
    for i in xrange(start, len(data), delta):
        aggregate_row = data[i][:2]
        for header in xrange(2, len(data[i])):
            total = 0
            bucket_size = min(len(data) - i, delta)
            for j in xrange(bucket_size):
                total += float(data[i+j][header])
            aggregate_row += [total * 1.0 / bucket_size]
        aggregate += [aggregate_row]
    return aggregate
                
def scale_pitch(y, pitch_range, weight=1):
    """
    Scales the given data points to the pitch range, zero-ing
    all points that belong to the smallest range, which by default
    occupies one point of the pitch range
    """
    print(y)
    hi = max(y)
    pitches = []
    for val in y:
        index = int((val*1.0/hi)*(len(pitch_range)+weight)) - weight
        if index < 0:
            pitches += [0]
            continue
        if index == len(pitch_range):
            # edge case, y is hi
            pitches += [pitch_range[-1]]
        else:
            assert(index < len(pitch_range))
            pitches += [pitch_range[index]]
    return pitches

def process_and_save_file(start, delta, data):
    lines = aggregate(start, delta, data)
    with open("wildfire_%d_%d.csv" % (start, delta), "w") as f:
        for line in lines:
            f.write(",".join([str(cell) for cell in line]) + "\n")

def process_and_save_pitches(start, delta, data):
    lines = aggregate(start, delta, data)
    discarded_buckets = 2
    num_pitches = 13
    pitches = scale_pitch([row[4] for row in lines], range(num_pitches+1)[1:], discarded_buckets)
    with open("pitches_%d_%d_%d_%d.csv" % (start, delta, num_pitches, discarded_buckets), "w") as f:
        for i in xrange(len(lines)):
            f.write(",".join([str(cell) for cell in lines[i]]) + "," + str(pitches[i]) + "\n")

def main():
    lines = process_data()
    #process_and_save_file(0, 50, lines)
    process_and_save_pitches(0, 50, lines)
    
if __name__ == "__main__":
    main()
