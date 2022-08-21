# ASCII ART 2020
![SPARC_final](https://user-images.githubusercontent.com/100084401/185801541-fbf20921-9f3c-4da6-9bd7-7122d3c7a691.png)
<br/><br/>
---

## How can I use it?
Specify the image path, output name, theme color and output size and run it. If no argument is provided, the default value is used.<br/>
```
python ASCII.py --image_path SPARC_ext.jpg --output_name SPARC_result --theme_color 2 71 254 --output_size 180 120
```

You can also enter the following command for more detailed settings:
```
python ASCII.py --image_path SPARC_ext.jpg --bright_path sort_bright.pickle --output_name SPARC_result --output_mode text --theme_color 2 71 254 --output_size 180 120
```


### Arguments
**output_mode** <br/>
By specifying the *output_mode* argument as 'text' or 'image', you can determine the format of the result. When set to 'text', the result is:
<p align="center">
<img width="672" alt="image" src="https://user-images.githubusercontent.com/100084401/185803140-a2388ae6-a880-4830-9660-513a6c845ae5.png">
</p>
If your .txt file looks garbled, it could be a font issue. Use a monospaced font such as **Consolas**.<br/>
<br/><br/>

**Theme color**<br/>
You can specify **at most one** theme color.<br/>
Theme color is not applied in text mode. In Image mode, only black and theme color are used for output.
It takes three integers in RGB format as input, and if there is no input, the output is all black. 
Internally, the inner product of the color is calculated and the theme color is used when the *threshold* value is exceeded. 
If you want to increase the level at which the theme color is used, set the *threshold* to a lower value.
<p align="center">
<img width="719" alt="image" src="https://user-images.githubusercontent.com/100084401/185803288-3434bb1c-01b9-46a6-bdb9-ebbf5e66f618.png">
</p>

---

## How does it work?
*Garage_ASCII.ipynb* automatically generates an 'ASCII palette' and calculates the average value of these pixels to calculate the average brightness of each ASCII character.<br/>
<p align="center">
<img width="765" alt="image" src="https://user-images.githubusercontent.com/100084401/185803486-5e5a0a4a-37c3-4e65-9be9-6da9fcb40dcf.png">
</p>
A linear calibration process is applied to the sorted brightness list to shift the color distribution to match the actual image.<br/>
<p align="center">
 <img width="800" alt="image" src="https://user-images.githubusercontent.com/100084401/185803549-864fdcda-e916-43b8-ac7e-ee6532b873e3.png">
</p>
Finally, the pixels in the image to be converted are compared against the list of calibrated brightnesses to find and place matching ASCII characters.<br/>

See *Garage_ASCII.ipynb* for more detail.

<br/>
<br/>
<br/>
© 2020 jun-pac [skg4078@snu.ac.kr]
