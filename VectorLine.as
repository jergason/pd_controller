package 
{
	import flash.display.MovieClip;
	
	/**
	 * ...
	 * @author Kason McEwen
	 */
	public class VectorLine extends MovieClip 
	{
		private var maxWidth:Number = 30;
		
		public function VectorLine() {
			mouseChildren = mouseEnabled = false;
		}
		
		public function setComponents(dx:Number,dy:Number):void {
			
			
			var newWidth = 1/10*Math.sqrt(dx * dx + dy * dy);
			
			if (newWidth > maxWidth) {
				line.width = maxWidth;
			}
			else {
				line.width = newWidth;
			}
			rotation = Math.atan2(dy, dx) * 180 / Math.PI;			
			head.x = line.width;
			
		}
		
	}
	
}