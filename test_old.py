# from producer import video_emitter
import argparse
from scaler_producer_old import resize
from time import sleep

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def test():
    (path, repeat_counter, seconds) = parse_options()
    resize(path)
    for i in range(1, repeat_counter):
        sleep(seconds)
        print("Sending video again")
        resize(path)


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
    except Exception as e:
        print("Exception occured running main():")
        print(str(e))
