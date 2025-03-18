from .. import bridge

bridge.ffi.cdef("""//cpp
typedef unsigned int Uint32;
typedef unsigned short Uint16;
typedef unsigned char Uint8;
typedef unsigned long long Uint64;
typedef int32_t Sint32;

typedef Uint32 SDL_KeyboardID;
typedef Uint32 SDL_EventType;
typedef Uint32 SDL_Scancode;
typedef Uint32 SDL_Keycode;
typedef Uint32 SDL_WindowID;
typedef Uint16 SDL_Keymod;

bool SDL_Init(Uint32 flags);
void SDL_Quit(void);

// window
typedef struct SDL_Window SDL_Window;
SDL_Window* SDL_CreateWindow(const char* title, int w, int h, Uint32 flags);
void SDL_DestroyWindow(SDL_Window* window);
bool SDL_SetWindowSize(SDL_Window* window, int w, int h);
bool SDL_ShowWindow(SDL_Window* window);
bool SDL_HideWindow(SDL_Window* window);
bool SDL_MinimizeWindow(SDL_Window* window);
SDL_WindowID SDL_GetWindowID(SDL_Window *window);

// renderer
typedef struct SDL_Renderer SDL_Renderer;
SDL_Renderer * SDL_CreateRenderer(SDL_Window *window, const char *name);
void SDL_DestroyRenderer(SDL_Renderer* renderer);
bool SDL_SetRenderDrawColor(SDL_Renderer* renderer, Uint8 r, Uint8 g, Uint8 b, Uint8 a);
bool SDL_RenderClear(SDL_Renderer* renderer);
bool SDL_RenderPresent(SDL_Renderer* renderer);
bool SDL_RenderFillRect(SDL_Renderer* renderer, const void *rect);

const char* SDL_GetError(void);


/* For SDL3, you might also query display info.
   (Add additional SDL3-specific functions here as needed.) */
  
typedef struct SDL_Rect {
    int x;
    int y;
    int w;
    int h;
} SDL_Rect;

// event
SDL_Keycode SDL_GetKeyFromScancode(SDL_Scancode scancode, SDL_Keymod modstate, bool key_event);
const char * SDL_GetKeyName(SDL_Keycode key);

typedef struct {
    Uint32 type;
    Uint32 timestamp;
} SDL_CommonEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int display;
    int event;
    int data1;
} SDL_DisplayEvent;

typedef struct {
    SDL_EventType type;
    Uint32 reserved;
    Uint64 timestamp; 
    SDL_WindowID windowID; 
    Sint32 data1;  
    Sint32 data2;   
} SDL_WindowEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int which;
} SDL_KeyboardDeviceEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int windowID;
    int state;
    int repeat;
    int keysym;  /* placeholder for actual SDL_Keysym */
} SDL_KeyboardEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    char text[32];
    int start;
    int length;
} SDL_TextEditingEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int numCandidates;
} SDL_TextEditingCandidatesEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int windowID;
    char text[32];
} SDL_TextInputEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int which;
} SDL_MouseDeviceEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int windowID;
    int which;
    int state;
    int x;
    int y;
    int xrel;
    int yrel;
} SDL_MouseMotionEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int windowID;
    int which;
    int button;
    int state;
    int clicks;
    int x;
    int y;
} SDL_MouseButtonEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int windowID;
    int which;
    int x;
    int y;
    Uint32 direction;
} SDL_MouseWheelEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int which;
} SDL_JoyDeviceEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int which;
    int axis;
    int value;
} SDL_JoyAxisEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int which;
    int ball;
    int xrel;
    int yrel;
} SDL_JoyBallEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int which;
    int hat;
    int value;
} SDL_JoyHatEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int which;
    int button;
    int state;
} SDL_JoyButtonEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int which;
    int battery;
} SDL_JoyBatteryEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int which;
} SDL_GamepadDeviceEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int which;
    int axis;
    int value;
} SDL_GamepadAxisEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int which;
    int button;
    int state;
} SDL_GamepadButtonEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int which;
    int touchpad;
    int finger;
    float x;
    float y;
    float pressure;
} SDL_GamepadTouchpadEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int which;
    int sensor;
    float data[3];
} SDL_GamepadSensorEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int which;
    int iscapture;
} SDL_AudioDeviceEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int which;
} SDL_CameraDeviceEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int which;
    int sensor;
    float data[6];
} SDL_SensorEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
} SDL_QuitEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int windowID;
    int code;
    void* data1;
    void* data2;
} SDL_UserEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int windowID;
    long long touchId;
    long long fingerId;
    float x;
    float y;
    float dx;
    float dy;
    float pressure;
} SDL_TouchFingerEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int windowID;
    int which;
    int state;
    int x;
    int y;
} SDL_PenProximityEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int windowID;
    int which;
    int state;
    int x;
    int y;
    int pressure;
} SDL_PenTouchEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int windowID;
    int which;
    int x;
    int y;
    int xrel;
    int yrel;
    int pressure;
} SDL_PenMotionEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int windowID;
    int which;
    int button;
    int state;
    int x;
    int y;
} SDL_PenButtonEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int windowID;
    int which;
    int axis;
    int value;
} SDL_PenAxisEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    int data1;
} SDL_RenderEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
    char file[520];
} SDL_DropEvent;

typedef struct {
    Uint32 type;
    Uint32 timestamp;
} SDL_ClipboardEvent;

// /* The complete SDL_Event union */
typedef union SDL_Event {
    Uint32 type;
    SDL_CommonEvent common;
    SDL_DisplayEvent display;
    SDL_WindowEvent window;
    SDL_KeyboardDeviceEvent kdevice;
    SDL_KeyboardEvent key;
    SDL_TextEditingEvent edit;
    SDL_TextEditingCandidatesEvent edit_candidates;
    SDL_TextInputEvent text;
    SDL_MouseDeviceEvent mdevice;
    SDL_MouseMotionEvent motion;
    SDL_MouseButtonEvent button;
    SDL_MouseWheelEvent wheel;
    SDL_JoyDeviceEvent jdevice;
    SDL_JoyAxisEvent jaxis;
    SDL_JoyBallEvent jball;
    SDL_JoyHatEvent jhat;
    SDL_JoyButtonEvent jbutton;
    SDL_JoyBatteryEvent jbattery;
    SDL_GamepadDeviceEvent gdevice;
    SDL_GamepadAxisEvent gaxis;
    SDL_GamepadButtonEvent gbutton;
    SDL_GamepadTouchpadEvent gtouchpad;
    SDL_GamepadSensorEvent gsensor;
    SDL_AudioDeviceEvent adevice;
    SDL_CameraDeviceEvent cdevice;
    SDL_SensorEvent sensor;
    SDL_QuitEvent quit;
    SDL_UserEvent user;
    SDL_TouchFingerEvent tfinger;
    SDL_PenProximityEvent pproximity;
    SDL_PenTouchEvent ptouch;
    SDL_PenMotionEvent pmotion;
    SDL_PenButtonEvent pbutton;
    SDL_PenAxisEvent paxis;
    SDL_RenderEvent render;
    SDL_DropEvent drop;
    SDL_ClipboardEvent clipboard;
    Uint8 padding[128];
} SDL_Event;
bool SDL_PollEvent(SDL_Event *event);
""")