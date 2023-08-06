#!/usr/bin/env python


def main():

    # ----- command-line args ------ #
    import argparse
    parser = argparse.ArgumentParser(description='Detect arctic cod grunts')
    parser.add_argument('-c', '--config', type=str, help='configuration file', default='config.txt')
    args = parser.parse_args()
    config_file = args.config
    
    # -------- user input -------- #
    user_input = open(config_file, 'r')
    input_dir = user_input.readline().strip()
    conf_cut = float(user_input.readline())
    user_input.close()

    print('Reading from: ', input_dir)


    # csv output header (RAVEN compatible)

    output_header = ',Selection,View,Channel,Begin Time (s),End Time (s),Channel,Begin Path,File Offset (s),Begin File,Detector Confidence\n'


    # -------- compute spectrograms -------- #

    sampling_rate=4000
    window_size=0.2
    step_size=0.02
    flow=80
    fhigh=1000

    import os

    db_path = os.path.join('cache','db.h5')
    cache_path = os.path.join('cache','log')

    db_exists = os.path.exists(db_path)

    if db_exists:
        # read cache
        cache = open(cache_path, 'r')
        _input_dir = cache.readline().strip()
        _sampling_rate = int(cache.readline())
        _window_size = float(cache.readline())
        _step_size = float(cache.readline())
        _flow = float(cache.readline())
        _fhigh = float(cache.readline())
        cache.close()
        # check if any settings have changed
        db_exists *= (input_dir == _input_dir)
        db_exists *= (sampling_rate == _sampling_rate)
        db_exists *= (window_size == _window_size)
        db_exists *= (step_size == _step_size)
        db_exists *= (flow == _flow)
        db_exists *= (fhigh == _fhigh)

    # create database, if it does not already exist
    if not db_exists:

        print('Creating database ...')

        from ketos.utils import ensure_dir
        ensure_dir(db_path)

        # create database
        from ketos.data_handling.database_interface import create_spec_database
        create_spec_database(output_file=db_path, input_dir=input_dir, annotations_file=None, sampling_rate=sampling_rate, window_size=window_size, step_size=step_size, flow=flow, fhigh=fhigh, progress_bar=True, duration=60, tpadmax=0.5)

        # cache settings
        cache = open(cache_path, 'w')
        cache.write(input_dir+'\n')
        cache.write('{0}\n'.format(sampling_rate))
        cache.write('{0}\n'.format(window_size))
        cache.write('{0}\n'.format(step_size))
        cache.write('{0}\n'.format(flow))
        cache.write('{0}\n'.format(fhigh))
        cache.close()


    # -------- load CNN -------- #

    from ketos.neural_networks.cnn import BasicCNN

    cnn_exists = os.path.exists('cnn')
    if cnn_exists:
        d = 'cnn'
    else:
        import sys
        d = sys.path[0]
        d = os.path.dirname(d)

        # Windows Anaconda special case
        i = d.rfind('Scripts')
        if i != -1:
            d = d[:i]

        print('Detector configuration: ',d)

        d = os.path.join(d,'config','arctic-cod-detector')

    cnn = BasicCNN(image_shape=(50, 185))
    cnn.load(saved_meta=os.path.join(d,'cnn.meta'), checkpoint=os.path.join(d), reset=False)



    # -------- make predictions -------- #

    import tables
    import numpy as np
    import ketos.data_handling.database_interface as di
    from ketos.audio_processing.audio_processing import append_specs
    from ketos.neural_networks.neural_networks import class_confidences, predictions
    from ketos.audio_processing.audio_processing import make_frames

    # output file
    output = open('detections.csv', 'w')
    output.write(output_header)
    counter = 0
    t_offset = 0

    # open database file
    f = tables.open_file(db_path, 'r') 
    tbl = f.get_node('/', 'spec') 
    N = tbl.nrows

    print('Searching for arctic cod grunts ...')

    # loop over entries
    from tqdm import tqdm
    for i in tqdm(range(N)):   

        # load spectrogram     
        spec = di.load_specs(tbl, [i])[0]

        # split into 1 second wide frames with 50% overlap
        specs = spec.segment(length=1.0, overlap=0.50, progress_bar=False)

        # reduce tonal noise
        for s in specs:
            s.tonal_noise_reduction() 

        # get matrices and labels
        x, y = list(), list()
        for s in specs:
            x.append(s.image)
            yvec = s.get_label_vector(1)
            label = int(np.sum(yvec) > 0)
            y.append(label)

        x = np.array(x) # transform to a numpy array
        y = np.array(y) # transform to a numpy array

        # compute classification weights, predictions and confidences
        weights = cnn.get_class_weights(x)
        pred = predictions(weights)
        confidences = class_confidences(weights)

        # only keep predictions with confidence > conf_cut
        detections = pred * (confidences > conf_cut)

        # detections
        detections = make_frames(detections, 2, 1, True)
        detections_start = np.logical_and(detections[:,0] == 0, detections[:,1] == 1)
        detections_stop = np.logical_and(detections[:,0] == 1, detections[:,1] == 0)

        # start and stop times
        start = np.argwhere(detections_start == True)
        stop = np.argwhere(detections_stop == True)
        for i in range(len(start)):
            i1 = start[i][0] + 1
            i2 = stop[i][0]
            s1 = specs[i1]
            s2 = specs[i2]        
            conf = confidences[i1]
            fid = s1.file_vector[0]
            fname = s1.file_dict[fid]
            start_time = round(s1.time_vector[0], 3)
            stop_time = round(s2.time_vector[-1] + s2.tres, 3)
            global_start_time = start_time + t_offset
            global_stop_time = stop_time + t_offset
            counter += 1
            full_path = input_dir + fname
            output.write('{0},Spectrogram,1,1,{1:.3f},{2:.3f},{3},{4:.3f},{5},{6:.4f}\n'.format(counter,global_start_time,global_stop_time,full_path,start_time,fname,conf))

        # global time
        t_offset += spec.duration()

    print('detections: ', counter)
    print('data saved to: ', output.name)

    # close files
    f.close()
    output.close()


if __name__ == '__main__':
   main() 
