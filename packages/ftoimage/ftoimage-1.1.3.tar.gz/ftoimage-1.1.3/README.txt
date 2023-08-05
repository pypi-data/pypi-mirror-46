Uses the **pdf2image** library and code from this [answer](https://stackoverflow.com/questions/29760402/converting-a-txt-file-to-an-image-in-python)
to convert files to jpg and returns the path

Can be imported with

```commandline
import file_to_image
```

Can be used with
```python
from file_to_image import convert_to_image
path = "Where your file is"
jpg_path = convert_to_image(path)
```


