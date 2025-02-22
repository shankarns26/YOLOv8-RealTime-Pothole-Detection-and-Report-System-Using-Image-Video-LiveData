import cv2
import torch
from ultralytics.yolo.utils.plotting import Annotator, colors
from ultralytics.yolo.engine.predictor import BasePredictor

class LiveCameraDetectionPredictor(BasePredictor):

    def get_annotator(self, img):
        return Annotator(img, line_width=self.args.line_thickness, example=str(self.model.names))

    def preprocess(self, img):
        img = torch.from_numpy(img).to(self.model.device)
        img = img.half() if self.model.fp16 else img.float()  # uint8 to fp16/32
        img /= 255  # 0 - 255 to 0.0 - 1.0
        return img

    def postprocess(self, preds, img, orig_img):
        preds = ops.non_max_suppression(preds,
                                        self.args.conf,
                                        self.args.iou,
                                        agnostic=self.args.agnostic_nms,
                                        max_det=self.args.max_det)

        for i, pred in enumerate(preds):
            shape = orig_img[i].shape if self.webcam else orig_img.shape
            pred[:, :4] = ops.scale_boxes(img.shape[2:], pred[:, :4], shape).round()

        return preds

    def live_camera_detection(self):
        cap = cv2.VideoCapture(0)  # Open the webcam
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to read from camera.")
                break

            # Preprocess the frame
            img = self.preprocess(frame)
            img = img.unsqueeze(0)  # Add batch dimension

            # Inference
            preds = self.model(img)
            preds = self.postprocess(preds, img, frame)

            # Annotate frame
            annotator = self.get_annotator(frame)
            for pred in preds[0]:
                xyxy, conf, cls = pred[:4], pred[4], pred[5]
                label = f"{self.model.names[int(cls)]} {conf:.2f}"
                annotator.box_label(xyxy, label, color=colors(int(cls)))

            # Display the frame
            cv2.imshow('Live Camera Detection', annotator.result())

            # Exit on 'q' key or window close
            if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Live Camera Detection', cv2.WND_PROP_VISIBLE) < 1:
                break

        # Release resources
        cap.release()
        cv2.destroyAllWindows()
