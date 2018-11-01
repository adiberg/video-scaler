# from producer import video_emitter
import argparse
from time import sleep
import imageio
from multiprocessing import Queue, Pool
from scaler_producer2 import resize
import threading
from utils import INSTANCE

NUM_WORKERS = 5


def worker(video, instance_idx):
    print(' emitting %s.....' % instance_idx)
    reader = imageio.get_reader(video, 'ffmpeg')
    metadata = reader.get_meta_data()

    # threads = []
    frame_idx = 0
    for frame in reader:
        msg = {"instance": "vid-instance%i" % instance_idx,
               "frame_num": frame_idx,
               "frame": frame}
        # send message to service
        resize(msg)
        # thread = threading.Thread(target=resize(msg))
        # thread.start()
        # threads.append(thread)
        if frame_idx % 10 == 0:
            print("sent instance %d, frame %d to service" % (instance_idx, frame_idx))
        frame_idx += 1

    # for t in threads:
    #     t.join()
    video.release()


def test():
    (video_path, repeat_counter, seconds) = parse_options()
    # Multiprocessing: Init input Queue and pool of workers
    # input_q = Queue(maxsize=repeat_counter)
    # pool = Pool(NUM_WORKERS, worker, (input_q))

    threads = []
    thread = threading.Thread(target=worker(video_path, 0))
    thread.start()
    threads.append(thread)

    count_read_instance = 1
    for i in range(1, repeat_counter):
        sleep(seconds)
        print("Sending video again")
        thread = threading.Thread(target=worker(video_path, i))
        thread.start()
        threads.append(thread)
        # input_q.put((video_path, i))
        count_read_instance += 1

        print("Read Instances reatio: %f.2" % (count_read_instance / repeat_counter))

    # When everything done, release the capture
    for t in threads:
        t.join()


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
