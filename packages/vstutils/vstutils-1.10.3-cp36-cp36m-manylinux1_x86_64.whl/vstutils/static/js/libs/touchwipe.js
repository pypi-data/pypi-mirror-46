(function($){$.fn.touchwipe=function(settings)
{var config={min_move_x:20,min_move_y:20,wipingLeft:function(){},wipingRight:function(){},wipingUp:function(){},wipingDown:function(){},wipingLeftEnd:function(){},wipingRightEnd:function(){},wipingUpEnd:function(){},wipingDownEnd:function(){},preventDefaultEvents:true};if(settings)$.extend(config,settings);this.each(function()
{var startX;var startY;var isMoving=false;var isStartWipingLeft=false;var isStartWipingRight=false;var isStartWipingDown=false;var isStartWipingUp=false;var lastPageX=0;var lastPageY=0;function onTouchEnd(e)
{var x=lastPageX;var y=lastPageY;var dx=startX-x;var dy=startY-y;var wipingEndEvent={dx:dx,dy:dy,event:e,}
this.removeEventListener('touchmove',onTouchMove);this.removeEventListener('touchend',onTouchEnd);if(isStartWipingLeft)
{wipingEndEvent.isFull=dx>=(config.min_move_x)
config.wipingLeftEnd(wipingEndEvent);}
if(isStartWipingRight)
{wipingEndEvent.isFull=(-dx)>=(config.min_move_x)
config.wipingRightEnd(wipingEndEvent);}
if(isStartWipingUp)
{wipingEndEvent.isFull=dy>=(config.min_move_x)
config.wipingUpEnd(wipingEndEvent);}
if(isStartWipingDown)
{wipingEndEvent.isFull=(-dy)>=(config.min_move_x)
config.wipingDownEnd(wipingEndEvent);}
startX=null;isMoving=false;isStartWipingLeft=false;isStartWipingRight=false;isStartWipingDown=false;isStartWipingUp=false;}
function onTouchMove(e)
{if(config.preventDefaultEvents)
{e.preventDefault();}
if(isMoving)
{var x=e.touches[0].pageX;var y=e.touches[0].pageY;lastPageX=x;lastPageY=y;var dx=startX-x;var dy=startY-y;var wipingEvent={dx:dx,dy:dy,event:e,}
if(Math.abs(dx)>=config.min_move_x)
{if(dx>0)
{isStartWipingLeft=true;config.wipingLeft(wipingEvent);}
else
{isStartWipingRight=true;config.wipingRight(wipingEvent);}}
else if(Math.abs(dy)>=config.min_move_y)
{if(dy>0)
{isStartWipingDown=true;config.wipingDown(wipingEvent);}
else
{isStartWipingUp=true;config.wipingUp(wipingEvent);}}}}
function onTouchStart(e)
{if(e.touches.length==1)
{startX=e.touches[0].pageX;startY=e.touches[0].pageY;isMoving=true;this.addEventListener('touchmove',onTouchMove,false);this.addEventListener('touchend',onTouchEnd,false);}}
if('ontouchstart'in document.documentElement)
{this.addEventListener('touchstart',onTouchStart,false);}});return this;};})(jQuery);