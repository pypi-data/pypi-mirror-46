Python Library to Read and Write Surface Files in Freesurfer's TriangularSurface Format

compatible with Freesurfer's MRISwriteTriangularSurface()
https://github.com/freesurfer/freesurfer/blob/release_6_0_0/include/mrisurf.h#L1281
https://github.com/freesurfer/freesurfer/blob/release_6_0_0/utils/mrisurf.c
https://raw.githubusercontent.com/freesurfer/freesurfer/release_6_0_0/utils/mrisurf.c

Freesurfer
https://surfer.nmr.mgh.harvard.edu/

Edit Surface File
>>> from freesurfer_surface import Surface, Vertex, Triangle
>>>
>>> surface = Surface.read_triangular('bert/surf/lh.pial'))
>>>
>>> vertex_a = surface.add_vertex(Vertex(0.0, 0.0, 0.0))
>>> vertex_b = surface.add_vertex(Vertex(1.0, 1.0, 1.0))
>>> vertex_c = surface.add_vertex(Vertex(2.0, 2.0, 2.0))
>>> surface.triangles.append(Triangle((vertex_a, vertex_b, vertex_c)))
>>>
>>> surface.write_triangular('somewhere/else/lh.pial')

List Labels in Annotation File
>>> from freesurfer_surface import Annotation
>>>
>>> annotation = Annotation.read('bert/label/lh.aparc.annot')
>>> for label in annotation.labels.values():
>>>     print(label.index, label.hex_color_code, label.name)

Find Border of Labelled Region
>>> surface = Surface.read_triangular('bert/surf/lh.pial'))
>>> surface.load_annotation_file('bert/label/lh.aparc.annot')
>>> region, = filter(lambda l: l.name == 'precentral',
>>>                  annotation.labels.values())
>>> print(surface.find_label_border_polygonal_chains(region))

