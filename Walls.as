package 
{
	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.ui.Mouse;
	
	/**
	 * ...
	 * @author Kason McEwen
	 */
	public class Walls extends Draggable 
	{
		private var wallSegments:Array = [];
		private var crossHairs:MovieClip;
		
		public function Walls() {			
			crossHairs = crossHairsInstance;
			crossHairs.visible = false;
			crossHairs.mouseEnabled = crossHairs.mouseChildren = false;
		}
		
		
		public function addWallMode():void {
			trace("add wall mode??");
			addEventListener(Event.ENTER_FRAME, followMouse);
			Mouse.hide();
			stage.addChild(crossHairs);
			crossHairs.visible = true;
			stage.addEventListener(MouseEvent.CLICK, addWall);
		}
		
		public function leaveWallMode():void {
			stage.removeEventListener(MouseEvent.CLICK, addWall);
			addEventListener(Event.ENTER_FRAME, followMouse);
			crossHairs.visible = false;
			Mouse.show();
		}
		
		
		private function followMouse(e:Event):void 
		{
			crossHairs.x = mouseX;
			crossHairs.y = mouseY;
		}
		
		
		
		private function addWall(e:MouseEvent):void {
			var wall:WallSegment = new WallSegment();
			wall.x = mouseX;
			wall.y = mouseY;
			addChild(wall);
			leaveWallMode();
		}
		
		
	}
	
}