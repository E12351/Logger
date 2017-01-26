import numpy as np
# from matplotlib import pyplot as plt
import cv2

class Video(object):
    def save_video():
        cap = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = cv2.imread('1.jpg')
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        x = 0
        y = 0
        z = 0
        SPEED = 0

        MP1 = 0
        MP2 = 0
        MT1 = 0
        MT2 = 0

        I = 0
        V = 0
        P = 0
        T = 0

        AL = 100
        AR = 30

        # fourcc = cv.CV_FOURCC('D','I','V','X')#FourCC code for AVI format
        try:
            out = cv2.VideoWriter('output.avi', -1, 20.0, (640,550))
        except:
            pass

        while(cap.isOpened()):
            ret, frame = cap.read()
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if ret==True:
                # frame = cv2.flip(frame,1)
                frame = np.concatenate((frame, img), axis=0)
                # write the flipped frame
                frame = cv2.line(frame,(0,480),(640,480),(255,255,255),1) #---
                frame = cv2.line(frame,(0,550),(640,550),(255,255,255),1) #---
                frame = cv2.line(frame,(80,480),(80,550),(255,255,255),1) #||
                frame = cv2.line(frame,(250,480),(250,550),(255,255,255),1) #||
                frame = cv2.line(frame,(340,480),(340,550),(255,255,255),1) #||
                frame = cv2.line(frame,(510,480),(510,550),(255,255,255),1) #||
                frame = cv2.line(frame,(570,480),(570,550),(255,255,255),1) #||

                frame = cv2.rectangle(frame,(350,490),(350+AL,500),(0,255,0),10) #[]
                frame = cv2.rectangle(frame,(350,520),(350+AR,530),(0,255,0),10) #[]


                frame = cv2.circle(frame,(605,515), 30, (255,255,255), -1)# o
                frame = cv2.circle(frame,(605,515), 5, (0,10,10), -1)# o


                frame = cv2.putText(frame,'X = '+str(x),(3,495), font, 0.4,(255,255,255),0,cv2.LINE_AA)
                frame = cv2.putText(frame,'Y = '+str(y),(4,510), font, 0.4,(255,255,255),0,cv2.LINE_AA)
                frame = cv2.putText(frame,'Z = '+str(z),(3,525), font, 0.4,(255,255,255),0,cv2.LINE_AA)
                frame = cv2.putText(frame,'Speed = '+str(SPEED),(3,540), font, 0.4,(255,255,255),0,cv2.LINE_AA)

                frame = cv2.putText(frame,'M1 Power = '+str(MP1)+' kW',(90,495), font, 0.4,(255,255,255),0,cv2.LINE_AA)
                frame = cv2.putText(frame,'M2 Power = '+str(MP2)+' kW',(90,510), font, 0.4,(255,255,255),0,cv2.LINE_AA)
                frame = cv2.putText(frame,'M1 Temp  = '+str(MT1)+' C',(90,525), font, 0.4,(255,255,255),0,cv2.LINE_AA)
                frame = cv2.putText(frame,'M2 Temp  = '+str(MT2)+' C',(90,540), font, 0.4,(255,255,255),0,cv2.LINE_AA)

                frame = cv2.putText(frame,'I = '+str(I)+' A',(260,495), font, 0.4,(255,255,255),0,cv2.LINE_AA)
                frame = cv2.putText(frame,'V = '+str(V)+' V',(260,510), font, 0.4,(255,255,255),0,cv2.LINE_AA)
                frame = cv2.putText(frame,'P = '+str(P)+' kW',(260,525), font, 0.4,(255,255,255),0,cv2.LINE_AA)
                frame = cv2.putText(frame,'T = '+str(T)+' C',(260,540), font, 0.4,(255,255,255),0,cv2.LINE_AA)

                frame = cv2.putText(frame,str(AL),(460,500), font, 0.6,(255,255,255),0,cv2.LINE_AA)
                frame = cv2.putText(frame,str(AR),(460,535), font, 0.6,(255,255,255),0,cv2.LINE_AA)

                out.write(frame)

                cv2.imshow('frame',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        # Release everything if job is finished
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    if __name__ == '__main__':

        save_video()