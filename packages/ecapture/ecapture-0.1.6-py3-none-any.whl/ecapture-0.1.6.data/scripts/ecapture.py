from cv2 import *
import time
def capture(camera_index,name_of_window,save_name):
    cam = VideoCapture(camera_index)   # 0 -> index of camera
    if cam is None or not cam.isOpened():
       print('Warning: unable to open image source: ', camera_index)
       exit()
    s, img = cam.read()
    if s:    # frame captured without any errors
        if name_of_window != False:
            namedWindow(name_of_window)
            imshow(name_of_window,img)
            waitKey(0)
            destroyWindow(name_of_window)
        if save_name != False:
            imwrite(save_name,img) #save image

            
def vidcapture(camera_index,name_of_window,save_name,key_for_exit):
    #Capture video from webcam
    vid_capture = cv2.VideoCapture(camera_index)
    if vid_capture is None or not vid_capture.isOpened():
       print('Warning: unable to open image source: ', camera_index)
       exit()

    vid_cod = cv2.VideoWriter_fourcc(*'XVID')
    if save_name != False:
        output = cv2.VideoWriter(save_name, vid_cod, 20.0, (640,480))        
    
    while(True):
         # Capture each frame of webcam video
         ret,frame = vid_capture.read()
         cv2.imshow(name_of_window, frame) 
         if save_name != False:
             output.write(frame)
         # Close and break the loop after pressing "x" key
         if cv2.waitKey(1) &0XFF == ord(key_for_exit):
             break
    # close the already opened camera
    vid_capture.release()
    # close the already opened file
    if save_name != False:
        output.release()
    # close the window and de-allocate any associated memory usage
    cv2.destroyAllWindows()

    
def auto_vidcapture(camera_index,name_of_window,save_name,time_for_exit):
    #Capture video from webcam
    vid_capture = cv2.VideoCapture(camera_index)
    if vid_capture is None or not vid_capture.isOpened():
       print('Warning: unable to open image source: ', camera_index)
       exit()
    
    vid_cod = cv2.VideoWriter_fourcc(*'XVID')
    if save_name != False:
        output = cv2.VideoWriter(save_name, vid_cod, 20.0, (640,480))
    t = time_for_exit  
    while(True):
         # Capture each frame of webcam video
         ret,frame = vid_capture.read()          
         if save_name != False:
             output.write(frame)
         while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            time.sleep(1)
            t -= 1
         break
         break   
    # close the already opened camera
    vid_capture.release()
    # close the already opened file
    if save_name != False:
        output.release()
    # close the window and de-allocate any associated memory usage
    cv2.destroyAllWindows()    
def delay_imcapture(camera_index,name_of_window,save_name,delay_time):
    cam = VideoCapture(camera_index)   # 0 -> index of camera
    if cam is None or not cam.isOpened():
       print('Warning: unable to open image source: ', camera_index)
       exit()
    s, img = cam.read()
    time.sleep(delay_time)
    if s:    # frame captured without any errors
        if name_of_window != False:
            namedWindow(name_of_window)
            imshow(name_of_window,img)
            waitKey(0)
            destroyWindow(name_of_window)
        if save_name != False:
            imwrite(save_name,img) #save image    


