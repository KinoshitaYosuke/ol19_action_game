import cv2
import numpy as np

def main():

    i = 0      # カウント変数
    th = 30  # 差分画像の閾値
    x0=0
    y0=0
    w0k=0
    h0k=0
    flag=0
    #保存
    #fmt = cv2.VideoWriter_fourcc(*'MJPG')
    #writer = cv2.VideoWriter('outtest2.avi', fmt, 30.0, (640, 480))

    # カメラのキャプチャ
    #cap = cv2.VideoCapture("output_02.avi")
    cap = cv2.VideoCapture(0)
    # 最初のフレームを背景画像に設定
    bg=makebg(cap)
    while(cap.isOpened()):
        ret,frame = cap.read()
        mask=subtraction(ret,frame,bg,th)
        if cv2.waitKey(10) & 0xFF == ord('w'): #輪郭抽出開始
            flag=1
            x0,y0,w0k,h0k=rinkaku(mask)
        if flag==1:
            key=kenshutsu(mask,x0,y0,w0k,h0k)
            print(key)
        # qキーが押されたら途中終了
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    #print(bg)
    # グレースケール変換
    #bg = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)
    #bg = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
    #ret,bg=cap.read()

def rinkaku(img):
    #imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img, 127, 255, 0)
    
    label = cv2.connectedComponentsWithStats(thresh)
    # オブジェクト情報を項目別に抽出
    n = label[0] - 1
    data = np.delete(label[2], 0, 0)
    center = np.delete(label[3], 0, 0)    
    min_x, min_y, max_w, max_h = Calculate_Player_Region(n, data)


    #x, y, w, h = cv2.boundingRect(cnt)
    
    #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    #return (x,y,w,h)

    #cv2.rectangle(img,(min_x,min_y),(max_w,max_h),(0,255,0),2)
    return (min_x,min_y,max_w - min_x,max_h - min_y)

def Calculate_Player_Region(n, data):
    min_x, min_y, max_w, max_h = 1000, 1000, 0, 0
    for i in range(n):
        if min_x > data[i][0]:
            min_x = data[i][0]
        if min_y > data[i][1]:
            min_y = data[i][1]
        if max_w < data[i][0] + data[i][2]:
            max_w = data[i][0] + data[i][2]
        if max_h < data[i][1] + data[i][3]:
            max_h = data[i][1] + data[i][3]

    return min_x, min_y, max_w, max_h

def Opening(img):
    kernel = np.ones((7,7),np.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return opening

def kenshutsu(img,x0,y0,w0k,h0k): #ここでイメージのパスをうけとる
        
    x, y, w, h = rinkaku(img)
    
    #if (h <= 3*h0k/4):
    #    return -1
    if ((y0-y) > h0k/8):
        return 1
    else:
        return 0
def makebg(cap):
    ret, bg = cap.read()
    return bg

def subtraction(ret, frame, bg,th):
    
        # フレームの取得
        #et,frame = cap.read()
        #cv2.imshow("Frame",frame)
        # グレースケール変換
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #ray = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
        #print(gray)
        # 差分の絶対値を計算
        
        b = cv2.absdiff(frame[:,:,0],bg[:,:,0])
        g = cv2.absdiff(frame[:,:,1],bg[:,:,1])
        r = cv2.absdiff(frame[:,:,2],bg[:,:,2])
        #mask = cv2.absdiff(gray, bg)
        # 差分画像を二値化してマスク画像を算出
        #mask[mask < th] = 0
        #mask[mask >= th] = 255
        g[g < th] = 0
        g[g >= th] = 1
        r[r < th] = 0
        r[r >= th] = 1
        b[b < th] = 0
        b[b >= th] = 1
        mask=g+r+b
        mask[mask == 0]=0
        mask[mask != 0]=255
        frame[mask==0]=0

        #Opening処理
        mask = Opening(mask)

        # フレームとマスク画像を表示
        
        #if ret==True:
            #frame = cv2.flip(frame,0)
            # write the flipped frame
            #mask=cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
            #writer.write(mask)
            #cv2.imshow("Mask", mask)
            #cv2.imshow("Result", frame)

        return mask
        #i += 1    # カウントを1増やす
        
        # 背景画像の更新（一定間隔）
        #if(i > 30):qqqqqqqqq
        #    ret, bg = cap.read()
            #bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
        #    i = 0 # カウント変数の初期化
            
        
    #cap.release()
    #cv2.destroyAllWindows()


if __name__ == '__main__':
    main()