name = "img2xlsx"

import xlsxwriter
from PIL import Image
import numpy as np
import string


class Img2Xlsx:
    def __init__(self, *args, **kwargs):
        self.letters = letters = sorted(list(set(string.ascii_letters.upper())))
    
    def columns_names(self, length):
        first = int((length - 1)/26)
        if first == 0:
            return self.letters[:length]
        else:
            al = self.letters + [i + j for i in self.letters[:first] for j in self.letters]
            return al[:length]

    def rgb2hex(self, orgin):
        rgbColorArray = list(orgin)
        output = "#"
        for x in rgbColorArray:
            intx = int(x)
            if intx < 16:
                output = output + '0' + hex(intx)[2:]
            else:
                output = output +  hex(intx)[2:]
        return output

    def run(self, img, xlsx):
        image = Image.open(img)
        image_array = np.array(image)
        h, w, _ = image_array.shape
        reimage = image.resize((w//3, h//3), Image.ANTIALIAS)
        reimage_array = np.array(reimage)
        h, w, _ = reimage_array.shape

        columns = self.columns_names(w)

        workbook = xlsxwriter.Workbook(xlsx)
        worksheet = workbook.add_worksheet()

        worksheet.set_column('A:%s' % columns[-1], 1.39)
        for i in range(h-1):
            worksheet.set_row(i, 12)

        for i, r in enumerate(list(range(1, h))):
            for j, l in enumerate(columns):
                cell_format = workbook.add_format()
                cell_format.set_pattern(1)
                cell_format.set_bg_color(self.rgb2hex(reimage_array[i, j]))
                worksheet.write('%s%s' % (l, r), '', cell_format)
        workbook.close()


img2xlsx = Img2Xlsx()