import cv2
import zbar
import Image
from barcode_scanner import BarcodeScanner


cap=cv2.VideoCapture(1)
scanner= BarcodeScanner()
codeScanner=zbar.ImageScanner()
codeScanner.parse_config("enable")


def start_capture():
    while(True):
        (grabbed, frame) = cap.read()
       
        box = scanner.detect_barcode(frame)

        cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)

        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY, dstCn=0)
        pil = Image.fromarray(gray)
        width, height = pil.size


        raw = pil.tobytes()
        image = zbar.Image(width, height, 'Y800', raw)
        codeScanner.scan(image)


        # extract results
        for symbol in image:
            # do something useful with results
            font = cv2.FONT_HERSHEY_SIMPLEX
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data

            if box != None:
                cv2.putText(frame, symbol.data, (box[0][0],box[0][1]), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow("Frame", frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__=="__main__":
    start_capture()
