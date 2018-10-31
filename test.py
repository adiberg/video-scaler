# from producer import video_emitter
import argparse
import os
import re
import subprocess
from decimal import Decimal


# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def test():
    (path, num_splits, seconds) = parse_options()
    if num_splits <= 0:
        print("Number of instances must be greater than 0")
        raise SystemExit

    process = subprocess.Popen(['ffmpeg', '-i', path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()
    matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout,
                        re.DOTALL).groupdict()
    if matches:
        duration = (Decimal(matches['hours']) * 60 * 60) + (Decimal(matches['minutes']) * 60) + (
        Decimal(matches['seconds']))  # duration of the media file
        print("Video length in seconds: {}".format(duration))
    else:
        print("Can't determine video length.")
        raise SystemExit

    dir_name = path.split('.')[0] + "_chunks"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)  # creating directory to save the chunks of the media file

    split_length = duration / float(num_splits)
    total_sec = duration
    from_time = 0
    file_no = 1
    file_names = path.split('.')[0] + '_'
    while total_sec > 0:
        # In case if you want the chunks of the file to be in other formats then you can change 'mp4'
        # to the required audio or video format.
        os.system('ffmpeg -ss ' + str(from_time) + ' -t 600 -i ' + path + ' ' + dir_name + '/' + file_names + str(
            file_no) + '.mp4')
        file_no += 1
        from_time = from_time + split_length
        total_sec = total_sec - split_length


def parse_options():
    # construct the argument parse and parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num-instances", dest="N", type=int,
                        help="# of instances of a video to resize")
    parser.add_argument("-s", "--seconds", dest="M", type=int,
                        help="# of seconds between scaling of video instances")
    parser.add_argument("-p", "--path", dest="path", type=str,
                        help="video path")

    args = parser.parse_args()

    if args.N and args.M and args.path:
        return args.path, args.N, args.M

    else:
        parser.print_help()
        raise SystemExit


if __name__ == '__main__':
    try:
        test()
    except Exception, e:
        print "Exception occured running main():"
        print str(e)
