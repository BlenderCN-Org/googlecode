/** \file core.h
 *  \brief Header file for core.c.

 <table>
 <tr><td>Project Name:                                   </td>
     <td><b>MakeHuman</b>                                </td></tr>
 <tr><td>Product Home Page:                              </td>
     <td>http://www.makehuman.org/                       </td></tr>
 <tr><td>SourceForge Home Page:                          </td>
     <td>http://sourceforge.net/projects/makehuman/      </td></tr>
 <tr><td>Authors:                                        </td>
     <td>Manuel Bastioni, Paolo Colombo, Simone Re       </td></tr>
 <tr><td>Copyright(c):                                   </td>
     <td>MakeHuman Team 2001-2009                        </td></tr>
 <tr><td>Licensing:                                      </td>
     <td>GPL3 (see also
         http://makehuman.wiki.sourceforge.net/Licensing)</td></tr>
 <tr><td>Coding Standards:                               </td>
     <td>See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards
                                                         </td></tr>
 </table>

 Header file for core.c.

 */

#ifndef CORE_H
#define CORE_H 1
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _DEBUG
  #undef _DEBUG
  #include <Python.h>
  #define _DEBUG
#else
  #include <Python.h>
#endif

#ifdef __cplusplus
extern "C" {
#endif

void RegisterObject3D(PyObject *module);

/*! \brief 3D object basic structure. */
/*!        3D object basic structure. */
typedef struct
{
    PyObject_HEAD
    int shadeless;              /**< \brief Whether this object is affected by scene lights or not.                     */
    unsigned int texture;       /**< \brief a texture id or 0 if this object doesn't have a texture.                    */
    int isVisible;              /**< \brief Whether this object is currently visible or not.                            */
                                /**<        An int defining whether this object is currently visible or not.            */
    int inMovableCamera;        /**< \brief Whether this object uses the Movable or Fixed camera mode.                  */
                                /**<        An int defining whether this object uses the Movable or Fixed camera mode.  */
    int isPickable;             /**< \brief Whether this object can be picked.                                          */
                                /**<        An int defining whether this object can be picked.                          */
    float location[3];          /**< \brief Tthe object location.                                                       */
                                /**<        Array of 3 floats defining the object location (x,y,z).                     */
    float rotation[3];          /**< \brief The object orientation.                                                     */
                                /**<        Array of 3 floats defining the object orientation (x, y and z rotations).   */
    float scale[3];             /**< \brief The object scale.                                                           */
                                /**<        Array of 3 floats defining the object size (x, y and z scale).              */
    int nVerts;                 /**< \brief The number of vertices in this object.                                      */
                                /**<        An int holding the number of vertices in this object.                       */
    int nTrigs;                 /**< \brief The number of faces in this object.                                         */
                                /**<        An int holding the number of triangular faces in this object.
                                            MakeHuman only supports triangular faces.                                   */
    int nNorms;                 /**< \brief The number of surface normals in this object.                               */
                                /**<        An int holding the number of surface normals defined for this object.       */
    int nColors;                /**< \brief The number of colors used in this object.                                   */
                                /**<        An int holding the number of colors used in this object.                    */
    int nColors2;               /**< \brief The number of colors used in this object.                                   */
                                /**<        An int holding the number of colors used in this object.
                                        <b>EDITORIAL NOTE: One of these may be for 'false' colors. Find out which.</b>  */
    int *trigs;                 /**< \brief The indices of faces in this object.                                        */
                                /**<        Three ints for each triangular face in this object.                         */
    float *verts;               /**< \brief Pointer to the start of the list of vertex coordinates.                     */
                                /**<        A pointer to an array of floats containing the list of vertex coordinates
                                            for each of the vertices defined for this object.
                                            The x, y and z coordinates for a single vertex are stored sequentially in
                                            this list.                                                                  */
    float *norms;               /**< \brief Pointer to the start of the list of surface normals.                        */
                                /**<        A pointer to an array of floats containing the list of surface normals
                                            defined for this object.
                                            The x, y and z components for a single normal are stored sequentially in
                                            this list.                                                                  */
    float *UVs;                 /**< \brief Pointer to the start of the list of UV vectors.                             */
                                /**<        A pointer to an array of floats containing the list of UV vectors used for
                                            texture mapping onto this object.
                                            The U and V components for a single vector are stored sequentially in
                                            this list.                                                                  */
    unsigned char *colors;      /**< \brief Pointer to the start of the list of color components.                       */
                                /**<        A pointer to an array of chars containing the list of color components
                                            defined for this object. Each color component takes a single byte and can
                                            have a value of 0-255.
                                            The Red, Green and Blue components of a single color are
                                            stored sequentially in this list.                                           */
    unsigned char *colors2;     /**< \brief Pointer to the start of the list of color components.                       */
                                /**<        A pointer to an array of chars containing the list of color components
                                            defined for this object. Each color component takes a single byte and can
                                            have a value of 0-255.
                                            The Red, Green, Blue and Alpha Channel components of a single color are
                                            stored sequentially in this list.                                           */
    char *textString;           /**< \brief Pointer to the start of a text string.                                      */
                                /**<        A pointer to a string of chars.                                             */
} Object3D;

// Object3D Methods
PyObject *Object3D_setVertCoo(Object3D *self, PyObject *args);
PyObject *Object3D_setNormCoo(Object3D *self, PyObject *args);
PyObject *Object3D_setUVCoo(Object3D *self, PyObject *args);
PyObject *Object3D_setColorIDComponent(Object3D *self, PyObject *args);
PyObject *Object3D_setColorComponent(Object3D *self, PyObject *args);
PyObject *Object3D_setTranslation(Object3D *self, PyObject *args);
PyObject *Object3D_setRotation(Object3D *self, PyObject *args);
PyObject *Object3D_setScale(Object3D *self, PyObject *args);

// Object3D attributes indirectly accessed by Python
PyObject *Object3D_getText(Object3D *self, void *closure);
int Object3D_setText(Object3D *self, PyObject *value, void *closure);

// Object3D object methods
void Object3D_dealloc(Object3D *self);
PyObject *Object3D_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
int Object3D_init(Object3D *self, PyObject *args, PyObject *kwds);

/** \brief A struct consolidating all global variables.
           A global struct - all globals must be here.
 */
typedef struct
{
    PyObject *world;
    //OBJARRAY world;                /**< \brief A pointer to the list of objects.                                           */
    /**<        A pointer to an array of object3D objects that contains the list of
                currently defined objects.                                                  */
    float fovAngle;                /**< \brief The current Field Of View angle.                                            */
    /**<        A float holding the current Field of View of the camera.                    */
    float zoom;                    /**< \brief The current camera Zoom setting.                                            */
    /**<        A float holding the current camera Zoom setting.                            */
    float rotX;                    /**< \brief The current camera rotation around the x-axis (the tilt).                   */
    /**<        A float holding the current camera x-rotation setting.                      */
    float rotY;                    /**< \brief The current camera rotation around the y-axis (left/right).                 */
    /**<        A float holding the current camera y-rotation setting.                      */
    float translX;                 /**< \brief The current camera x-translation (pan left/right).                          */
    /**<        A float holding the current camera x-translation setting.                   */
    float translY;                 /**< \brief The current camera y-translation (pan up/down).                             */
    /**<        A float holding the current camera y-translation setting.                   */
    int windowHeight;              /**< \brief The current window height in pixels.                                        */
    /**<        An int holding the current window height in pixels.                         */
    int windowWidth;               /**< \brief The current window width in pixels.                                         */
    /**<        An int holding the current window width in pixels.                          */
    int modifiersKeyState;         /**< \brief The current modifier key state (e.g. shift, ctrl, alt etc.).                */
    /**<        An int holding the current modifier key state (e.g. shift, ctrl, alt etc.). */
    unsigned char color_picked[3]; /**< \brief The 'color' of the currently selected object.                               */
    /**<        An array of three characters holding the Red, Green and Blue color
                components (each with a value from 0 to 255) of the color of the currently
                selected object.
                This is a 'false' color used as part of the technique for identifying
                objects selected with the mouse.                                            */
    /**<        An array of ints holding the list of textures.                              */
    double mouse3DX;/*mouse 3D scene coords*/
    double mouse3DY;/*mouse 3D scene coords*/
    double mouse3DZ;/*mouse 3D scene coords*/
    double mouseGUIX;/*mouse 3D GUI coords*/
    double mouseGUIY;/*mouse 3D GUI coords*/
    double mouseGUIZ;/*mouse 3D GUI coords*/
    unsigned int millisecTimer; /*millisecond delay for SDL_AddTimer*/

    int fontOffset; /*first index of the font display list*/
    int pendingUpdate; /*1 if an update is already pending*/
    int pendingTimer; /*1 if a timer is already pending*/
    int loop; /*1 if we haven't quit yet*/
    int fullscreen; /*1 for fullscreen, 0 for windowed*/
    float clearColor[4]; /*color for background clear*/
} Global;
extern Global G;

// Python callbacks
void callMouseButtonDown(int b, int x, int y);
void callMouseButtonUp(int b, int x, int y);
void callMouseMotion(int s, int x, int y, int xrel, int yrel);
void callTimerFunct(void);
void callKeyDown(int key, unsigned short character, int modifiers);
void callKeyUp(int key, unsigned short character, int modifiers);
void callReloadTextures(void);

// Scene methods
void initscene(int n);
PyObject *addObject(float locX, float locY,float locZ, int numVerts, int numTrigs);
void setClearColor(float r, float g, float b, float a);

// Helper functions
float *makeFloatArray(int n);
unsigned char *makeUCharArray(int n);
int *makeIntArray(int n);

#ifdef __cplusplus
        }
#endif
        
#endif // CORE_H
