import vidstab
import cv2
import time

# Create a VidStab object
stabilizer = vidstab.VidStab()
vidcap = cv2.VideoCapture('C:/Users/Admin/Videos/videoplayback.mp4')

# Get video properties (width, height, frames per second, etc.)
frame_width = int(vidcap.get(3))
frame_height = int(vidcap.get(4))
fps = int(vidcap.get(cv2.CAP_PROP_FPS))
out_filename = 'C:/Users/Admin/Videos/stabilized_video.mp4'

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(out_filename, fourcc, fps, (frame_width, frame_height))

# Create a new window to display the stabilized video
cv2.namedWindow('Stabilized Video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Stabilized Video', frame_width, frame_height)

prev_frame_time = 0

while True:
    grabbed_frame, frame = vidcap.read()

    if frame is not None:
        # Display the original frame
        cv2.imshow("Original", frame)

        # Perform stabilization
        # Start timer
        start_time = time.time()
        stabilized_frame = stabilizer.stabilize_frame(input_frame=frame, smoothing_window=20)
        # End time
        end_time = time.time()

        # Calculate the runtime
        runtime = end_time - start_time
        print(f"Runtime: {runtime:.5f} seconds")



        # Resize stabilized frame to match the original frame size
        stabilized_frame = cv2.resize(stabilized_frame, (frame_width, frame_height))

        # Display the stabilized frame in the 'Stabilized Video' window
        cv2.imshow('Stabilized Video', stabilized_frame)

        # Wait for the same duration as the stabilization time to synchronize frames
        wait_time = int((1 / fps) * 1000)  # Convert to milliseconds
        current_time = time.time()
        if prev_frame_time == 0:
            prev_frame_time = current_time
        time_elapsed = current_time - prev_frame_time
        prev_frame_time = current_time
        delay_time = wait_time - int(time_elapsed * 1000)
        if delay_time > 0:
            cv2.waitKey(delay_time)
        else:
            cv2.waitKey(1)

        # Press 'q' to exit the loop and stop writing the video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        # Break the loop when the video reaches the end
        break

# Release the VideoCapture and VideoWriter objects
vidcap.release()
out.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
