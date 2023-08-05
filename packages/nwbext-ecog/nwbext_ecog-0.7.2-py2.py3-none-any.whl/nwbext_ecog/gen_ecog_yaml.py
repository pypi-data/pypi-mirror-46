from pynwb.spec import NWBDatasetSpec, NWBNamespaceBuilder, NWBGroupSpec, NWBAttributeSpec

namespace = 'ecog'

ns_builder = NWBNamespaceBuilder(doc=namespace + ' extensions', name=namespace,
                                 version='1.2.1', author='Ben Dichter',
                                 contact='ben.dichter@gmail.com')

ns_builder.include_type('NWBDataInterface', namespace='core')
ns_builder.include_type('Subject', namespace='core')

surface = NWBGroupSpec(
    neurodata_type_def='Surface',
    neurodata_type_inc='NWBDataInterface',
    quantity='+',
    doc='brain cortical surface',
    datasets=[  # set Faces and Vertices as elements of the Surfaces neurodata_type
        NWBDatasetSpec(
            doc='faces for surface, indexes vertices', shape=(None, 3),
            name='faces', dtype='uint32', dims=('face_number', 'vertex_index')),
        NWBDatasetSpec(
            doc='vertices for surface, points in 3D space', shape=(None, 3),
            name='vertices', dtype='float', dims=('vertex_number', 'xyz'))],
    attributes=[
        NWBAttributeSpec(
            name='help', dtype='text', doc='help',
            value='This holds Surface objects')])

surfaces = NWBGroupSpec(
    neurodata_type_def='CorticalSurfaces',
    neurodata_type_inc='NWBDataInterface',
    name='cortical_surfaces',
    doc='triverts for cortical surfaces', quantity='?',
    groups=[surface],
    attributes=[NWBAttributeSpec(
        name='help', dtype='text', doc='help',
        value='This holds the vertices and faces for the cortical surface '
              'meshes')])

images = NWBGroupSpec(neurodata_type_inc='Images', doc="images of subject's brain",
                      name='images', quantity='?')

ecog_subject = NWBGroupSpec(
    neurodata_type_def='ECoGSubject',
    neurodata_type_inc='Subject',
    name='subject',
    doc='extension of subject that holds cortical surface data',
    groups=[surfaces, images]
)

ns_path = namespace + ".namespace.yaml"
ext_source = namespace + ".extensions.yaml"
ns_builder.add_spec(ext_source, ecog_subject)
ns_builder.export(ns_path)
