"""
The `ops` module contains a number of useful operations. These can be used to transform a loaded GLTF (in-place) in
various ways.

Use these like so:

```python
from gltf import GLTF
from gltf.ops import my_op

model = GLTF.load("input.glb")
my_op(model)  # These operate on the model in-place and return None
model.save("output.glb")
```
"""
import copy
from pprint import pprint

from PIL import Image as PImage

from gltf.buffers import Accessor


def merge_animations(model):
    """
    Merges the animations of the model into the first animation. This is useful when you have a bunch of individual
    animations that should be played simultaneously in a GLTF viewer.
    """
    anim = model.animations[0]
    for an in model.animations[1:]:
        anim.channels.extend(an.channels)
    model.animations = [anim]


def sample_textures_to_materials(gltf, min_x=0.83, min_y=0.95):
    """
    Remove the UVs from a portion of the mapping, and recreate those as single-color materials. This is useful to
    remove texture coordinates from geometry that doesn't need it.
    """
    from .materials import Sampler
    images = dict()
    colors = dict()

    for n in (n for n in gltf.nodes if n.mesh):
        for p in n.mesh.primitives:
            if p.material is None or not p.texcoords:
                continue

            texcoord_idx = 0 if p.material.color_uv is None else p.material.color_uv
            texcoords = p.texcoords[texcoord_idx]
            indices = p.indices.data if p.indices else list(range(texcoords.count))

            tex = p.material.color_texture or p.material.diffuse_texture
            if tex is None:
                continue
            sampler = tex.sampler or Sampler()
            if id(tex) not in images:
                images[id(tex)] = PImage.open(tex.source.get_fp())
            img = images[id(tex)]

            color = None
            for i in indices:
                point = texcoords.data[i]
                if point[0] < min_x and point[1] < min_y:
                    print(point)
                    break
                # Get the RGBA value for each point
                point = sampler.wrap_point(point)
                x = round((img.size[0] - 1) * point[0])
                y = round((img.size[1] - 1) * point[1])
                pixel = img.getpixel((x, y))
                if len(pixel) < 4:
                    pixel = list(pixel)
                    if len(pixel) == 1:
                        pixel *= 3
                    if len(pixel) == 3:
                        pixel.append(255)
                    else:
                        raise ValueError('Incorrect number of channels in pixel')

                pixel = tuple(pixel)
                if color is None:
                    print(pixel)
                    color = pixel
                if pixel != color:
                    print(pixel)
                    break
            else:
                # All texcoords mapped to the same color
                if color not in colors:
                    new_mat = copy.copy(p.material)
                    new_mat.base_color_factor = [(c/255) ** 2.2 for c in color]
                    new_mat.color_texture = None
                    new_mat.color_uv = None
                    new_mat.name = 'SampledTexture'
                    colors[color] = new_mat
                mat = colors[color]
                p.material = mat

                if texcoord_idx != 0 or len(p.texcoords) > 1:
                    p.texcoords = []
                    continue
                    raise NotImplementedError
                del p.texcoords[texcoord_idx]

    gltf.repair()


def print_analysis(model):
    """
    Prints a filesize analysis of the GLTF file.
    """
    _accessor_cache = set()

    def _size(accessor: Accessor):
        if id(accessor) in _accessor_cache:
            return 0
        else:
            _accessor_cache.add(id(accessor))

        n = accessor.data
        return n.size * n.itemsize

    def _primitive_extractor(path, prim, sizes):
        accessor = getattr(prim, path)
        if accessor is None:
            return

        if isinstance(accessor, list):
            many = accessor
            for accessor in many:
                sizes[path] += _size(accessor)
        else:
            sizes[path] += _size(accessor)

    def _format_bytes(byte_count):
        # 2**10 = 1024
        power = 2 ** 10
        n = 0
        powers = {0: '', 1: 'k', 2: 'M', 3: 'G', 4: 'T'}
        while byte_count > power:
            byte_count /= power
            n += 1
        return f'{round(byte_count, 1)} {powers[n]}B'

    sizes = {
        "positions": 0,
        "normals": 0,
        "tangents": 0,
        "texcoords": 0,
        "indices": 0,
        "animation_translation": 0,
        "animation_rotation": 0,
        "animation_scale": 0,
        "animation_timesamples": 0,
    }

    for mesh in model.meshes:
        for prim in mesh.primitives:
            _primitive_extractor("positions", prim, sizes)
            _primitive_extractor("normals", prim, sizes)
            _primitive_extractor("tangents", prim, sizes)
            _primitive_extractor("texcoords", prim, sizes)
            _primitive_extractor("indices", prim, sizes)

    for anim in model.animations:
        for channel in anim.channels:
            sizes["animation_" + channel.target_path] += _size(channel.sampler.output)
            sizes["animation_timesamples"] += _size(channel.sampler.input)

    # TODO: JSON data

    # TODO: Textures

    pprint({k: _format_bytes(sizes[k]) for k in sizes})
