#! /usr/bin/env python

# Author: Konstantin Qew[erty] Evdokimenko (qewerty_Ы_gmail.com).
# The script is in public domain.
# Place the script into the ~/gimp-<version>/plug-ins and restart the GIMP

from gimpfu import *

def cut_into_layers(timg, tdrawable, rows=1, cols=1, order=1):
    al = timg.active_layer
    w = al.width
    h = al.height
    cols = int(cols)
    rows = int(rows)
    fw, fwmod = divmod(w, cols)
    fh, fhmod = divmod(h, rows)
    if fwmod != 0 or fhmod != 0:
        raise gimp.error("The active layer size isn't multiple of rows/cols")

    fw = int(fw)
    fh = int(fh)
    img = gimp.Image(fw, fh, RGB)
    img.disable_undo()

    frames = rows*cols
    index = 0

    def create_layer(index, r, c):
        l = gimp.Layer(img, '#' + str(index), fw, fh, al.type,
                       100, NORMAL_MODE)
        img.add_layer(l, index)
        pdb.gimp_rect_select(timg, fw*c, fh*r, fw, fh, CHANNEL_OP_REPLACE, False, 0)
        pdb.gimp_edit_copy(al)
        floating_sel = pdb.gimp_edit_paste(l, False)
        pdb.gimp_floating_sel_anchor(floating_sel)
        index += 1
        pdb.gimp_progress_update(float(index)/frames)
        return index

    if order == 0:
        for r in xrange(rows):
            for c in xrange(cols):
                index = create_layer(index, r, c)
    elif order == 1:
        for c in xrange(cols):
            for r in xrange(rows):
                index = create_layer(index, r, c)
    else:
        raise gimp.error("Invalid 'order' value: " + str(order))

    pdb.gimp_selection_none(timg)
    gimp.progress_update(1.0)

    img.enable_undo()
    gimp.Display(img)
    gimp.displays_flush()

register(
        'python_fu_cut_into_layers',
        'Cut an active layer into more layers',
        'Cut an active layer into more layers',
        'Konstantin Qew[erty] Evdokimenko',
        'Konstantin Qew[erty] Evdokimenko',
        '2010',
        '<Image>/Filters/Animation/_Cut into layers',
        'RGB*',
        [
            (PF_SPINNER, 'rows', 'Rows', 1, (1, 1000000, 1)),
            (PF_SPINNER, 'cols', 'Columns', 1, (1, 1000000, 1)),
            (PF_OPTION, 'order', 'Order', 1, ['Row-Major', 'Column-Major']),
        ],
        [],
        cut_into_layers)

main()
