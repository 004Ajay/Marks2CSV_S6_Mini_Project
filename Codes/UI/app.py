from flask import Flask, render_template, request
import cv2
from PIL import Image
from predictions import return_dictonary
import tensorflow as tf
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/realtime', methods=['POST'])
def real_time():
    model = tf.keras.models.load_model("D:/AJAYMON/AJAY/Programming/S6_Mini_Project/Codes/Neural Network/MP_Latest_Model.h5")
    image_list = []
    dict_ret_df_lst = []

    def dataframe(dict_ret_df_lst):
        df = pd.DataFrame(dict_ret_df_lst[0])

        # Remove columns with all zeros
        df1 = df.loc[:, (df != 0).any(axis=0)]
        df1['Sum'] = df1.sum(1)

        df1.insert(0, 'Name', '') # Add empty colum, Name to left of df
        df1.insert(0, 'Roll No', '')
        return df1

    def capture_images():
        # Open the default camera (index 0)
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 250)
        while True:
            # Read the current frame from the camera
            ret, frame = cap.read()
            cv2.putText(frame, "Press \'Enter\' to capture image", (40, 310), cv2.FONT_ITALIC, 0.4, (50, 200, 255), 2)
            cv2.putText(frame, "Press \'ESC\' to quit", (40, 350), cv2.FONT_ITALIC, 0.4, (50, 200, 255), 2)

            # Display the frame in a window called "Real-time Image Capture"
            cv2.imshow("Real-time Image Capture", frame)

            # Wait for the user to press a key
            key = cv2.waitKey(1)

            # If the user presses the "ENTER" key (ASCII code 13) or spacebar 
            if key == 13 or key == 32:
                # Convert the captured frame to PIL image
                pil_image = Image.fromarray(frame)

                # Append the PIL image to the image list
                image_list.append(pil_image)

            # If the user presses the "ESC" key (ASCII code 27)
            elif key == 27:
                break

        # Release the camera and close the window
        cap.release()
        cv2.destroyAllWindows()
        return_dict = return_dictonary(image_list, model)
        dict_ret_df_lst.append(return_dict)
        final_dataframe = dataframe(dict_ret_df_lst)
        return final_dataframe

    # Call the capture_images() function
    data_frame = capture_images()
    return data_frame.to_csv(index=False)

if __name__ == '__main__':
    app.run(debug=True)
