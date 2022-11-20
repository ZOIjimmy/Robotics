# Part A: Camera Calibration

![Alt text](docs/figure_1.png?raw=true)

This program uses images of chess board under `calibrate_src` directory to calibrate our camera. Images under the `calibrate_src`  and the `input` directory will be calibrated and saved in the `output` directory.

Some sample outputs are shown in `sample_output` directory.

## Team member (team16):
B09507016 鄭達郁

B09901058 邱奕翔

B09901060 王泓予

B09902037 薛尚齊

## How to run 
1, ```pip install opencv-python numpy```

2, ```python hw3_a.py```

3, Once start running, a window showing the calibrated image should pop up, press any key to see the next image.

4, The result will be saved in the output directory.

## Features
- The program checks that all images for calibrating the camera have the same aspect ratio, and resizes them to the same size.
<br>

- For images that are being calibrated, if their heights are greater than their widths, the program automatically rotate them 90 degrees to ensure optimal result.