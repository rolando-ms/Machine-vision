# Machine vision
Repository of the Machine vision lecture + Lab (1535382)

* The edge_detection script detects edges of a hardcoded name image located in the benchmark_imgs folder. The user can try out with any image but it is strongly recommended to run the script with a low res RGB picture due to the fact that the project is not yet optimized.

* The object_detection script detects objects from images with uniform and very discriminative colors.

* The linefitting script takes lists of points gathered by the object_detection module and determines the start and end point of the corresponding segments. It draws then the line segments with the openCV library. 

Some other modules used are located in subfolders.

The project was created and tested with the following programs and library versions:
* Python 2.7.5
* Pillow 2.2.1
* cmake 2.8.11.2
* Matplotlib 1.4.2
* Numpy 1.9.0
(All of them in 32 bits version)
