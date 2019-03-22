import cv2
import time
from Borkar_et_al import process_image
import tkinter as tk
from threading import Thread


VIDEO_OPTIONS = ["highway.mp4", "highway2.mp4", "highway_sunlight.mp4",
                 "highway_night.mp4", "night_traffic.mp4",
                 "night_with_bend.mp4", "shadows_and_road_markings.mp4",
                 "shadows_and_traffic.mp4"]
VIDEO_THREAD_RUNNING = True
cap = None
fps_count = 0


def main():
    setup_gui()


def setup_gui():
    global video_string
    gui = tk.Tk()
    gui.title("Lane Detection Menu")

    # List of test video options
    video_string = tk.StringVar(gui)
    video_string.set(VIDEO_OPTIONS[0])
    options = tk.OptionMenu(gui, video_string, *VIDEO_OPTIONS)
    options.pack()

    button = tk.Button(gui, text="Select", command=setup_video_thread)
    button.pack()

    tk.mainloop()


def setup_video_thread():
    global cap
    global VIDEO_THREAD_RUNNING
    try:
        if cap is None:
            VIDEO_THREAD_RUNNING = True
            video_thread = Thread(target=setup_video)
            video_thread.start()
        else:
            VIDEO_THREAD_RUNNING = False
            thread_ready = False
            while not thread_ready:
                if VIDEO_THREAD_RUNNING:
                    thread_ready = True
                    video_thread = Thread(target=setup_video)
                    video_thread.start()
    except Exception as e:
        print(e)


def setup_video():
    global fps_count
    global cap
    global VIDEO_THREAD_RUNNING

    selection = video_string.get()
    cap = cv2.VideoCapture("C:\\Users\\Brian\\Desktop\\test_videos\\BDD\\"+selection)
    num_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    cv2.namedWindow("Video Stream")
    cv2.createTrackbar("Video Slider", "Video Stream", 0, num_of_frames, trackbar_update)

    if not cap.isOpened:
        print("Error opening video stream")
        exit(1)

    frames = []
    while True:

        if VIDEO_THREAD_RUNNING is False:
            VIDEO_THREAD_RUNNING = True
            cap = None
            cv2.destroyAllWindows()
            print("Exiting thread.")
            return

        start_time = time.time()
        selection = video_string.get()
        fps_count += 1

        ret, frame = cap.read()
        frames.append(frame)
        if len(frames) == 4:
            del frames[0]

        if ret:
            # for f in frames:
            #     frame = cv2.addWeighted(frame, 1, f, 1, 0)
            processed_view = process_image.process(frame, selection=selection)
            cv2.imshow('Video Stream', processed_view)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        else:
            frames = []
            cap = cv2.VideoCapture("C:\\Users\\Brian\\Desktop\\test_videos\\BDD\\"+selection)

        # if fps_count == 300:
        #    cv2.imwrite("C:\\Users\\Brian\\Desktop\\test_videos\\project_images\\hist_eq_original.jpg", processed_view)
        print("FPS: ", 1.0 / (time.time() - start_time))


def trackbar_update(self):
    cap.set(cv2.CAP_PROP_POS_FRAMES, cv2.getTrackbarPos("Video Slider", "Video Stream"))


if __name__ == "__main__": main()