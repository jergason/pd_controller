package 
{
	import fl.controls.Button;
	import fl.motion.MotionEvent;
	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.ui.Mouse;
	
	/**
	 * ...
	 * @author Kason McEwen
	 */
	public class AddItemsPanel extends MovieClip
	{
		private var addTankBtn:Button;
		private var addRepulsiveBtn:Button;
		private var addTangentialBtn:Button;
		private var randomTankBtn:Button;
		private var addWallBtn:Button;
		
		public function AddItemsPanel():void {
			addWallBtn = addWallBtnInstance;
			addTankBtn = addTankBtnInstance;
			addRepulsiveBtn = addRepulsiveBtnInstance;
			addTangentialBtn = addTangentialBtnInstance;
			randomTankBtn = randomTankBtnInstance;
			
			addTankBtn.addEventListener(MouseEvent.MOUSE_DOWN, addTank);
			addRepulsiveBtn.addEventListener(MouseEvent.MOUSE_DOWN, addRepulsive);
			addTangentialBtn.addEventListener(MouseEvent.MOUSE_DOWN, addTangential);
			addWallBtn.addEventListener(MouseEvent.MOUSE_DOWN, addWall);
			randomTankBtn.addEventListener(MouseEvent.MOUSE_DOWN, randomizeTanks);
			
		}
		
		private function addWall(e:MouseEvent):void {
			dispatchEvent(new Event("addWall"));
		}
		
		private function addTangential(e:MouseEvent):void 
		{
			dispatchEvent(new Event("addTangential"));
		}
		
		private function addRepulsive(e:MouseEvent):void 
		{
			dispatchEvent(new Event("addRepulsive"));
		}
		
		private function addTank(e:MouseEvent):void 
		{
			dispatchEvent(new Event("addTank"));
		}
		
		private function randomizeTanks(e:MouseEvent):void {
			dispatchEvent(new Event("randomizeTanks"));
		}
	}
	
}