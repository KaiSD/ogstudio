# Introduction #

As Mahjong 1.0 approaches, I have a wish to try out other engines to see if they possibly fit better than what we use. To speed up the process, I need to know what we use exactly.

# OGRE #
MJIN:
  * Ogre::Singleton template;
  * Ogre::LogManager to redirect OGRE internal logging to Mahjong log;
  * Ogre::String type (aka typedef std::string);
  * Ogre::ConfigFile to read INI-like files;
  * Ogre::DataStream(Ptr) to manage sound streams as Ogre resources;
  * Ogre::Resource to manage sound buffers (small sound files like Click.ogg) as Ogre resources;
  * Ogre::ResourceManager to manage sound resources in Ogre resource system;
  * Ogre::RenderWindow for display and input;
  * Ogre::RenderSystemCapabilities to get info about OpenGL and videocard;
  * Ogre::StringConverter to convert int/float to String and vice versa;
  * Ogre::StringUtil for simple pattern matching, string replacing, splitting by token;
  * Ogre::Texture(Ptr) for render to texture of CEGUI;
  * Ogre::Camera to view scene;
  * Ogre::SceneManager to manage nodes;
  * Ogre::Vector3 for position;
  * Ogre::Quaternion for rotation;
  * Ogre::Degree to convert degree to radian for rotation;
  * Ogre::SceneNode/Entity to present visual entities like tiles, environment, etc which are able to pitch/yaw/roll;
  * Ogre::ColourValue to represent RGBA colour of lighting, material colour, etc.;
  * Ogre::MeshManager to manage meshes, scene meshes;
  * Ogre::Skybox/dome for skybox/dome;
  * Ogre::Light for lights (we use point light);
  * Ogre::MaterialManager to manage themes;
  * Ogre::WindowEventUtitilies to accept RenderWindow events at desired times (each run cycle), to accept close/resize/focus change events;
  * Ogre::RenderWindow::FrameStats to get FPS and polycount statistics;
  * game window recreation capability without reloading resources which is achieved by hiding the first RenderWindow and displaying the second one;
  * convenient material scripts even with inheritance;
  * Blender OGRE script that converts meshes to XML format;
  * OgreXMLConverter that converts XML mesh format to binary one understandble by Ogre::MeshManager.

MJ:
  * Ogre::ResourceGroupManager to manage groups of resources (scenes/themes);
  * MJ LayoutManager resigered as OgreResourceManager for easy layout handling;
  * Ogre::OverlayManager to display background for menu, lose/win screens;
  * Ogre::Ray/SceneQuery/Result to select object by mouse clicks (ray tracing);
  * Ogre::Viewport as a layer between Ogre::RenderWindow and Ogre::Camera, also allows to switch shadowing on/off;
  * Ogre::TextureFilterOptions for graphics quality settings;
  * Ogre::RenderTexture for RTT;
  * Ogre::ManualObject to draw Shisen-Sho path lines.

# OIS #
MJIN:
  * OIS::InputManager/Keyboard/Mouse to create/manage keyboard and mouse listeners;
  * OIS::Key/MouseEvent;
  * OIS::MouseButtonID;
  * Key enum values;
  * keyPress/Release;
  * mouseMove/Press/Release.

# CEGUI #
MJIN:
  * CEGUI::MultiColumnList for table-like display;
  * CEGUI::ListBox (with possibility to center contents);
  * CEGUI::Combobox;
  * CEGUI::Window for static text windows (descriptions);
  * CEGUI::PushButton;
  * CEGUI::Key/Window/EventArgs for key/window/general events;
  * CEGUI::Key enum;
  * CEGUI::Event::Subscriber for subscribing to events;
  * CEGUI::Editbox;
  * CEGUI::Scrollbar;
  * Scrolled area that we fill with text and it adds Scrollbar;
  * CEGUI::WindowManager to manage windows/dialogs;
  * CEGUI::utf8 to convert C strings to CEGUI ones;
  * CEGUI::String to represent GUI strings;
  * Redirecting CEGUI internal logging to Mahjong log;
  * Recreating GUI after recreating second Ogre::RenderWindow used for display;
  * CEGUI fonts/imagesets/layouts/looknfeel/schemes all handled by CEGUI Ogre resource manager without a problem;
  * CEGUI::MouseCursor;
  * CEGUI::OgreRenderer for easy CEGUI Ogre integration;
  * CEGUI::Texture/Imageset for RTT;
  * CEGUI::Right/Middel/LeftButton for mouse buttons;
  * Injecting key/mouse events into CEGUI.

MJ:
  * CEGUI::Image for RTT;
  * CEGUI::UVector2/URect/UDim for relational widget positioning;
  * CEGUI::FontManager/ImagesetManager for re-scaling GUI after game window resize.