package 
{
	import flash.display.MovieClip;
	import flash.events.MouseEvent;
	
	/**
	 * ...
	 * @author Kason McEwen
	 */
	public class Draggable extends MovieClip
	{
		
		public function Draggable():void{
			addEventListener(MouseEvent.MOUSE_DOWN, drag);
		}
		
		private function drag(e:MouseEvent):void {
			startDrag();
			stage.addEventListener(MouseEvent.MOUSE_UP, drop);
		}
		
		private function drop(e:MouseEvent):void 
		{
			stopDrag();
		}
		
	}
	
}