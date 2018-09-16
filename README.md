# **Advanced Lane Finding Project Report**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/original_undistored.jpg "Original and Undistorted Images"
[image2]: ./output_images/original_undistored_thresholded.jpg "Undistored Thresholded Image"
[image3]: ./output_images/undistored_perpsective_points.jpg "Source & Destination points for perspective tranform"
[image4]: ./output_images/lines_orig_udist.jpg "Source and Destination point verification"
[image5]: ./output_images/warped_unwarped.jpg "Warp & Unwarped Images"
[image6]: ./output_images/lanes_detection.jpg "Lane detections"
[video1]: ./output_video.mp4 "Video"

## Implementation

This project was implemented using the `lane_finding.ipynb` jupyter notebook . The resulting images can be found under the test images folder. The resulting videos can be found under the root folder.

## 1. Camera Calibration

The code for this step is contained in the first section of the IPython notebook `lane_finding.ipynb`. The images used for calibration were loaded from the camera_cal folder using the glob library. By visual observation, the number of corners was found to be 9,6 for each the calibration images. An array of 3D object points was prepared `objpoints`, using `numpy.mgrid()`, for the x,y coordinates and assuming that z=0 i.e. the chessboard is fixed on the (x,y) plane. The (x, y, z) points will represent the coordinates of the chessboard corners in the world. Using OpenCV's `findChessboardCorners()` for each one of the calibration images, the actual image points where detected. In order to confirm the validity of our detected points, `cv2.drawChessboardCorners()` was used to display them.
In order to calculate the camera calibration and distortion coefficients, the function `cv2.calibrateCamera()` was used. Subsequently, distorsion correction was perfomed using the function `cv2.undistort()`, to undistort all the images in the test_images folder. The resulting images can be found under the output_images folder.  Here is a comparison of the result for one of the test images.

![alt text][image1]

The camera calibration and distortion coefficients were stored in a pickle file, `camera_matrix.p`.

## 2. Image Thresholding

The various thresholding method are implemented in the section 2 of the IPython notebook. Several different algorithms for image thresholding where explored and various parameters were tested to improve the final result.

* Gradient thresholding in `abs_sobel_thresh()`
* Magnitude of gradients in `mag_thresh()`
* Direction of gradients in `dir_threshold()`
* HLS thresholding in `hls_select()`
* Combined in `combined_threshold()`

The combined methond included all gradient thresholding in the x direction along with the other four methods. The result of applying this method in an undistorted image can be seen in the figure below:

![alt text][image2]

## 2.1 Perspective transform

The implementation for the perspective transform can be found within the function `perspective_transform()`, in section 2.1 of the IPython Notebook. The function uses a set of source and destination points, for the given input image and `cv2.getPerspectiveTransform()` to calculate the transformation matrix. The inverse transformation matrix was obtained using `cv2.getPerspectiveTransform()`. The source and destination points were selected using the following formula:

```python
src = np.float32(
    [[(img_size[0] / 2) - 55, img_size[1] / 2 + 100],
    [((img_size[0] / 6) - 10), img_size[1]],
    [(img_size[0] * 5 / 6) + 60, img_size[1]],
    [(img_size[0] / 2 + 55), img_size[1] / 2 + 100]])
dst = np.float32(
    [[(img_size[0] / 4), 0],
    [(img_size[0] / 4), img_size[1]],
    [(img_size[0] * 3 / 4), img_size[1]],
    [(img_size[0] * 3 / 4), 0]])
```

This resulted in the following source and destination points:

| Source        | Destination   |
|:-------------:|:-------------:|
| 585, 460      | 320, 0        |
| 203, 720      | 320, 720      |
| 1127, 720     | 960, 720      |
| 695, 460      | 960, 0        |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image:

![alt text][image3]

Then i drew a line on the original, then undistorted and a warped image to verify that the lines appear parallel:

![alt text][image4]

Using these two matrices, a warped and unwarped version of the thresholded images was obtained using `cv2.warpPerspective()` and `cv2.warpPerspective()` respectively:

![alt text][image5]

## 3. Lane Detection

Lane detection is implemented in section 3 of the IPython Notebook, using two distinct functions. When the algorithm is executed for the first time or the lane needs to be re-detected without taking into account any previous detections, `find_lane_pixels()` is used. This method takes a binary thresholded image as an input and returns the left and right lane pixel positions. The state of each line is stored using class `Line()`. The Line class implementation can be found in `Line.py`. Two instansiations of this class are needed, one for the left and one for the right lane. Once we detect the pixels for each line, `fit_polynomial()` is used to fit a polynomial. Here is the result of `find_lane_pixels()` and `fit_polynomial()`:

![alt text][image6]

When the lane has already been detected, `search_around_poly()` is used to increase efficiency.

### 3.1 Curvature calculation

The implementation of curvature calculation  can be found in section 3.1 of the IPython Notebook, within the `measure_curvature_real()` method. The calculation for the vehicle offset is implemented within `vehicle_offset()`.

### 3.2 Detection pipeline

The detection pipeline is implemented within `detect_lane()`. During the initial state `find_lane_pixels()` is used while `search_around_poly()` is used if the lines where already detected. Once the lane pixels are found `fit_polynomial()` is used to fit an appropriate polynomial. Then the curvature is measured and the offset from the center is calculated.
Overlaying the result is done using two functions. `overlay_img()` which draws the offset and `label_img()` that adds the required labels for offset and average curvature. The resulting video can be seen here ![here][video1]:

[![LaneDetector](https://i.ytimg.com/vi/hK7WGtM3uw0/3.jpg)](https://www.youtube.com/embed/hK7WGtM3uw0)

## 4. Discussion

The algorithm performed as expected on the project_video, but the results were not so good on the advanced challenges. In the case of the challenge video, the shadow to left of the left line, is mistakenly identified as the actuall line. More experimentation, on the parameters for thresholding might solve this issue. On the harder challenge, the problem is that the line excibits curve on both ends, at opposite directions. Therefore, the algorithm, sometimes fail to fit a polinomial. This can be fixed if someone was to used an average fit value instead of the actual fit value.
