package 
{
	import flash.display.MovieClip;
	import flash.events.MouseEvent;
	
	/**
	 * ...
	 * @author Kason McEwen
	 */
	public class FieldObject extends Draggable 
	{
		
		private var radius:Number;
		private var defaultRadius:Number = 80;
		
		public function FieldObject():void {
			radius = defaultRadius;
			alpha = .5;
			
		}

		public function getRadius():Number {
			return radius;
		}
		
		public function setRadius(r:Number){
			radius = r;
		}
		
	}
	
}