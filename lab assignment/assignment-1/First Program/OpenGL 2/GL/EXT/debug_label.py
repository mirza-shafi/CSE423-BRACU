'''OpenGL extension EXT.debug_label

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.debug_label to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension defines a mechanism for OpenGL and OpenGL ES applications to 
	label their objects (textures, buffers, shaders, etc.) with a descriptive 
	string. 
	
	When profiling or debugging such an application within a debugger or 
	profiler it is difficult to identify resources from their object names. 
	Even when the resource itself is viewed it can be problematic to 
	differentiate between similar resources. Attaching a label to an object         
	helps obviate this difficulty.
	
	The intended purpose of this is purely to improve the user experience 
	within OpenGL and OpenGL ES development tools.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/debug_label.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.EXT.debug_label import *
from OpenGL.raw.GL.EXT.debug_label import _EXTENSION_NAME

def glInitDebugLabelEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# INPUT glGetObjectLabelEXT.label size not checked against bufSize
glGetObjectLabelEXT=wrapper.wrapper(glGetObjectLabelEXT).setInputArraySize(
    'label', None
).setInputArraySize(
    'length', 1
)
### END AUTOGENERATED SECTION