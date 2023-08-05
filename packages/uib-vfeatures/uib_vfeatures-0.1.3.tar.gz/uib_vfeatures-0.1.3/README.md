# UIB - V Features

## Introduction 

*UIB - V Features* provide a set of useful features. With three types of features: morphological, texture 
and color. All the features can be used with mask or with the contours. Every feature is a numerical value 
that used in ML can improve their results. 
 
The morphological features are all grouped in one iterator, so you can calculate all the features inside 
a loop easily.

The library use mask and contours. Masks are two value image, where the object has a value diferent than the rest of 
the image. A contour is a 2D vector of points that define a contour. To calculate a contour normally is used the OpenCV
function.

### Installation

Install the library is very simple with pip

```
pip install uib-vfeatures
``` 

---
## List of features

### Morphological

#####All this features are in the iterator

*   Solidity
*   Convex hull perimeter
*   Convex hull area
*   Bounding box area
*   Rectangularity
*   Minor radius
*   Maximum radius
*   Feret
*   Breadh
*   Circularity
*   Roundness
*   Feret Angle
*   Eccenctricity
*   Center
*   Sphericity
*   Aspect Ratio
*   Area equivalent diameter
*   Perimeter equivalent diameter
*   Equivalent elipse area
*   Compactness
*   Area
*   Convexity
*   Shape
*   Perimeter

### Color

*   Mean of the LAB channels
*   Mean of the RGB channels
*   Mean of the HSV channels
*   Standard deviation of the LAB channels
*   Standard deviation of the RGB channels
*   Standard deviation of the HSV channels


### Textures

The texture features depends on the parameter of a unique function. The first two parameter define the texture,
with the distance and the angle of the texture. The third defines the feature to extract and the last one is 
a grey-scale image.

#### Texture features

+   Contrast
+   Dissimilarity
+   Homogeneity
+   ASN
+   Energy
+   Correlation

---

## Demo

We're going to use our library with a mask image .

```python
from uib_vfeatures.masks import Masks
from uib_vfeatures import Features_mask as ftrs
import cv2

```
First of all we read the image from a file, then we try our features with visualizations. We only have 
three features with visualization: the bounding box area, the eccentricity and the solidity. 

```python
mask = cv2.imread("mask.jpg")

Masks.bounding_box_area(mask, True)

Masks.eccentricity(mask, True)
Masks.solidity(mask, True)
```

### Iterator

You can use an iterator and implement every morpholical feature. 

```python
features = {}

for key, func in features.items():
    features[key] = func(mask)

```
As a result we had a dicctionary of the form *{'Feature_name': value}*
