var CANVAS_WIDTH = 1360;
var CANVAS_HEIGHT = 540;

var EDGEBOARD_X = 330;
var EDGEBOARD_Y = 0;

var FONT = "gotham_boldregular";

var NUM_LEVELS      = 10;
var NUM_CARS        = 18;
var NUM_CONTAINERS  = 8;

var FPS_TIME      = 1000/24;
var DISABLE_SOUND_MOBILE = false;

var LEVEL_TIME;
var MIN_SPEED_OFFSET;
var SOUNDTRACK_VOLUME_IN_GAME  = 0.5;

var STATE_LOADING = 0;
var STATE_MENU    = 1;
var STATE_HELP    = 1;
var STATE_GAME    = 3;

var LEFT_DIR      = 37;
var UP_DIR        = 38;
var RIGHT_DIR     = 39;
var DOWN_DIR      = 40;
var SPACEBAR      = 32;

var ON_MOUSE_DOWN  = 0;
var ON_MOUSE_UP    = 1;
var ON_MOUSE_OVER  = 2;
var ON_MOUSE_OUT   = 3;
var ON_DRAG_START  = 4;
var ON_DRAG_END    = 5;
var ON_BUT_NO_DOWN = 6;
var ON_BUT_YES_DOWN = 7;

var ENABLE_FULLSCREEN;
var ENABLE_CHECK_ORIENTATION;